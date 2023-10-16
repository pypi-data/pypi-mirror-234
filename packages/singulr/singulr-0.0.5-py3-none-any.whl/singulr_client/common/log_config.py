# Created by msinghal at 12/09/23
import logging
import logging.config
import colorlog

# Default log path and log format constants
DEFAULT_LOG_PATH = "/tmp"
LOG_FORMAT = '%(asctime)s.%(msecs)03dZ %(levelname)s %(filename)s:%(lineno)d %(message)s'
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'

# Create a color formatter
COLOR_LOG_FORMAT = colorlog.ColoredFormatter(
    LOG_FORMAT,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
    secondary_log_colors={},
    style="%",
)

# Configuration for logging to a file
log_file_config = {
    'version': 1,
    'formatters': {
        'genai_log_formatter': {
            'class': 'logging.Formatter',
            'datefmt': DATE_FORMAT,
            'format': LOG_FORMAT
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
        },
        'info_file_handler': {
            'class': 'logging.FileHandler',
            'filename': '',
            'mode': 'a',
            'formatter': 'genai_log_formatter'
        }
    },
    'loggers': {
        'singulr_gen_ai': {
            'handlers': ['info_file_handler']
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': []
    },
}

# Configuration for logging to the console
stream_config = {
    'version': 1,
    'formatters': {
        'genai_log_formatter': {
            'class': 'logging.Formatter',
            'datefmt': DATE_FORMAT,
            'format': LOG_FORMAT
        }
    },
    'handlers': {
        'info_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'genai_log_formatter'
        }
    },
    'loggers': {
        'app_gen_ai': {
            'handlers': ['info_handler']
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': []
    },
}


# Function to configure the logger
def configure_logger(folder_path: str, is_console_logging: bool, is_debug_enabled: bool) -> None:
    """
    Args:
        folder_path:
        is_console_logging:
        is_debug_enabled:

    Returns:
    """
    if not is_console_logging:
        log_info_file = folder_path + "/latest.log"
        log_file_config['handlers']['info_file_handler']['filename'] = log_info_file
        logging.config.dictConfig(log_file_config)
    else:
        logging.config.dictConfig(stream_config)
    logging.captureWarnings(True)
    if is_debug_enabled:
        logging.root.setLevel(logging.DEBUG)


# Logger for 'singulr-sdk' module
singulr_sdk = logging.getLogger("singulr-sdk")
