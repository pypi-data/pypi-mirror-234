#!/usr/bin/env python3

import datetime, random, requests, lorem
from loguru import logger

@logger.catch
def get_random_author_name():
    names = ['Frodo Baggins', 'Aragorn', 'Gandalf', 'Legolas', 'Gimli', 'Boromir', 'Samwise Gamgee',
             'Luke Skywalker', 'Han Solo', 'Princess Leia', 'Darth Vader', 'Obi-Wan Kenobi']
    return random.choice(names)

@logger.catch
def get_random_title():
    titles = ['Jedi Night: The Force Sleeps Tight', 'How to Train Your Drogon', 'The Return of the Thing',
              'Desolation of Smaug\'s Pantry', 'Fifty Shades of Gandalf the Grey']
    return random.choice(titles)

@logger.catch
def get_random_text():
    return lorem.get_paragraph(3)

@logger.catch
def create_document(url, auth, search_space_id, i):
    
    padding = '.' * (20 - len(str(i+1)))
    payload = {
        'searchSpaceId': search_space_id,
        'author': get_random_author_name(),
        'identifier': f'{url}/{i}',
        'date': datetime.datetime.now().strftime('%Y-%m-%d'),
        'title': get_random_title(),
        'language': 'en',
        'text': get_random_text()
    }

    response = requests.post(url+"/GraphSearch/api/content/create", json=payload, auth=auth)
    logger.info(f'\rDocument #{i+1} {padding} {response.status_code}')
