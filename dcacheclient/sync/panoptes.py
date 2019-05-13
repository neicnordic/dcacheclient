"""
   panoptes: Service to synchronise storage.
"""

import json
import logging
import os
import requests
import traceback
import time

try:
    from queue import Queue
except ImportError:
    import Queue

from threading import Thread

try:
    from urlparse import urljoin, urlparse
except:
    from urllib.parse import urljoin, urlparse

from sseclient import SSEClient

_LOGGER = logging.getLogger(__name__)


def submit_transfer_to_fts(source_url, bytes, adler32, destination_url, proxy, fts_host):
    transfer_request = {'files': [{
        'sources': [source_url],
        'destinations': [destination_url],
        'filesize': bytes,
        'checksum': 'adler32:%s' % adler32}],
        'params': {'verify_checksum': True}}

    # response = session.get('%s/api-docs/schema/submit' % fts_host)
    # schema = response.json()
    # from jsonschema import validate
    # print (validate(instance=transfer_request, schema=schema))

    response = requests.post(
        '%s/jobs' % fts_host,
        json=transfer_request,
        cert=proxy,
        headers={'Content-Type': 'application/json'})
    # if response.status_code == 200:
    _LOGGER.info("Transfer from {} to {} has been submitted to FTS ({})".format(source_url, destination_url, response.content))


def do_replication(session, new_files):
    while True:
        try:
            source_url, destination_url, fts_host = new_files.get()
            # Workaround: slight risk the client receives the `IN_CLOSE_WRITE`
            # event before the upload is completed. TBR.
            for _ in range(10):
                # Get this info with dav
                # Can use the namespace operation later
                response = session.head(source_url, headers={'Want-Digest': 'adler32'})
                if response.status_code == 200:
                    break
                time.sleep(0.1)
            _LOGGER.debug(response.headers)

            adler32 = response.headers['Digest'].replace('adler32=', '')
            bytes = int(response.headers['Content-Length'])
            submit_transfer_to_fts(
                source_url=source_url,
                bytes=bytes,
                adler32=adler32,
                destination_url=destination_url,
                proxy=session.cert,
                fts_host=fts_host)
        except:
            _LOGGER.error(traceback.format_exc())
        finally:
            new_files.task_done()


def main(root_path, source, destination, client, fts_host, recursive):
    '''
    main function
    '''
    new_files = Queue(maxsize=0)
    worker = Thread(target=do_replication, args=(client.session, new_files,))
    worker.setDaemon(True)
    worker.start()

    base_path = urlparse(source).path
    paths = [os.path.normpath(root_path + '/' + base_path)]
    if recursive:
        directories = [urlparse(source).path]
        _LOGGER.debug("Scan {}".format(base_path))
        while directories:
            prefix = directories.pop()
            response = client.namespace.get_file_attributes(path=prefix, children=True)
            for entry in response["children"]:
                if entry["fileType"] == "DIR":
                    directory = os.path.normpath(prefix + '/' + entry["fileName"])
                    _LOGGER.debug("Directory found {}".format(directory))
                    directories.append(directory)
                    paths.append(os.path.normpath(root_path + '/' + directory))

    watches = {}
    while True:
        response = client.events.register()
        channel = response.headers['Location']
        _LOGGER.info("Channel is {}".format(channel))

        id = channel[channel.find('/api/v1/events/channels/') + 24:]

        for path in paths:
            response = client.events.subscribe(type='inotify', id=id, body={"path": path})
            watch = response.headers['Location']
            _LOGGER.debug("Watch on {} is {}".format(path, watch))
            watches[watch] = path

        messages = SSEClient(channel, session=client.session)
        try:
            for msg in messages:
                _LOGGER.debug("Event {}:".format(msg.id))
                _LOGGER.debug("    event: {}".format(msg.event))
                _LOGGER.debug("    data: {}".format(msg.data))
                data = json.loads(msg.data)
                if 'event' in data and data['event']['mask'] == ['IN_CLOSE_WRITE']:
                    name = data['event']['name']
                    full_path = watches[data["subscription"]]
                    short_path = os.path.relpath(full_path, root_path)[len(base_path) - 1:]
                    source_url = urljoin(source, os.path.normpath(short_path + '/' + name))
                    _LOGGER.info('New file detected: ' + source_url)
                    print (source_url[len(source):])
                    destination_url = urljoin(destination, os.path.normpath(source_url[len(source):]))
                    _LOGGER.info('Request to copy it to: ' + destination_url)

                    new_files.put((source_url, destination_url, fts_host))
                elif 'event' in data and data['event']['mask'] == ["IN_CREATE", "IN_ISDIR"]:
                    name = data['event']['name']
                    full_path = watches[data["subscription"]]
                    dir_path = os.path.normpath(full_path + '/' + name)
                    _LOGGER.info('New directory detected: ' + dir_path)
                    response = client.events.subscribe(type='inotify', id=id, body={"path": dir_path})
                    watch = response.headers['Location']
                    _LOGGER.debug("Watch on {} is {}".format(dir_path, watch))
                    watches[watch] = dir_path
                    paths.append(dir_path)

        except requests.exceptions.HTTPError as exc:
            _LOGGER.error(str(exc))
#           raise
            _LOGGER.info('Re-register and Re-subscribe to channel')
