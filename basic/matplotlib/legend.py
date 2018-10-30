import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 50)
y1 = 2*x + 1
y2 = x**2

plt.figure(num=2, figsize=(10, 6))  # index + figure size

plt.xlim((-1, 2))  # x range
plt.ylim((-2, 3))  # y range
new_ticks = np.linspace(-1, 2, 5)
print(new_ticks)
plt.xticks(new_ticks)  # 设置x轴刻度：范围是(-1,2);个数是5
# y刻度为[-2, -1.8, -1, 1.22, 3]；对应刻度的名称为[‘really bad’,’bad’,’normal’,’good’, ‘really good’]
# plt.yticks([-2, -1.8, -1, 1.22, 3,],
#            ['really bad', 'bad', 'normal', 'good', 'really good'])
plt.yticks([-2, -1.8, -1, 1.22, 3,],
           [r'$really\ bad$', r'$bad\ \alpha$', r'$normal$', r'$good$', r'$really\ good$'])

l1, = plt.plot(x, y1, label='up')  # 若要传进legned，需要在l1后加个逗号
l2, = plt.plot(x, y2, color='red', linewidth=2.0, linestyle='--', label='down')
# 使用legend绘制多条曲线
plt.legend(handles=[l1, l2,], labels=['aaa', 'bbb'], loc='best')  # loc='upper right'

plt.xlabel('I am X')
plt.ylabel('I am Y')
plt.show()
