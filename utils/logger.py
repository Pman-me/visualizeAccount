import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.FileHandler('app.log')

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)

logger.addHandler(handler)
