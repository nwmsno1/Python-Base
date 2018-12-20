import tkinter as tk

on_hit = False


def hit_me():
    global on_hit
    if on_hit is False:
        on_hit = True
        var.set('you hit me')
    else:
        on_hit = False
        var.set('')


window = tk.Tk()
window.title('my window')
window.geometry('300x150')
var = tk.StringVar()  # store text variable
l = tk.Label(window, textvariable=var, bg='green', font=('Arial', 12), width=15, height=2)
l.pack()

b = tk.Button(window, text='hit me', width=15, height=2, command=hit_me)
b.pack()

window.mainloop()
