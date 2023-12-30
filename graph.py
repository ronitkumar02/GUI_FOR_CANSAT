from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# plt.style.use('seaborn-whitegrid')

x_vals = []
y_vals = []
fig=plt.figure()

index = count()

def animate(i):
    data = pd.read_csv('data.csv')
    x = data.tail(20)['x_value']
    y1 = data.tail(20)['total_1']
    # y2 = data.tail(20)['total_2']
    ax.cla()
    ax.plot(x  ,y1  ,"r"  ,label="one")
    # plt.plot(x  ,y2  ,label="two")
    ax.legend(loc="upper left")
    # y1 = data.tail(20)['total_1']
    y2 = data.tail(20)['total_2']
    ax1.cla()
    # plt.plot(x  ,y1  ,label="one")
    ax1.plot(x  ,y2  ,label="two")
    ax1.legend(loc="upper left")

ani=FuncAnimation(fig  ,animate  ,interval=1000)
ax=plt.subplot(211)
ax1=plt.subplot(212)
plt.tight_layout()
plt.show()