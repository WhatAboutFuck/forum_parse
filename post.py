
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from config import get_page,another_page

import config 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import db
import pymongo
import pprint
import re
import new

#Берем все сообщения с страницы форума в один большой список
def get_message_from_page():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)


    driver.get(get_page()[0])

    group = driver.find_elements_by_class_name("messageContent")#messageContent
    # ht = driver.
    first_take = []
    if int(get_page()[1])>1:
        for i in range(len(group)):
            first_take.append(group[i].text)
    else:
        for i in range(1,len(group)):
            first_take.append(group[i].text)

    driver.close()

    return first_take
#Разбиваем список на подсписки
def lst_of_lst():
    lst = get_message_from_page()
    new_list = []
    for i in range(len(lst)):
        new_list.append(lst[i].strip().rstrip().split('\n'))
    
    return new_list


def get_right_lst():
    l = lst_of_lst()
    right_lst = []

    for i in range(len(l)):
        for j in l[i]:
            
            if j.upper().find("ESSID")!=-1:
                    right_lst.append(l[i])

    
    
    return list(filter(None, right_lst))


def get_essid_mac_http():
    right = get_right_lst()
    mac_re = r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})'
    http_re = r'(https?://[^\"\s]+)'
    to_db = []
    for s in right:
        current = []
        for j in s:
            a = re.compile(mac_re,re.IGNORECASE).search(j)
            b = re.compile(http_re,re.IGNORECASE).search(j)
            s = j.upper()
            if "ESSID-" in s:
                current.append(j.upper().split('ESSID-')[1].strip())
            elif "ESSID -" in s:
                current.append(j.upper().split('ESSID -')[1].strip())
            elif "ESSID=" in s:
                current.append(j.upper().split('ESSID=')[1].strip())
            elif "ESSID =" in s:
                current.append(j.upper().split('ESSID =')[1].strip())
            elif "ESSID:" in s:
                current.append(j.upper().split('ESSID:')[1].strip())
            elif "ESSID :" in s:
                current.append(j.upper().split('ESSID :')[1].strip())
            elif 'ESSID' in s:       
                current.append(j.upper().split('ESSID')[1].strip())
            if a:
                current.append(j[a.start(): a.end()])
            elif b:
                current.append(j[b.start(): b.end()])
        to_db.append(current)
    l = [i for i in to_db if len(i) is 2]
    lst = [i for i in to_db if len(i) is 3]
    
    sort_2 = []
    sort_3 = []
    for j in l:
        len_2 = []
        for q in j:
            a = re.compile(mac_re,re.IGNORECASE).search(q)
            b = re.compile(http_re,re.IGNORECASE).search(q)
            if a:
                len_2.insert(0,q[a.start(): a.end()])
            elif not b:
                len_2.append(q)
        sort_2.append(len_2)
    for s in lst:
        len_3 = []
        count_mac = 0
        count_http = 0
        for z in s:    
            a = re.compile(mac_re,re.IGNORECASE).search(z)
            b = re.compile(http_re,re.IGNORECASE).search(z)
            if a:
                len_3.insert(0,z[a.start(): a.end()])
            elif b and count_mac < 1:
                count_mac+=1
                len_3.insert(1,z[b.start(): b.end()])
            elif not a and not b and count_http < 1:
                count_http+=1
                len_3.append(z)
        sort_3.append(len_3)
    return [[i for i in sort_2 if len(i) is 2],[i for i in sort_3 if len(i) is 3]]


def DB():
    basic =get_essid_mac_http()
    l = basic[0]
    lst = basic[1]
    new.write_to_db(l,lst)
    return main()

def main():
    if int(get_page()[1]) < 500:
        another_page() 
        return DB()
    else:
        return f'Current page: {int(get_page()[1])}'

# print(len(get_essid_mac_http()[0][0]),len(get_essid_mac_http()[1][0]))
DB()