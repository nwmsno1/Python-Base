import time


def job(t):
    print('Start job ', t)
    time.sleep(t)  # wait for "t" seconds
    print('Job ', t, ' takes ', t, ' s')


def main():
    [job(t) for t in range(1, 3)]


if __name__ == '__main__':
    t1 = time.time()
    main()
    print("NO async total time : ", time.time() - t1)
