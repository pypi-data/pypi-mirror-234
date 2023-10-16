import logging
import os
from swmonkey.util.util import get_out_dir


def monkey_logger(log_file, log_level=logging.INFO):
    logger = logging.getLogger('monkey')
    logger.setLevel(log_level)
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s = %(filename)s %(lineno)d - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger


# TODO: 参数化
out_dir = get_out_dir()
log_file = os.path.join(out_dir, 'monkey.log')
# if log_file does not exist, create it
if not os.path.exists(log_file):
    open(log_file, 'w').close()
assert os.path.exists(log_file)
logger = monkey_logger(log_file)
