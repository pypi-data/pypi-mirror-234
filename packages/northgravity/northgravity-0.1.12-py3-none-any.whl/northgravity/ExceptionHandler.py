import base64
from . import *
import os
import logging

log = logging.getLogger(LOGGER_NAME)


class PythonStepWarnException(Exception):
    def __init__(self, message="PythonStepWarnException was raised, exiting pipeline"):
        self.message = message
        log.warn(super().__init__(message))
    pass
