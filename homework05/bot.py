import requests
import config
import telebot
import datetime
import give_week
from bs4 import BeautifulSoup
from typing import List, Tuple


access_token = '1000685654:AAE-ZmA2pFLXRQlBx2LjptRcDIe5UNZjEjI'
telebot.apihelper.proxy = {'https': 'https://149.56.106.104:3128'}
bot = telebot.TeleBot(access_token)

def get_page(group: str, week: str='') -> str:
    if week:
        week = str(week) + '/'
    url = f"{config.domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm"
    response = requests.get(url)
    web_page = response.text
    return web_page\



def get_schedule(web_page: str,number) -> Tuple[List[str], List[str], List[str]]:
    soup = BeautifulSoup(web_page, "html5lib")
    DAY = {'monday':'1','tuesday':'2','wednesday':'3','thursday':'4','friday':'5','saturday':'6','sunday':'7'}

    # Получаем таблицу с расписанием на понедельник
    day_number = DAY[number]
    schedule_table = soup.find("table", attrs={"id":day_number+'day'})
    if not schedule_table:
        return ('Занятий НЕТ)))')

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info.replace('\n','').replace('\t','').replace('нечетная неделя','').replace('четная неделя','') for info in lesson_info if info]) for lesson_info in lessons_list]
    return times_list, locations_list, lessons_list

def fix_text(schedule):
    try:
        times_list, locations_list, lessons_list = schedule
    except ValueError:
        return schedule
    text = ''
    for i in range(len(times_list)):
        text += times_list[i]
        text += ', '
        text += locations_list[i]
        text += ', '
        text += lessons_list[i]
        text += ('\n')
    return(text)


@bot.message_handler(commands=['DAY'])
def get_schedule_for_a_day(message: str):
    message_text = message.text
    message_text = message_text.replace('/DAY ','')
    try:
        day, week_number, group = message_text.split()
        WEEK = 0
        if week_number == 'четная':
            WEEK = 1
        elif week_number == 'нечетная':
            WEEK = 2
        else:
            bot.send_message(message.chat.id,'Вы некорректно ввели команду, список доступных команд вы можете посмотреть написав /commands')
            return
    except ValueError:
        try:
            WEEK = 0
            day, group = message_text.split()
        except ValueError:
            bot.send_message(message.chat.id,'Вы некорректно ввели команду, список доступных команд вы можете посмотреть написав /commands')
            return
    if is_group_exceeded(group):
        message_text = fix_text(get_schedule(get_page(group,WEEK),day)) 
        bot.send_message(message.chat.id,message_text)
    else:
        bot.send_message(message.chat.id,'Вы ввели некорректный номер группы')


@bot.message_handler(commands=['all'])
def get_schedule_for_a_week(message: str):
    message_text = message.text
    message_text = message_text.replace('/all ','')
    try:
        week_number, group = message_text.split()
        if week_number == 'четная':
            WEEK = 1
        elif week_number == 'нечетная':
            WEEK = 2
        else:
            bot.send_message(message.chat.id,'Вы некорректно ввели команду, список доступных команд вы можете посмотреть написав /commands')
            return
    except ValueError:
        WEEK = 0
        group = message_text
    message_text = ''
    if is_group_exceeded:
        for day in ('monday','tuesday','wednesday','thursday','friday','saturday','sunday'):
            message_text += day + ':\n'
            message_text += fix_text(get_schedule(get_page(group,WEEK),day))
            message_text += ('\n\n')
        bot.send_message(message.chat.id,message_text)
    else:
        bot.send_message(message.chat.id,'Вы ввели некорректны номер группы')


@bot.message_handler(commands=['tomorrow'])
def get_schedule_for_tomorrow(message: str):
    message_text = message.text
    message_text = message_text.replace('/tomorrow ','')
    group = message_text
    if is_group_exceeded(group):
        times_today = list(give_week.today_day_is(0))
        if times_today[1] == 'sunday':
            times_today[1] = 'monday'
            if times_today[0] == 0:
                times_today[0] = 1
            else:
                times_today[0] = 0
        else:
            days_week = ('monday','tuesday','wednesday','thursday','friday','saturday','sunday')
            for i in range(6):
                if days_week[i] == times_today[1]:
                    times_today[1] = days_week[i+1]
        times_today[0] += 1
        WEEK,day = times_today
        message_text = fix_text(get_schedule(get_page(group,WEEK),day)) 
        bot.send_message(message.chat.id,message_text)
    else:
        bot.send_message(message.chat.id,'Вы ввели некорректный номер группы')



def is_group_exceeded(group):
    k = 0
    for i in ('monday','tuesday','wednesday','thursday','friday','saturday','sunday'):
        if get_schedule(get_page(group,0),i) == 'Занятий НЕТ)))':
            k += 1
            continue
        else:
            break
    if k == 7:
        return False
    else:
        return True

@bot.message_handler(commands=['near'])
def near(message: str):
    start = ''
    end = ''
    message_text = message.text
    message_text = message_text.replace('/near ','')
    group = message_text
    if is_group_exceeded(group):
        now = datetime.datetime.now()
        now_hour = now.hour
        now_minutes = now.minute
        times_today = give_week.today_day_is(0)
        if  get_schedule(get_page(group,times_today[0]),times_today[1]) != 'Занятий НЕТ)))':
            today_schedule_times = get_schedule(get_page(group,times_today[0]),times_today[1])[0]
        else:
            today_schedule_times = None
        if today_schedule_times:
            today_starts = []
            today_ends = []
            for i in today_schedule_times:
                a,_,y = i.partition('-')
                today_starts.append(a)
                today_ends.append(y)
            now_time = now_hour * 60 + now_minutes
            for m in range(len(today_starts)):
                i,l = today_starts[m],today_ends[m]
                minutes_start = int(i[0:1]) * 60 + int(i[3:4])
                minutes_end = int(l[0:1]) * 60 + int(l[3:4])
                if (minutes_start <= now_time) and (minutes_end > now_time):
                    start = i
                    end = l
                    now = 'Сейчас идет пара: '
                    break
                if minutes_start > now_time:
                    start = i
                    end = l
                    now = 'Следующая пара: ' 
                    break
            time_lesson_near = start+'-'+end
            if time_lesson_near != '-':
                index = today_schedule_times.index(time_lesson_near)
                schedule = get_schedule(get_page(group,times_today[0]),times_today[1])
                text = now
                for i in schedule:
                    text += schedule[index]
                bot.send_message(message.chat.id,text)
            else:
                weekend = True
                k = 1
                while weekend == True:
                    WEEK,weekday = give_week.today_day_is(k)
                    schedule = get_schedule(get_page(group,WEEK),weekday)
                    if  schedule != 'Занятий НЕТ)))':
                        now = 'Следующая пара: '
                        text = now
                        for i in range(len(schedule)):
                            text += schedule[i][0]
                            text += ' '
                        bot.send_message(message.chat.id,text)
                        weekend = False
                    else:
                        k += 1
    else:
        bot.send_message(message.chat.id,'Вы ввели некорректный номер группы')



@bot.message_handler(commands=['commands'])
def command(message: str):
    bot.send_message(message.chat.id,'Список доступных команд:\n\'/commands\'\n\'/DAY день_недели тип_недели номер_группы\'\n\'/all тип_недели номер_группы\'\n\'/tomorrow номер_группы\'\n\'/near: номер_группы\'')
    bot.send_message(message.chat.id,'если не указан тип недели показывается полное расписание')
    bot.send_message(message.chat.id,'день недели может быть следующим: monday/tuesday/wednesday/thursday/friday/saturday/sunday')


if __name__ == '__main__':
    bot.polling()