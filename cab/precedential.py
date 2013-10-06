#!/usr/bin/env python

# CAB Precedential Opinion Scraper

from pyquery import PyQuery as pq
import json
import os

# Initialize the JSON file
data = []

# Going to have to go through the site to pull down all of the results in 15 document increments.

i = 0
base_url = 'http://app.cab.dc.gov/Worksite/DisplayResults.asp?minlevel='

while i <= 520:
  current_url = base_url + str(i)
  i = i + 15

pq(url="http://app.cab.dc.gov/Worksite/DisplayResults.asp?minlevel=0&displaytype=")
output = p('tr').hasClass('text')
