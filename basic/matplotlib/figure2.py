import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 50)
y1 = 2*x + 1
y2 = x**4

plt.figure(num=2, figsize=(10, 6))  # index + figure size
plt.plot(x, y1)
plt.plot(x, y2,
         color='red',   # 线颜色
         linewidth=2.0,  # 线宽
         linestyle='--'  # 线样式
        )

plt.xlim((-1, 2))  # x range
plt.ylim((-2, 3))  # y range
new_ticks = np.linspace(-1, 2, 5)
print(new_ticks)
plt.xticks(new_ticks)  # 设置x轴刻度：范围是(-1,2);个数是5
# y刻度为[-2, -1.8, -1, 1.22, 3]；对应刻度的名称为[‘really bad’,’bad’,’normal’,’good’, ‘really good’]
plt.yticks([-2, -1.8, -1, 1.22, 3,],
           ['really bad', 'bad', 'normal', 'good', 'really good'])
# plt.yticks([-2, -1.8, -1, 1.22, 3,],
#            [r'$really\ bad$', r'$bad\ \alpha$', r'$normal$', r'$good$', r'$really\ good$'])
plt.xlabel('I am X')
plt.ylabel('I am Y')
plt.show()
