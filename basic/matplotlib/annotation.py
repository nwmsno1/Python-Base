import numpy as np
import matplotlib.pyplot as plt


x = np.linspace(-3, 3, 50)
y = x**2 + 2

plt.figure(num=1, figsize=(8, 5))
plt.plot(x, y)

plt.xlim((-3, 3))
plt.ylim((0, 9))

x_ticks = np.linspace(-3, 3, 7)
y_ticks = np.linspace(0, 9, 10)
plt.xticks(x_ticks)
plt.yticks(y_ticks)
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.spines['bottom'].set_position(('data', 0))
ax.spines['left'].set_position(('data', 0))

# 显示交叉点
x0 = 1
y0 = x0**2 + 2
# s表示点的大小，默认rcParams['lines.markersize']**2
plt.scatter(x0, y0, s=50, color='b')
# 定义线的范围，X的范围是定值，y的范围是从y0到0的位置
# lw的意思是linewidth,线宽
plt.plot([x0, x0], [y0, 0], 'k--', lw=3)

# method1
############################################
# 设置关键位置的提示信息
# xytext=(+30, -30) 在点的上下30显示
plt.annotate(r'$x**2+2=%s$' % y0, xy=(x0, y0), xycoords='data', xytext=(+30, -30), textcoords='offset points', fontsize=16,
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3, rad=.2'))

# method2
############################################
# 在figure中显示文字信息
# 可以使用\来输出特殊的字符\mu\ \sigma\ \alpha
plt.text(-3.7, 3, r'$This\ is\ the\ some\ text.\ \mu\ \sigma_i\ \alpha_t$', fontdict={'size': 16, 'color': 'r'})


plt.show()
