import logging
import os

# Get the logging level from an environment variable
log_level = os.environ.get('LOG_LEVEL', logging.INFO)

log_file = os.environ.get('LOG_FILE_PATH', "./commutauto.log")
log_format = os.environ.get('LOG_FORMAT', "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

f_handler = logging.FileHandler(log_file)
c_handler = logging.StreamHandler()

logging.basicConfig(
    level=log_level, 
    format=log_format,
    handlers=[f_handler, c_handler])
