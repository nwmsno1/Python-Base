
def trace_func(func):
    def temp(*args, **kwargs):
        print('Start %s(%s, %s)...' % (func.__name__, args, kwargs))
        return func(*args, **kwargs)
    return temp


@trace_func
def log_test_with_empty_parameter():
    pass


@trace_func
def log_test_with_many_parameter(a_int, b_string, c_list, d_dict):
    pass


@trace_func
def log_test_with_key_parameter(a = 'www', b = 1, c = [2, 3]):
    pass


if __name__ == '__main__':
    log_test_with_empty_parameter()
    log_test_with_many_parameter(1, 'gaodi', [1, 2, 'w'], {1: 'a', 2: 'bb'})
    log_test_with_key_parameter(1, 'wew', [2, 34])
