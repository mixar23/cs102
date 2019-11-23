import datetime
 
def today_day_is(plus):
    today = datetime.datetime.today()
    date = today.strftime("%d %m %Y %A")#Получаем строку сегодняшней даты формата день, месяц, год, день недели
    DATE = date.split(' ')#Получаем список из строки 
    DAY = DATE[0]#Сегодняшний день месяца
    weekdays = ('monday','tuesday','wednesday','thursday','friday','saturday','sunday')
    WEEK_DAY = DATE[3].lower()#Сегодняшний день недели
    WEEK_DAY = weekdays[(weekdays.index(WEEK_DAY)+plus)%7]
    MONTH = DATE[1]#Сегодняшний месяц
    d = datetime.datetime.strptime(date, "%d %m %Y %A")#Преобразуем во временной формат
    days1 = d.toordinal()#Получаем кол-во дней с начала эпохи
    date2 = date.replace(DAY,'01').replace(MONTH,'09')#date2 = 1 Сентября нынешнего года (редактируем строку date)
    if int(MONTH) < 9:
        date2 = date.replace(DATE[2],str(int(DATE[2])-1))#Проверяем год
    d2 = datetime.datetime.strptime(date2, "%d %m %Y %A")#Преобразуем во времененой формат  день, месяц, год, день недели
    stray = datetime.datetime.strftime(d2,"%d %m %Y %A")#Получаем дату 1 сентября в формате день, месяц, год, день недели
    stray = stray.split(' ')#Создаем список
    Day_week = stray[3]#И достаем из него день недели 1 сентября текущего учебного года
    days2 = d2.toordinal()#Получаем кол-во дней с начала эпохи для 1-ого сентября текущего учебного года 
    difference = days1 - days2#находим разницу между сегодняшним днем и 1-ым сентября
    days_in_week = {'Monday':'0','Tuesday':'1','Wednesday':'2','Thursday':'3','Friday':'4','Saturday':'5','Sunday':'-1'}#"Откатываем" 1-ое сентября на понедельник 
    week = ((difference+plus + int(days_in_week[Day_week]))// 7) + 1#Получаем номер недели
    return (week % 2 +1,WEEK_DAY)#Возвращаем 1, если четная, 2, если нечетная и сегодняшний день недели
