import logging.config
import os
import pathlib
from logging.handlers import RotatingFileHandler

from dotenv import dotenv_values

from codingame_backup import __app_name__


class MyRotatingFileHandler(RotatingFileHandler):
    """"""

    def namer(self, name, *args, **kwargs):
        """Change the order of suffixes when naming rotated files.

        foo.log.1 -> foo.1.log
        """
        p = pathlib.Path(name)
        true_stem, *suffixes = p.name.split('.')
        return '.'.join((true_stem, *suffixes[::-1]))


def setup_logging():
    logs_dir = pathlib.Path.cwd() / 'logs'
    LOG_CONF = {
        'version'   : 1,
        'formatters': {
            'file_form'   : {
                'format': '%(asctime)s - %(levelname)-7s - %(funcName)-10s - %(message)s'
            },
            'console_form': {
                'format': '%(levelname)-7s - %(message)s'
            },
        },
        'handlers'  : {
            'console_hand' : {
                'class'    : 'logging.StreamHandler',
                'stream'   : 'ext://sys.stdout',
                'level'    : 'DEBUG',
                'formatter': 'console_form',
            },
            'rich'         : {
                '()'             : 'rich.logging.RichHandler',
                'rich_tracebacks': True,
                'level':    'DEBUG',
            },
            'file_hand_rot': {
                'class'      : 'codingame_backup.config.MyRotatingFileHandler',
                'filename'   : logs_dir / f'{__app_name__}.log',
                'maxBytes'   : 3_145_728,  # 3MB
                'backupCount': 5,  # five files with log backup
                'level'      : 'DEBUG',
                'encoding'   : 'utf-8',
                'formatter'  : 'file_form',
            },
            'file_err_hand': {
                'class'      : 'codingame_backup.config.MyRotatingFileHandler',
                'filename'   : logs_dir / f'{__app_name__}_ERROR.log',
                'maxBytes'   : 3_145_728,  # 3MB
                'backupCount': 5,  # five files with error log backup
                'level'      : 'ERROR',
                'encoding'   : 'utf-8',
                'formatter'  : 'file_form',
            },
        },
        'loggers'   : {
            '': {
                'handlers': ['rich', 'file_hand_rot', 'file_err_hand'],
                'level'   : 'DEBUG',
            }
        }
    }
    # create logs directory
    logs_dir.mkdir(exist_ok=True)
    # setup logging
    logging.config.dictConfig(LOG_CONF)
    logging.debug('logging setup complete')


# env cofig
config = {
    **dotenv_values(".env"),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}
