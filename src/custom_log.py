import logging

logger = None
#logger initialization is made by app.py
def init_logger(log):
    global logger
    logger = log

def custom_logger(msg,lvl=logging.INFO):
    global logger
    if logger:
        if lvl == logging.INFO:
            logger.info(msg)
        elif lvl == logging.WARNING:
            logger.warning(msg)
        elif lvl == logging.DEBUG:
            logger.debug(msg)
