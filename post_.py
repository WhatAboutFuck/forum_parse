import re
from typing import List, Tuple
import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent as ua
import new

def get_message_from_page(url: str) -> list:
    """
    Return list of list all message from current page
    """
    all_taken_message_from_page = []
    try:
        response = requests.get(
            url,
            headers={
                'accept': '*/*',
                'user-agent': ua().firefox})
        soup = bs(response.content, 'html.parser')
        # Find all message on the page
        list_of_messages = soup.find_all("div", {"class": "messageContent"})
        remove_all_trash = lambda x: x.lower().startswith("essid") or x.lower().startswith("bssid") or x.lower().startswith("http")

        for message in list_of_messages:
            all_taken_message_from_page.append(
                list(filter(remove_all_trash, message.text.splitlines())))

        return [i for i in all_taken_message_from_page if 1 < len(i) < 4]
    except Exception as error:
        print('Ошибка:', error, sep='\n')

def remove_all_trash_from_list(message_to_compare: List[list]) -> Tuple[List[dict]]:
    """
    Prepares data to database 
    """
    prepare_to_db = []
    for message in message_to_compare:
        temporary_dict = {}
        essid_re = r'(\bessid[\"\s:=-]+)'
        mac_re = r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})'
        href_re = r'(https?://[^\"\s]+)'
        for element in message:
            mac = re.compile(mac_re, re.IGNORECASE).search(element)
            href = re.compile(href_re, re.IGNORECASE).search(element)
            essid = re.compile(essid_re, re.IGNORECASE).search(element)
            if mac:
                temporary_dict['mac'] = mac.group(0)
            elif href:
                temporary_dict['href'] = href.group(0)
            elif essid:
                temporary_dict['essid'] = element.split(
                    element[essid.start(): essid.end()])[1]
        prepare_to_db.append(temporary_dict)

    length_2, length_3 = [], []
    for data in prepare_to_db:
        if len(data) == 2:
            length_2.append(data)
        elif len(data) == 3:
            length_3.append(data)

    return length_2, length_3

def main():
    url = new.get_page()
    current_page = url[-1]
    first_step = get_message_from_page(url)
    second_step = remove_all_trash_from_list(first_step)
    new.write_to_db(second_step[0], second_step[1], current_page)