# ------------ IMPORT MODULES -------
import os
import threading
import logging
import sys
import multiprocessing
import threading
import time

from config_manager.config_logger import logger_configurer, root_configurer
from processes.single_thread_process import single_thread_process
from processes.multi_thread_process import multi_thread_process

# DEBUG
# INFO
# WARNING
# ERROR
logging_level = logging.DEBUG
log_msg = 0

def multi_process_logging(queue):
    logger_configurer()
    while True:
        while not queue.empty():
            record = queue.get()
            logger = logging.getLogger(record.name)
            logger.handle(record)

def init_multi_process_logger():
    global logging_level

    logger_queue = multiprocessing.Queue(-1)

    # handling all logging activities in a seperate thread
    try:
        logging_process = multiprocessing.Process(target=multi_process_logging, 
                                                    args=(logger_queue,))
        logging_process.start()

    except Exception:
        print("Could not start logging thread")
        return 0

    root_configurer(logger_queue)  

    log_obj = logging.getLogger(__name__)

    return log_obj

def main_child_thread():
    global log_msg

    while True:
        log_msg.debug("Ack from MainProcess ChildThread!!!")
        time.sleep(1)


def main():
    global log_msg

    print("+-------------------------------------------------------------------+")
    print("|                                                                   |")
    print("|                  Multi Process Logger Application                 | ")
    print("|                                                                   |")
    print("+-------------------------------------------------------------------+")

    log_msg = init_multi_process_logger()

    if not log_msg:
        return

    log_msg.info("Yay! Logging started")

    # Create an Event object useful to signal all process to terminate
    shutdown = multiprocessing.Event()
    shutdown.clear()

    # start main_child_thread
    try:
        child_thread = threading.Thread(target=main_child_thread, name="Thread1")
        child_thread.start()
    
    except Exception:
        log_msg.error("Could not start main_child_thread")

    # start other processes
    try:
        process_1 = multiprocessing.Process(target=single_thread_process,
                                            name="Process1")

        process_2 = multiprocessing.Process(target=multi_thread_process,
                                            name="Process2")

        process_1.start()
        log_msg.info("Process_1 started")

        process_2.start()
        log_msg.info("Process_1 started")

    except KeyboardInterrupt:
        shutdown.set()

        process_1.join()
        process_2.join()

if __name__ == "__main__":
    main()



