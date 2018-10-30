import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 50)
y1 = 2*x + 1
y2 = x**4

plt.figure(num=1, figsize=(8, 5))  # index + figure size
plt.plot(x, y1)

plt.figure(num=2, figsize=(10, 6))  # index + figure size
plt.plot(x, y1)
plt.plot(x, y2,
         color='red',   # 线颜色
         linewidth=10.0,  # 线宽
         linestyle='--'  # 线样式
        )
plt.show()
