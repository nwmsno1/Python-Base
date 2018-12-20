import tkinter as tk


window = tk.Tk()
window.title('my window')
# 窗口尺寸
window.geometry('200x200')

var = tk.StringVar()
# 创建输入框entry，用户输入任何内容都显示为*
e = tk.Entry(window, show='*')
e.pack()


def insert_point():
    var = e.get()
    t.insert('insert', var)


def insert_end():
    var = e.get()
    t.insert('end', var)
    # t.insert(1.1, var)


b1 = tk.Button(window, text='insert point', width=15, height=2, command=insert_point)
b1.pack()
b2 = tk.Button(window, text='insert end', width=15, height=2, command=insert_end)
b2.pack()
# 创建一个文本框用于显示
t = tk.Text(window, height=2)
t.pack()
# 显示出来
window.mainloop()
