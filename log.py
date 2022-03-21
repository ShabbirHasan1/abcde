"""
Create a logging interface here.
"""

import logging

logging.basicConfig(
    filename='/Users/hardcorecoder/Documents/Python/Projects/SingleClientAutomation Dummy/single-option/logs/AutomatedStraddle_logger.log',
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO,
    datefmt='%m/%d/%Y %I:%M:%S %p'
)


def get_logger():
    """
    Get logger.

    :param name:
    :return:
    """
    return logging.getLogger()


if __name__ == "__main__":

    logger = get_logger()

    logger.info("Hello")