#!/usr/bin/env python

# CAB Precedential Opinion Scraper

from pyquery import PyQuery as pq
import json
import os

# Initialize the JSON file
data = []
f0 = open('glob.html','r')
print f0.readline()
print f0.readline()
blob = pq(f0)

print blob('tr').eq(1)
