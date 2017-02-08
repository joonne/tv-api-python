#!/usr/bin/env python
'''scraper.py'''

from bs4 import BeautifulSoup
import grequests
import arrow

TODAY = arrow.now('Europe/Helsinki').format('dddd', 'fi_fi')
CHANNELS = ['yle1', 'yle2', 'mtv3', 'nelonen', 'subtv']
BASE_PATH = 'http://www.telsu.fi'

def process_channel(content):
    '''processes channel information'''

    soup = BeautifulSoup(content, 'html.parser')

    summaries = [x.get_text() for x in soup.find_all('var', class_='atc_title')]
    descriptions = [x.get_text() for x in soup.find_all('div', class_='t')]
    starts = [x.get_text() for x in soup.find_all('var', class_='atc_date_start')]
    ends = [x.get_text() for x in soup.find_all('var', class_='atc_date_end')]

    programs = []

    for i in range(len(summaries)):
        programs.append({
            'name': summaries[i],
            'description': descriptions[i],
            'start': starts[i],
            'end': ends[i]
        })

    print ('processed {} programs'.format(len(programs)))

    return {
        'programs': programs
    }

# creates a set of unsent requests
REQUESTS = (grequests.get(BASE_PATH + '/' + TODAY + '/' + channel) for channel in CHANNELS)
# send them all at the same time and map the responses to processChannel function
ALL_PROGRAMS = [process_channel(response.text) for response in grequests.map(REQUESTS)]
