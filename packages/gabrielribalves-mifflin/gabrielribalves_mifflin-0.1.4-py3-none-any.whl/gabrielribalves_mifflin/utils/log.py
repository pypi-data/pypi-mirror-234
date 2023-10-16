import logging
import os
from logging import handlers

LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING").upper()
log = logging.Logger("dundie")
fmt = logging.Formatter(
    "%(asctime)s %(name)s %(levelname)s "
    "l:%(lineno)d f:%(filename)s %(message)s"
)


def getLogger(logFile="dundie.log"):
    """Returns a configured logger"""

    fh = handlers.RotatingFileHandler(
        logFile, maxBytes=10**6, backupCount=10
    )
    fh.setLevel(LOG_LEVEL)
    fh.setFormatter(fmt)
    log.addHandler(fh)
    return log
