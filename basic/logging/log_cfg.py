import logging
import logging.config


def getLogging():
    return logging.getLogger('test.subtest')


if __name__ == '__main__':
    logging.config.fileConfig("log.cfg")
    logger = getLogging()
    logging.info('This is an example!')
