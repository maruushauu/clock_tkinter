import tkinter as tk
from clock import *
from data_day import *

winwod1 = tk.Tk()
alarm = AlarmClock(winwod1)
alarm.pack()
winwod1.geometry('400x400')
winwod1.title('One')

data_d = fill()
root.geometry('400x400+500+0')
root.title('Two')

label_one = tk.Label(winwod1, text='Win number: 1')
label_one.pack()


winwod1.mainloop()
