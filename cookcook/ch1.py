#!/usr/bin/env python3
# !encoding=utf-8


def ch1_1():
    """
    1.1 将序列分解为单独的变量对象可迭代，就可以分解，包括字符串，文件，迭代器，
    生成器分解操作可以使用"_"来丢弃一些特定的值
    """
    print("\nch1_1:")
    data=['hello', 'ch1', ["*", "_"], (-6, 1, 4)]

    _, a, [_, b], (_, middle, _) = data

    print(a+b+str(middle))  # ch1_1


def ch1_2():
    """
    1.2 从任意长度的可迭代对象中分解元素
    "*表达式" 用于未知长度或者任意长度的对象分解
    分解linux shadow文件字符串
    """
    print("\nch1_2:")

    linux_shadow = "username:$1$jMzjGK//$Do9jjAM9TqHVhkH3eSytT.:14576:0:99999:7:::"
    username, passwd, *drop = linux_shadow.split(":")
    print(username, passwd, *drop)
    _, encrpty_type, encrpty_salt, encrptyed_str = passwd.split("$")

    print("type:%s\nsalt:%s\npasswd:%s\n" % (encrpty_type, encrpty_salt, encrptyed_str))


def ch1_3():
    """
    1.3 保存最后N个元素
    使用colletions.deque
    添加，弹出均为O(1)
    """
    print("\nch1_3:")

    from collections import deque

    def search(lines, pattern, history=5):
        pre_lines = deque(maxlen=history)  # 保存最后5个搜索结果
        for line in lines:
            if pattern in line:
                yield line, pre_lines
            pre_lines.append(line)

    with open('ch1_3.txt') as f:
        for line, prelines in search(f, 'Java', 5):
            print(prelines, len(prelines))
            print(line)


def ch1_4():
    """
    找到最大或者最小的N个元素
    使用heapq中的nlargest和nsmallest
    找出学生成绩的前五名
    """
    print("\nch1_4:")

    # heappush(heap,item)往堆中插入一条新的值
    # heap = [] 建立一个常见的堆
    # heappoppush() 弹出最小的值，并且将新的值插入其中
    from heapq import nlargest, heapify, heappop
    from operator import itemgetter

    # 元素数量相对较小时使用nlargest nsmallest
    dict1 = {'name1': 34, 'name2': 45, 'name3': 98, 'name4': 34, 'name5': 66, "name6": 90, "name7": 90}
    top5 = nlargest(5, dict1.items(), key=lambda x: x[1])  # 注意python3 iteritem没有了 用items替代了
    print(top5)

    # 如果元素总数很大，N很小
    heap = list(dict1.values())  # 转化为list 变成堆 pop
    heapify(heap)  # heapify()以线性时间将一个列表转为堆
    for i in range(5):  # 输出最小的5个值
        print(heappop(heap))  # 弹出最小的值

    # 如果元素数量和N差不多大，建议排序再做切片
    for name, score in sorted(dict1.items(), key=itemgetter(1), reverse=True)[:5]:
        print(name, score)


def ch1_5():
    """
    1.5 实现优先级队列
    使用heapq来pop优先级最高的元素
    """
    print("\nch1_5:")

    import heapq

    class PriorityQueue():
        def __init__(self):
            self._queue = []
            self._index = 0

        def push(self, item, priority):
            heapq.heappush(self._queue, [-priority, self._index, item])  # 从高到低排列

        def pop(self):
            return heapq.heappop(self._queue)[-1]

    q = PriorityQueue()
    q.push('1', 1)
    q.push('10', 10)
    q.push('100', 100)
    q.push('50', 50)
    q.push('double 50', 50)
    q.push('25', 25)

    for i in range(5):
        print(q.pop())


def ch1_6():
    """
    1.6 在字典中将键映射到多个值上 （一键多值字典）使用collections中的defaultdict
    """
    print("\nch1_6:")

    from collections import defaultdict

    d = defaultdict(list)
    # 一个键对应一个list
    d['a'].append(1)
    d['a'].append(2)
    d['a'].append(3)

    d['b'].append(4)

    print(d)


def ch1_7():
    """
    1.7 让字典保持有序,使用collections中的OrderedDict类
    """
    print("\nch1_7:")

    from collections import OrderedDict
    # OrderedDict 中维护了一个双向链接，来保持顺序加入的位置，大量数据会增大内存消耗

    d = OrderedDict()
    d['1'] = 1
    d['2'] = 2
    d['3'] = 3
    d['4'] = 4

    for key in d:
        print(key, d[key])


def ch1_8():
    """
    1.8 与字典有关的计算问题 如最小值，最大值，排序等
    使用zip把字典的键值反过来
    """
    print("\nch1_8:")

    scores = {'name1': 34, 'name2': 45, 'name3': 98, 'name4': 34, 'name5': 66, "name6": 90, "name7": 90}

    min_score = min(zip(scores.values(), scores.keys()))
    max_score = max(zip(scores.values(), scores.keys()))
    scores_sorted = sorted(zip(scores.values(), scores.keys()), reverse=True)

    print(min_score, max_score)
    print(scores_sorted)


def ch1_9():
    """
     1.9 在两个字典中寻找相同点 寻找相同的键，相同的值等 使用集合操作 如 & -
    """

    print("\nch1_9:")

    a = {'x': 1, 'y': 2, 'z': 3}
    b = {'w': 100, 'x': 50, 'y': 2}
    print(a.keys() & b.keys())
    print(a.keys() - b.keys())
    print(a.items() & b.items())


def ch1_10():
    """
    1.10 从序列中移除重复项且保持元素间顺序不变 利用set和生成器，返回不同的元素
    """
    print("\nch1_10:")

    def dedupe(items, key=None):
        b = set()
        for i in items:
            print(i)
            val = i if key is None else key(i)
            print(val)
            if val not in b:
                yield i  # 生成器
                b.add(val)

    a = [{'x': 1, 'y': 5}, {'x': 2, 'y': 7}, {'x': 1, 'y': 5}, {'x': 1, 'y': 100}]

    print(a, type(a))

    print(list(dedupe(a, key=lambda d: (d['x'], d['y']))))


if __name__ == '__main__':
    ch1_1()
    ch1_2()
    ch1_3()
    ch1_4()
    ch1_5()
    ch1_6()
    ch1_7()
    ch1_8()
    ch1_9()
    ch1_10()
