import tkinter as tk


window = tk.Tk()
window.title('my window')
# 窗口尺寸
window.geometry('200x200')

var1 = tk.StringVar()

l = tk.Label(window, bg='yellow', width=6, textvariable=var1)
l.pack()

var2 = tk.StringVar()
var2.set((11,22,33,44))
lb = tk.Listbox(window, listvariable=var2)
list_items = [1, 2, 3, 4]
for item in list_items:
    lb.insert('end', item)
lb.insert(1, 'first')
lb.insert(2, 'second')
lb.pack()


def print_selection():
    value = lb.get(lb.curselection())  # 获取当前选中的文本
    var1.set(value)   # 为label设置值


b = tk.Button(window, text='print selection', width=15, height=2, command=print_selection)
b.pack()

# 创建一个文本框用于显示
t = tk.Text(window, height=2)
t.pack()
# 显示出来
window.mainloop()
