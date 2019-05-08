"""
   panoptse: Synchronise storage.
"""

import json
import logging
import requests
import traceback
import time

try:
    from queue import Queue
except ImportError:
    import Queue

from threading import Thread

try:
    from urlparse import urljoin
except:
    from urllib.parse import urljoin

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

    response = requests.post('%s/jobs' % fts_host,
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
                response = session.get(source_url, headers={'Want-Digest': 'adler32'})
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


def main(path, source, destination, client, fts_host):
    '''
    main function
    '''
    new_files = Queue(maxsize=0)
    worker = Thread(target=do_replication, args=(client.session, new_files,))
    worker.setDaemon(True)
    worker.start()

    while True:
        response = client.events.register()
        channel = response.headers['Location']
        _LOGGER.info("Channel is {}".format(channel))

        id = channel[channel.find('/api/v1/events/channels/') + 24:]

        response = client.events.subscribe(type='inotify', id=id, body={"path": path})
        watch = response.headers['Location']
        _LOGGER.debug("Watch on {} is {}".format(path, watch))
        messages = SSEClient(channel, session=client.session)
        try:
            for msg in messages:
                _LOGGER.debug("Event {}:".format(msg.id))
                _LOGGER.debug("    event: {}".format(msg.event))
                _LOGGER.debug("    data: {}".format(msg.data))
                data = json.loads(msg.data)
                if data['event']['mask'] == ['IN_CLOSE_WRITE']:
                    name = data['event']['name']
                    source_url = urljoin(source, name)
                    _LOGGER.info('New file detected: ' + source_url)
                    destination_url = urljoin(destination, name)
                    _LOGGER.info('Request to copy it to: ' + destination_url)
                    new_files.put((source_url, destination_url, fts_host))
        except requests.exceptions.HTTPError as exc:
            _LOGGER.error(str(exc))
#           raise
            _LOGGER.info('Re-register and Re-subscribe to channel')
