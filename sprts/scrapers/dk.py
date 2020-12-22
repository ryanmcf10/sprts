import datetime

import requests
from bs4 import BeautifulSoup

nba_homepage = "https://sportsbook.draftkings.com/leagues/basketball/103"

def main():
    soup = get_homepage()
    date_cards = get_date_cards(soup)
    events = get_events(date_cards)

def get_homepage():
    page = requests.get(nba_homepage)

    return BeautifulSoup(page.content, features='html.parser')


def get_date_cards(soup):
    return soup.findAll('div', class_='parlay-card-10-a')

    return result

def get_events(date_cards):
    result = {
        'today': extract_event_ids(date_cards[0]),
        'tomorrow': extract_event_ids(date_cards[1])
    }

    return result

    
def extract_event_ids(date_card):
    result = set()

    for link in date_card.findAll('a', class_='event-cell-link'):
        href = link['href']
        event_id = href.split('/')[-1].strip()
        result.add(event_id)

    return result

if __name__ == '__main__':
    main()