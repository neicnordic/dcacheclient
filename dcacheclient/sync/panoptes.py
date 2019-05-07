import json
import logging
import requests

#  try:
#     from queue import Queue
#  except ImportError:
#     import Queue as queue
# from threading import Thread

from sseclient import SSEClient


_DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

_LOGGER = logging.getLogger(__name__)


def _configure_logging():
    _LOGGER.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()

    formatter = logging.Formatter(_DEFAULT_LOG_FORMAT)
    ch.setFormatter(formatter)

    _LOGGER.addHandler(ch)


def main(path, destination, client):
    '''
    main function
    '''
    _configure_logging()

#    new_files = Queue(maxsize=0)
#    worker = Thread(target=do_stuff, args=(new_files, storage, rse, scope, proxy))
#    worker.setDaemon(True)
#    worker.start()

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
                    source_url = 'https://' + name
                    _LOGGER.info('New file detected: ' + source_url)
                    destination_url = 'https://' + name
                    _LOGGER.info('Request to copy it to: ' + destination_url)
#        if data['event']['mask'] == ['IN_ATTRIB']:
#            # new file
#            name = data['event']['name']
#            new_file = storage + path + '/' + name
#            _LOGGER.info('New file detected: ' + new_file)
#            new_files.put((name, new_file))
        except requests.exceptions.HTTPError as exc:
            _LOGGER.error(str(exc))
            if exc.response.status_code != 404:
                raise
            _LOGGER.info('Re-register and Re-subscribe to channel')
