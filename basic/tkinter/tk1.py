import tkinter as tk

# Framework of window
window = tk.Tk()
window.title('My window')
window.geometry('600x150')

# content of window
l = tk.Label(window, text='OMG, this is tk', bg='red', font=('Arial', 12), width=15, height=2)
l.pack()  # position of window
window.mainloop()
