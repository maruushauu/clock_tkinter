Стэк проекта clock_tkinter:
  - python
  - tkinter
>> Проект реализует коробочное решение, в котором есть часы, будильник, календарь.
>> Построен на принципах ООП, имеет оди запускающий файл для удобства и два независимых модуля, каждый из которых отвечает за свою функцию.
>> Главный файл main.py из которого запускается проект, имеет два экземпляра класса tkinter для каждого из frameworks (окон). Происходит инициализация,задаются параметры

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
  
 >> clock.py - для реализации часов + будильника. В который мы передаем ранее созданный в main.py образец класса.
    В основе данного метода реализации я использовала класс self - для передачи аргументов между функциями в одной сессии и также all_alarms - список,в который мы 
      дабавляем или удаляем введеное время
  Функция ini_body - инициализирует Frame 
  Функция ini_clock, tick - задаем параметры времени
  Функция ini_table, ini_mid - задаем параметры таблицы для окон Будильника
  Функция set_alarm, cancel_alarm - отвечают за создание, удаление значения будильника
  Функция register_alarm, invoke_alarm - запускаются чтобыотобразить, что будильник сработал
  
  
  
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


  >> data_day.py -реализован динамеческий календарь,в основе которого мы задаем глобальные переменные для дня, месяца,года, далее проходимся циклом по текущему 
      месяцу и прибавляем дни. В отличие от ранее описанного модуля, здесь мы передаем экземпляр класса tkinter обратно в главный файл main.py - это сделано 
      специально, чтобы иметь возможность задать глобальные переменные и для удобства обращения к ним и функция tkinter.
      
    from tkinter import *
    import calendar
    import datetime
    root = Tk()
    root.title('Calendar')
    days = []
    now = datetime.datetime.now()
    year = now.year
    month = now.month

    def prew():
        global month, year
        month -= 1
        if month == 0:
            month = 12
            year -= 1
        fill()

    def next():
        global month, year
        month += 1
        if month == 13:
            month = 1
            year += 1
        fill()

    def fill():
        info_label['text'] = calendar.month_name[month] + ', ' + str(year)
        month_days = calendar.monthrange(year, month)[1]
        if month == 1:
            prew_month_days = calendar.monthrange(year-1, 12)[1]
        else:
            prew_month_days = calendar.monthrange(year, month - 1)[1]
        week_day = calendar.monthrange(year, month)[0]
        for n in range(month_days):
            days[n + week_day]['text'] = n+1
            days[n + week_day]['fg'] = 'black'
            if year == now.year and month == now.month and n == now.day:
                days[n + week_day]['background'] = 'green'
            else:
                days[n + week_day]['background'] = 'lightgray'
        for n in range(week_day):
            days[week_day - n - 1]['text'] = prew_month_days - n
            days[week_day - n - 1]['fg'] = 'gray'
            days[week_day - n - 1]['background'] = '#f3f3f3'
        for n in range(6*7 - month_days - week_day):
            days[week_day + month_days + n]['text'] = n+1
            days[week_day + month_days + n]['fg'] = 'gray'
            days[week_day + month_days + n]['background'] = '#f3f3f3'

    prew_button = Button(root, text='<', command=prew)
    prew_button.grid(row=0, column=0, sticky='nsew')
    next_button = Button(root, text='>', command=next)
    next_button.grid(row=0, column=6, sticky='nsew')
    info_label = Label(root, text='0', width=1, height=1, 
                font=('Verdana', 16, 'bold'), fg='blue')
    info_label.grid(row=0, column=1, columnspan=5, sticky='nsew')
    for n in range(7):
        lbl = Label(root, text=calendar.day_abbr[n], width=1, height=1, 
                    font=('Verdana', 10, 'normal'), fg='darkblue')
        lbl.grid(row=1, column=n, sticky='nsew')
    for row in range(6):
        for col in range(7):
            lbl = Label(root, text='0', width=4, height=2, 
                        font=('Verdana', 16, 'bold'))
            lbl.grid(row=row+2, column=col, sticky='nsew')
            days.append(lbl)
    fill()
