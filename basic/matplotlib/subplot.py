import matplotlib.pyplot as plt
import numpy as np

plt.figure()

# 将整个figure分成两行两列
plt.subplot(2, 2, 1)
# 第一个参数表示X的范围，第二个是y的范围
plt.plot([0, 1], [0, 1])

plt.subplot(2, 2, 2)
plt.plot([0, 1], [0, 2])

plt.subplot(2, 2, 3)
plt.plot([0, 1], [0, 3])

plt.subplot(2, 2, 4)
plt.plot([0, 1], [0, 4])

'''
plt.subplot(2, 1, 1)
plt.plot([0, 1], [0, 1])

plt.subplot(2, 3, 4)
plt.plot([0, 1], [0, 2])

plt.subplot(2, 3, 5)
plt.plot([0, 1], [0, 3])

plt.subplot(2, 3, 6)
plt.plot([0, 1], [0, 4])
'''

plt.show()
