import requests
import csv
from bs4 import BeautifulSoup
from data import graph

BASE_URL = 'https://escapefromtarkov.fandom.com'
QUESTS_URL = 'https://escapefromtarkov.fandom.com/wiki/Quests'
PREV_QUEST = 'Previous'
NEXT_QUEST = 'Leads to'

def get_next_quests(soup, direction = True):
    va_infobox_content_items = soup.find_all('td', class_='va-infobox-content')
    result = []
    text_tag = NEXT_QUEST if direction else PREV_QUEST
    for item in va_infobox_content_items:
        if text_tag not in item.text: continue
        refs = item.find_all('a', href=True)
        if refs:
            for ref in refs:
                result.append((ref.text, f'{BASE_URL}{ref["href"]}'))
    return result

def search_first_quest(soup):
    traders_tables = soup.find_all('table', class_='questtable') # This gets all the tables as bs4.element.Tag each
    result = []
    for table in traders_tables:
        trader_name = table.find('tr').find('th').find('a').text
        first_quest_link = table.find_all('tr')[2].find('th').find('a', href=True)["href"]
        first_quest_name = table.find_all('tr')[2].find('th').find('a').text
        result.append((trader_name, first_quest_link, first_quest_name))
    return result

def main():
    # Send a GET request to the URL
    response = requests.get(QUESTS_URL)
    print(response.status_code)
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    topo_graph = graph.Graph(is_directed=True)

    # TO-DO: Create a function to do a DFS algorithm to get all the quests and their dependencies
    first_quests = search_first_quest(soup)
    for quest in first_quests:
        first_quest_trader = quest[0]
        first_quest_link = f'{BASE_URL}{quest[1]}'
        quest_node = graph.Node(quest[2], first_quest_link)
        topo_graph.add_vertex(quest_node)
        print(f'First quest for {first_quest_trader}: {first_quest_link}')
        response = requests.get(first_quest_link)
        soup = BeautifulSoup(response.content, 'html.parser')
        print(get_next_quests(soup))






if __name__ == '__main__':
    main()

