import datetime
import functools


def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('%s %s() %s:' % (text, func.__name__, datetime.datetime.now()))
            return func(*args, **kw)
        return wrapper
    return decorator


@log('execute')
def now(i):
    sum = i + 1
    return sum


if __name__ == '__main__':
    print(now(5))
    print(now.__name__)

