#!/usr/bin/env python

import grequests
from bs4 import BeautifulSoup

channels = ["yle1", "yle2", "mtv3", "nelonen", "subtv"]

def processChannel(content):
    soup = BeautifulSoup(content, 'html.parser')

    summaries = map(lambda x: x.get_text(), soup.find_all("span", class_="_summary"))
    descriptions = map(lambda x: x.get_text(), soup.find_all("div", class_="t"))
    starts = map(lambda x: x.get_text(), soup.find_all("span", class_="_start"))
    ends = map(lambda x: x.get_text(), soup.find_all("span", class_="_end"))

    programs = []

    for i in range(len(summaries)):
        program = {
            "name": summaries[i],
            "description": descriptions[i],
            "start": starts[i],
            "end": ends[i]
        }
        programs.append(program)

    print("processed {} programs".format(len(programs)))

    return {
        "programs": programs
    }

# creates a set of unsent requests
requests = (grequests.get("http://www.telsu.fi/sunnuntai/" + channel) for channel in channels)
# send them all at the same time and map the responses to processChannel function
all_programs = map(lambda response: processChannel(response.text), grequests.map(requests))
