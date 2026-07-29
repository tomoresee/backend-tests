import logging
import os


class LoggerConfig:
    LOGS_DIR_NAME = "logs"
    LOGGER_NAME = "Logger"
    LOGS_FILE_NAME = LOGS_DIR_NAME + os.sep + "api.log"
    LOGS_LEVEL = logging.INFO
    MAX_BYTES = 100000
    BACKUP_COUNT = 10
    FORMAT = "[%(asctime)s - %(levelname)s] - %(message)s"
    DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
