# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103,R0205

import logging
import threading
import pika
import random
import socket

LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.ERROR, format=LOG_FORMAT)

threads = []


def do_work_0(stop_event: threading.Event, i: int):
    while not stop_event.is_set():
        thread_id = threading.get_ident()
        LOGGER.info("i: %s pika thread id: %s", i, thread_id)
        credentials = pika.PlainCredentials("guest", "guest")
        p = 5672
        parameters = pika.ConnectionParameters(
            host="localhost", port=p, credentials=credentials, heartbeat=5
        )
        connection = None
        try:
            connection = pika.BlockingConnection(parameters)
            for i in range(1, random.randrange(5, 10)):
                connection.channel()
            connection.process_data_events(time_limit=random.randrange(5, 10))
        finally:
            if connection is not None:
                connection.close()


def do_work_1(stop_event: threading.Event, i: int):
    thread_id = threading.get_ident()
    LOGGER.info("i: %s socket thread id: %s", i, thread_id)
    while not stop_event.is_set():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 5672))
        stop_event.wait(random.randrange(0, 10))
        s.close()


stop_event = threading.Event()

for i in range(0, 32):
    t0 = threading.Thread(target=do_work_0, args=(stop_event, i))
    t0.start()
    threads.append(t0)
    t1 = threading.Thread(target=do_work_1, args=(stop_event, i))
    t1.start()
    threads.append(t1)

input("ANY KEY TO STOP")
print()
stop_event.set()
# Wait for all to complete
for thread in threads:
    thread.join()
