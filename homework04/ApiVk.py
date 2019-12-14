import vk_api
import requests
import time
import random
import datetime
import numpy as np
import pandas as pd
import requests
import textwrap
import igraph

from pandas.io.json import json_normalize
from string import Template
from tqdm import tqdm



def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    for i in range(max_retries):
        try:
            res = requests.get(url, params=params, timeout=timeout)
            return res
        except requests.exceptions.RequestException:
            if i == max_retries - 1:
                raise
            backoff_value = backoff_factor * (2 ** i)
            time.sleep(backoff_value)
    

def get_friends(user_id, fields=False):
    """ Returns a list of user IDs or detailed information about a user's friends """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    domain = "https://api.vk.com/method"
    access_token = '0b2b845d0b2b845d0b2b845d8a0b45c94600b2b0b2b845d56c9e24595c571c95014542d'
    v = '5.103'

    query = f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}"
    response = requests.get(query)
    response = response.json()
    return response


def age_predict(user_id):
    """
    >>> age_predict(???)
    ???
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    
    friends = get_friends(user_id,'bdate')
    bdates = {}
    for i in range (friends['response']['count']):
        try:
            birthday = []
            bdate =  friends['response']['items'][i]['bdate'].split('.')
            for k in range (3):
                birthday.append(bdate[k])
            bdates[i] = birthday
        except:
            pass
    all_age = 0
    count = len(bdates.keys())
    for i in bdates.keys():
        date = bdates[i]
        all_age += get_age(date)
    avg_age = all_age // count    
    return avg_age


def get_age(bdate):
    today = datetime.datetime.today()
    date = today.strftime("%d %m %Y")#Получаем строку сегодняшней даты формата день, месяц, год, день недели
    DATE_now = date.split(' ')#Получаем список из строки
    if  int(bdate[1]) > int(DATE_now[1]):
        age = int(DATE_now[2]) - int(bdate[2]) - 1
    elif int(bdate[1]) == int(DATE_now[1]):
        if int(bdate[0]) > int(DATE_now[0]):
            age = -1
        else:
            age = 0
        age += (int(DATE_now[2]) - int(bdate[2]))
    else:
        age = int(DATE_now[2]) - int(bdate[2])
    return age


def get_network(user_id, as_edgelist=True):
    """ Building a friend graph for an arbitrary list of users """
    users_ids = get_friends(user_id)['response']['items']
    edges = []
    num = len(get_friends(user_id))
    matrix = [[0] * num for i in range(num)]

    for user1 in range(num):
        friends = get_friends(users_ids[user1])['response']['items']
        for user2 in range(user1 + 1, num):
            if users_ids[user2] in friends:
                if as_edgelist:
                    edges.append((user1, user2))
                else:
                    matrix[user1][user2] = 1
                    matrix[user2][user1] = 1
        time.sleep(0.33333334)

    surnames = get_friends(user_id, 'last_name')['response']['items']
    vertices = [i['last_name'] for i in surnames]
    if not as_edgelist:
        edges = matrix

    g = igraph.Graph(vertex_attrs={"shape": "circle",
                                   "label": vertices,
                                   "size": 10},
                     edges=edges, directed=False)

    n = len(vertices)
    visual_style = {
        "vertex_label_dist": 1.6,
        "vertex_size": 20,
        "edge_color": "gray",
        "layout": g.layout_fruchterman_reingold(
            maxiter=100000,
            area=n ** 2,
            repulserad=n ** 2)
    }
    g.simplify(multiple=True, loops=True)
    clusters = g.community_multilevel()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)
    igraph.plot(g, **visual_style)




def get_wall(
    owner_id: str='',
    domain: str='',
    offset: int=0,
    count: int=10,
    filter: str='owner',
    extended: int=0,
    fields: str='',
    v: str='5.103'
) -> pd.DataFrame:
    access_token = '0b2b845d0b2b845d0b2b845d8a0b45c94600b2b0b2b845d56c9e24595c571c95014542d'
    v = '5.103'
    domain = "https://api.vk.com/method"
    query = f"{domain}/wall.get?access_token={access_token}&owner_id={owner_id}&domain={domain}&offset={offset}&count={count}&filter={filter}&extended={extended}&fields={fields}&v={v}"
    response = requests.get(query)
    response = response.json()
    """
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get 

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param v: Версия API.
    """
    # PUT YOUR CODE HERE
    return response




