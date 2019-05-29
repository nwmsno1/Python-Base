import functools
import logging


def create_logger():
    """
    Create a logging object and returns it
    :return:
    """
    logger = logging.getLogger("example_logger")
    logger.setLevel(logging.INFO)

    # create the logging file handler
    fh = logging.FileHandler("test.log")

    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    # add handler to logger object
    logger.addHandler(fh)
    return logger


def exception(function):
    """
    A decorator that wraps the passed in function and logs exception should one occur
    :param function:
    :return:
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        logger = create_logger()
        try:
            return function(*args, **kwargs)
        except:
            # log the exception
            err = "There was an exception in "
            err += function.__name__
            logger.exception(err)

            # re-raise the exception
            raise
    return wrapper


@exception
def zero_divide():
    1 / 0


if __name__ == '__main__':
    zero_divide()
