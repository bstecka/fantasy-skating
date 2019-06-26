import re
from bs4 import BeautifulSoup
import requests


def handle_name(name_string):
    matches = re.findall(r"([A-Z']+[^a-z0-9])", name_string)
    last_name = ''.join(matches).strip()
    first_name = name_string.replace(last_name, '').strip()
    last_name = last_name.upper()
    first_name = first_name.title()
    return first_name, last_name


def split_skaters(name_string):
    split = name_string.split('/')
    return split[0], split[1]


def get_world_standings(url):
    world_standings = {}
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find('table', attrs={'class': 'results'})
    skaters = table.find_all('tr', attrs={'class': 'content'})
    for skater in skaters:
        rank = skater.find('td', attrs={'class': 'rank'})
        name = skater.find('td', attrs={'class': 'name'})
        if rank is not None and name is not None:
            name_str = name.find('a').text.__str__()
            world_standings[name_str] = rank.text.__str__()
    return world_standings