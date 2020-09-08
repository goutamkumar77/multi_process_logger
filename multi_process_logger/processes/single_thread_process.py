import logging
import threading
import time

# level defined for this process only
logging_level = logging.DEBUG

def thread1():
    global log_msg

    while True:
        log_msg.debug("Ack from Process1 Thread1")
        time.sleep(1)

def single_thread_process():
    global log_msg
    global logging_level

    log_msg = logging.getLogger(__name__)
    log_msg.setLevel(logging_level)
    log_msg.info("Single Thread Process started")

    try:
        child_thread = threading.Thread(target=thread1, name="Thread1")
        child_thread.start()

    except Exception:
        log_msg.error("Could not start child thread")

    while True:
        log_msg.info("Ack from Process1 MainThread")
        time.sleep(1)