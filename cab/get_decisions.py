#!/usr/bin/env python
import os
import mechanize
import cookielib
import json
import urllib

#initialize outfile
out = open('glob.html', 'w')

# Open the browser and initialize the cookie jar
br = mechanize.Browser()
cj = cookielib.CookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
br.set_debug_http(True)
br.set_debug_redirects(True)
br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

br.open('http://app.cab.dc.gov/WorkSite/Published_Board_Decisions.asp')
br.select_form(name="TheForm")
br.submit

json_data = open('blob.json')
data = json.load(json_data)

for i in data:
    date = i.get('date_filed').replace(r'/','-')
    file_name = 'opinions/' + i.get('case_number') + '_' + date
    doc_url = 'http://app.cab.dc.gov/WorkSite/' + i.get('url')
    
#   This is the part that I need to figure out...
    br.retrieve(doc_url, file_name)