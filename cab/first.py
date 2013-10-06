#!/usr/bin/env python
import os
import requests

#initialize outfile
out = open('glob.html', 'w')

# start out with i being 0
i = 15
baseUrl = 'http://app.cab.dc.gov/WorkSite/SearchDocs.asp?minLevel='
endUrl = '&OriginalURL=Published_Board_Decisions'
values = {'from_date':'','to_date':'','search_type':'fulltext','parmCount':'2','parm1':'49','parm2':'83'}

url = baseUrl + str(i) + endUrl
s = requests.session()
r = s.post(url,data=values)
#the_page = r.text.encode('utf8')	

new_url = 'http://app.cab.dc.gov/Worksite/DisplayResults.asp?minlevel='
while i <= 520:
	url= new_url + str(i)
	r2=s.post(url)
	out.write(r2.text.encode('utf-8'))
	i = i + 15
# do something with prepped.body
# do something with prepped.headers

#base_url2 = 'http://app.cab.dc.gov/Worksite/DisplayResults.asp?minlevel=15'
#values2 = {'minlevel':i}

#r2 = requests.get(base_url2)
#print r2.text

out.close()
