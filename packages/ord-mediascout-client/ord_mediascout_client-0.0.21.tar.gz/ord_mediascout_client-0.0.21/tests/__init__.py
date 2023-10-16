import os

from dotenv import load_dotenv

load_dotenv()

if os.getenv('LOGGING') == 'debug':
    import logging

    logger = logging.getLogger('ord_mediascout_client')
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler = logging.FileHandler('ord_mediascout_client.log')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
