"""
Copyright (c) 2021 Plugin Andrey (9keepa@gmail.com)
Licensed under the MIT License
"""
import logging, os

def log(name, filename=None):

    logger = logging.getLogger(name)
    logger.setLevel( logging.DEBUG )

    if filename:
        ch = logging.FileHandler(os.path.join(  os.getcwd(), filename ))
    else:
        ch = logging.StreamHandler()

    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s : %(lineno)d : %(name)s : %(levelname)s : %(message)s')
    ch.setFormatter(formatter)

    # добавляем ch к logger
    logger.addHandler(ch)

    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warn('warn message')
    # logger.error('error message')
    # logger.critical('critical message')
    return logger