import multiprocessing as mp
import time

# value = mp.Value('d', 1)
# array = mp.Array('i', [1, 2, 3])


def job(v, num):
    for _ in range(10):
        time.sleep(0.1)
        v.value += num
        print(v.value)


def multicore():
    v = mp.Value('i', 0)
    p1 = mp.Process(target=job, args=(v, 1))
    p2 = mp.Process(target=job, args=(v, 3))
    p1.start()
    p2.start()
    p1.join()
    p2.join()


if __name__ == '__main__':
    multicore()
