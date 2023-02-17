import tkinter as tk
from tkinter import ttk as ttk
import datetime     


class AlarmClock(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.all_alarms = []
        
        self.ini_body()
        self.ini_clock()
        self.ini_mid()
        self.ini_table()

    def ini_body(self):
        self.up_frame = tk.Frame(self)
        self.mid_frame= tk.Frame(self)
        self.dow_frame= tk.Frame(self)

        self.up_frame.pack(side='top')
        self.mid_frame.pack(side='top',fill='x')
        self.dow_frame.pack(side='top')

    def ini_clock(self):
        self.clock = tk.Label(self.up_frame, text='00:00:00')
        self.clock.pack(side='top', fill='x')
        self.tick()
    def tick(self):
        self.showed_time = ''
        self.current_time = datetime.datetime.now().strftime("%H:%M:%S")
        if self.showed_time != self.current_time:
            self.showed_time = self.current_time
            self.clock.configure(text=self.current_time)
        if self.showed_time in self.all_alarms:
            self.invoke_alarm(self.showed_time)
        self.after(1000, self.tick)

    def ini_table(self):
        self.table = ttk.Treeview(self.dow_frame,height=10,columns=('#1'))
        self.table.heading('#0', text='Alarm ID')
        self.table.heading('#1', text='Будильник')

        self.table.pack()
    def ini_mid(self):
        self.alarm_id = tk.Entry(self.mid_frame,justify='center')
        self.alarm_id.insert('end','Alarm ID')

        self.alarm_time = tk.Entry(self.mid_frame,justify='center')
        self.alarm_time.insert('end','HH:MM')

        self.set_button = tk.Button(self.mid_frame, text='Установитьбудильник',
                                    command=self.set_alarm)
        self.cancel_button=tk.Button(self.mid_frame, text='Удалить будильник',
                                     command=self.cancel_alarm)

        self.alarm_time.grid(column=1,row=0,sticky='ew')
        self.alarm_id.grid(column=0,row=0, sticky='we')
        self.set_button.grid(column=0, row=1, sticky='ew')
        self.cancel_button.grid(column=1, row=1, sticky='ew')
        self.mid_frame.columnconfigure(0, weight=1)
        self.mid_frame.columnconfigure(1, weight=1)
        
    def set_alarm(self):
        Id = self.alarm_id.get()
        time = self.alarm_time.get()
        self.table.insert('','end', iid=Id, text=Id,
                          values=time, tags=time)
        self.register_alarm()
    def cancel_alarm(self):
        Id = self.alarm_id.get()
        time = self.alarm_time.get()
        if self.table.exists(Id):
            tag = self.table.item(Id, "tags")[0]
            alarm_time=tag+":00"
            self.all_alarms.remove(alarm_time)
            self.table.delete(Id)
        elif self.table.tag_has(time):
            Id = self.table.tag_has(time)[0]
            tag = self.table.item(Id, "tags")[0]
            alarm_time=tag+":00"
            self.all_alarms.remove(alarm_time)
            self.table.delete(Id)
        
    def register_alarm(self):
        self.all_alarms.append(f'{self.alarm_time.get()}:00')
    def invoke_alarm(self, time):
        self.alarm_window = tk.Toplevel()
        self.alarm_window.title('Alarm!')

        self.message = tk.Label(self.alarm_window,
                                text=f"ALARM!! It's {time[:5]} o'clock!")
        self.message.pack(fill='both')

