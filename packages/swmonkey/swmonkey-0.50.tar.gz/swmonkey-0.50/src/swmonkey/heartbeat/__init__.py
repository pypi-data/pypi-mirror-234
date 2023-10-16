import requests
import time
from threading import Thread
from swmonkey.log.log import logger
import os
INTERVAL = 5


def send_heartbeat():
    HEARTBEAT_URL = os.getenv('HEARTBEAT_URL')
    print("HEARTBEAT_URL: ", HEARTBEAT_URL)
    assert HEARTBEAT_URL is not None
    while True:
        try:
            requests.post(f'{HEARTBEAT_URL}/heartbeat',
                          json={'status': 'running'})
        except Exception as e:
            print(e)
            logger.error(e)
        time.sleep(INTERVAL)


def finish_heartbeat():
    try:
        HEARTBEAT_URL = os.getenv('HEARTBEAT_URL')
        requests.post(f'{HEARTBEAT_URL}/finish', json={'status': 'finished'})
        logger.info('Finish sending heartbeat')
    except Exception as e:
        print(e)
        logger.error(e)
