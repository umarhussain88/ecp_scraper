import logging
from pandas import Timestamp
from pathlib import Path 



file_dt = Timestamp('now').strftime('%Y_%m_%d-%H%M%S')

log_path = Path(__file__).parent\
                         .parent.parent.joinpath('logs', f'{file_dt}_export.log')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler(log_path)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
