import logging

logging.basicConfig(
    filename='output.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(levelname)s:  %(filename)s:  %(threadName)s:  %(name)s:  %(message)s'
)

LOGGER = logging.getLogger(__name__)
