from loguru import logger as log
LOGS_PATH = './logs/'

log.add(
    LOGS_PATH + "workers.log",
    format='{time} | {level} | {message}',
    rotation="10 MB",
    compression="zip",
    encoding='utf-8',
)