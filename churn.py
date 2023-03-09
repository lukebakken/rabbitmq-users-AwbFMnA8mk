# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103,R0205

import logging
import threading
import pika
import random
import socket
import time

LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.ERROR, format=LOG_FORMAT)

stopping = False

threads = []


def do_work_0(i):
    while True and not stopping:
        thread_id = threading.get_ident()
        LOGGER.info("i: %s pika thread id: %s", i, thread_id)
        credentials = pika.PlainCredentials("guest", "guest")
        p = 5672
        parameters = pika.ConnectionParameters(
            host="localhost", port=p, credentials=credentials, heartbeat=5
        )
        connection = pika.BlockingConnection(parameters)
        # for i in range(1, random.randrange(5, 10)):
        #    connection.channel()
        connection.process_data_events(time_limit=random.randrange(5, 10))
        connection.close()


def do_work_1(i):
    thread_id = threading.get_ident()
    LOGGER.info("i: %s socket thread id: %s", i, thread_id)
    while True and not stopping:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 5672))
        time.sleep(random.randrange(0, 10))
        s.close()


for i in range(0, 8):
    t0 = threading.Thread(target=do_work_0, args=(i,))
    t0.start()
    threads.append(t0)
    t1 = threading.Thread(target=do_work_1, args=(i,))
    t1.start()
    threads.append(t1)

input("ANY KEY TO STOP")
print()
stopping = True
# Wait for all to complete
for thread in threads:
    thread.join()
