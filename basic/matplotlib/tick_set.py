import numpy as np
import matplotlib.pyplot as plt


x = np.linspace(-3, 3, 50)
y = 0.1*x

plt.figure(num=1, figsize=(8, 5))
# alpha是设置透明度的
plt.plot(x, y, linewidth=10, zorder=1, alpha=0.5)

# plt.xlim((-30, 30))
plt.ylim((-3, 3))

# x_ticks = np.linspace(-30, 30, 7)
# y_ticks = np.linspace(-3, 3, 10)
# plt.xticks(x_ticks)
# plt.yticks(y_ticks)
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.spines['bottom'].set_position(('data', 0))
ax.spines['left'].set_position(('data', 0))

# 可以使用tick设置透明度
# label.set_fontsize(12)重新调节字体大小,bbox设置目的内容的透明度相关参,facecolor调节box前景色,edgecolor设置边框,
# 本处设置边框为无,alpha设置透明度.
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(12)
    # 在 plt 2.0.2 或更高的版本中, 设置 zorder 给 plot 在 z 轴方向排序
    label.set_bbox(dict(facecolor='white', edgecolor='None', alpha=0.7, zorder=2))

plt.show()
