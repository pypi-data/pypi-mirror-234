#  Copyright (c) 2023 Roboto Technologies, Inc.

import logging

LOGGER_NAME = "roboto"


def default_logger():
    return logging.getLogger(LOGGER_NAME)
