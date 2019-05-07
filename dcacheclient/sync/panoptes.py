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


_DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

_LOGGER = logging.getLogger(__name__)


def _configure_logging():
    _LOGGER.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()

    formatter = logging.Formatter(_DEFAULT_LOG_FORMAT)
    ch.setFormatter(formatter)

    _LOGGER.addHandler(ch)


def do_replication(session, new_files):
    while True:
        try:
            source_url, destination_url = new_files.get()
            _LOGGER.info(source_url)
            _LOGGER.info(destination_url)
            for _ in range(10):
                response = session.get(source_url, headers={'Want-Digest': 'adler32'})
                if response.status_code == 200:
                    break
                time.sleep(0.1)
            _LOGGER.info(response.headers)
            adler32 = response.headers['Digest'].replace('adler32=', '')
            bytes = response.headers['Content-Length']
#            replica  = {
#                'pfn': new_file,
#                'bytes': int(bytes),
#                'adler32': adler32}
        except:
            _LOGGER.error(traceback.format_exc())

        finally:
            new_files.task_done()


def main(path, source, destination, client):
    '''
    main function
    '''
    _configure_logging()

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
        _LOGGER.info("Watch on {} is {}".format(path, watch))
        messages = SSEClient(channel, session=client.session)
        try:
            for msg in messages:
                _LOGGER.info("Event {}:".format(msg.id))
                _LOGGER.info("    event: {}".format(msg.event))
                _LOGGER.info("    data: {}".format(msg.data))
                data = json.loads(msg.data)
                if data['event']['mask'] == ['IN_CREATE']:
                    name = data['event']['name']
                    source_url = urljoin(source, name)
                    _LOGGER.info('New file detected: ' + source_url)
                    destination_url = urljoin(destination, name)
                    _LOGGER.info('Request to copy it to: ' + destination_url)
                    new_files.put((source_url, destination_url))
        except requests.exceptions.HTTPError as exc:
            _LOGGER.error(str(exc))
#           raise
            _LOGGER.info('Re-register and Re-subscribe to channel')
