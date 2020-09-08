import logging
import logging.handlers
import os

log_level = logging.DEBUG
log_filename = "multi_process_log.log"

def logger_configurer():
    global log_level
    global log_filename

    _pwd = ""
    _log_dir = "log"

    root = logging.getLogger()

    root.setLevel(log_level)

    f_out = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] %(message)s')
    f_file = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(processName)s] [%(threadName)s] %(message)s')


    # check log directory
    if not os.path.exists(_log_dir):
        os.makedirs(_log_dir)
    
    log_filename = _pwd + _log_dir + os.sep + log_filename

    out_h = logging.StreamHandler()
    out_h.setFormatter(f_out)

    one_MB = 2 ** 20
    file_h = logging.handlers.RotatingFileHandler(log_filename, maxBytes=one_MB, backupCount=5)
    file_h.setFormatter(f_file)
    
    root.addHandler(file_h)
    root.addHandler(out_h)

def root_configurer(queue):
    global log_level

    h = logging.handlers.QueueHandler(queue)
    root = logging.getLogger()
    root.addHandler(h)
    root.setLevel(log_level)
