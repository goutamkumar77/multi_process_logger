import logging
import threading
import time

# level defined for this process only
logging_level = logging.DEBUG

def thread1():
    global log_msg

    while True:
        log_msg.debug("Ack from Process2 Thread1")
        time.sleep(1)


def thread2():
    global log_msg

    while True:
        log_msg.debug("Ack from Process2 Thread2")
        time.sleep(1)

def multi_thread_process():
    global log_msg
    global logging_level

    log_msg = logging.getLogger(__name__)
    log_msg.setLevel(logging_level)
    log_msg.info("Multi Thread Process started")

    try:
        child_thread1= threading.Thread(target=thread2, name="Thread1")
        child_thread2 = threading.Thread(target=thread2, name="Thread2")
        child_thread1.start()
        child_thread2.start()

    except Exception:
        log_msg.error("Could not start child threads")

    while True:
        log_msg.info("Ack from Process2 MainThread")
        time.sleep(1)