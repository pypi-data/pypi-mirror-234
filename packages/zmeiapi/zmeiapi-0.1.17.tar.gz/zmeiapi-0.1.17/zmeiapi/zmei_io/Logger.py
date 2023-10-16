import logging


logger = logging.getLogger('zmei-api logger')
logger.setLevel(logging.DEBUG)

# creating console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# creating error handler
eh = logging.FileHandler(f'zmei-api.log')
eh.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
eh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(eh)
