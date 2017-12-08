#!/usr/bin/env python
'''xmltv.py'''

import grequests
import arrow

TODAY = arrow.now('Europe/Helsinki').format('YYYY-MM-DD', 'fi_fi')
CHANNELS = ['mtv3.fi', 'nelonen.fi']
BASE_URL = 'https://json.xmltv.se'

def process_channel(content):
    '''processes channel information'''

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

def update_schedule():
    # creates a set of unsent requests
    REQUESTS = (grequests.get(BASE_PATH + '/' + channel + '_' + TODAY + '.js.gz') for channel in CHANNELS)
    # send them all at the same time and map the responses to processChannel function
    ALL_PROGRAMS = [process_channel(response.text) for response in grequests.map(REQUESTS)]