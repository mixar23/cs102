import requests
import config
import telebot
import time
import give_week
from bs4 import BeautifulSoup
from typing import List, Tuple

'''
</table><h4 class="rasp_day_mobile">Понедельник</h4>
  <div class="rasp_tabl_day">
      <table id="1day" class="rasp_tabl" border="0" cellpadding="0" cellspacing="0">
          <tbody>
              <tr>
                  <th class="day">
                      <script>$("#1day_btn").show();</script>
                      <span>Пн</span>
                  </th>
                  <td class="time">
                      <span>08:20-09:50</span>
                      <dt style="font-size:14px;"></dt>
                      <dd class="rasp_aud_mobile"></dd>
                      <dt class="rasp_corp_mobile">
                          <i class="fa fa-map-marker"></i>
                          <span>ул.Ломоносова, д.9, лит. Е</span>
                      </dt>
                  </td>
'''

access_token = access_token
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
    for i in range(10):
        try:
            text += times_list[i]
            text += ', '
            text += locations_list[i]
            text += ', '
            text += lessons_list[i]
            text += ('\n')
        except IndexError:
            continue
    return(text)


@bot.message_handler(commands=['DAY'])
def get_schedule_for_a_day(message: str):
    message_text = message.text
    message_text = message_text.replace('/DAY ','')
    try:
        day, week_number, group = message_text.split()
        if week_number == 'четная':
            WEEK = 1
        elif week_number == 'нечетная':
            WEEK = 2
    except ValueError:
        WEEK = 0
        day, group = message_text.split()
    message_text = fix_text(get_schedule(get_page(group,WEEK),day)) 
    bot.send_message(message.chat.id,message_text)


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
    except ValueError:
        WEEK = 0
        group = message_text
    message_text = ''
    for day in ('monday','tuesday','wednesday','thursday','friday','saturday','sunday'):
        message_text += day + ':\n'
        message_text += fix_text(get_schedule(get_page(group,WEEK),day))
        message_text += ('\n\n')
    bot.send_message(message.chat.id,message_text)


@bot.message_handler(commands=['tomorrow'])
def get_schedule_for_tomorrow(message: str):
    message_text = message.text
    message_text = message_text.replace('/tomorrow ','')
    WEEK,day = give_week.tomorrow_day_is()
    WEEK += 1
    group = message_text.split()
    message_text = fix_text(get_schedule(get_page(group,WEEK),day)) 
    bot.send_message(message.chat.id,message_text)

if __name__ == '__main__':
    bot.polling()
