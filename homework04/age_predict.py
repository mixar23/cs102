import datetime as dt
from statistics import median
from typing import Optional
import config
from api import get_friends

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
