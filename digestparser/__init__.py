import logging

__version__ = '0.1.1'

LOGGER = logging.getLogger('digest_parser')
HDLR = logging.FileHandler('digest_parser.log')
FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
HDLR.setFormatter(FORMATTER)
LOGGER.addHandler(HDLR)
LOGGER.setLevel(logging.INFO)
