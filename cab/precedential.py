#!/usr/bin/env python
import os
import mechanize
from pyquery import PyQuery as pq
import json

#initialize outfile
out = open('glob.html', 'w')

br = mechanize.Browser()
br.open('http://app.cab.dc.gov/WorkSite/Published_Board_Decisions.asp')
br.select_form(name="TheForm")
response = br.submit().read()

# print response

# start out with i being 0
d = pq(response)
data = []
i=0

for row in d('table').eq(0).find('tr').filter('.text'):

#  if row.find('span').hasClass('foot1'):
#    continue
  cells = row.cssselect('td')
  
  data.append({
    "row_id":str(i),
    "date_filed":cells[0].text_content(),
    "description":cells[1].text_content(),
    "url":cells[1].cssselect('a')[0].get('href'),
    "case_number":cells[2].text_content(),
    "file_size":cells[3].text_content(),
#    "file_type":cells[4].cssselect('img')[0].get('alt')
  })
  i = i + 1

# Do it for the follow-on pages
j = 15
new_url = 'http://app.cab.dc.gov/Worksite/DisplayResults.asp?minlevel='

while j <= 520:
	url= new_url + str(j)
	
	d2 = pq(br.open(url).read())	
	#d2=pq(s.post(url).text.encode('utf-8'))
	
	for row in d2('table').eq(0).find('tr').filter('.text'):
		cells = row.cssselect('td')
		data.append({
		  "row_id":str(i),
		  "date_filed":cells[0].text_content(),
		  "description":cells[1].text_content(),
		  "url":cells[1].cssselect('a')[0].get('href'),
		  "case_number":cells[2].text_content(),
		  "file_size":cells[3].text_content(),
#		  "file_type":cells[4].cssselect('img')[0].get('alt')
		})
		i = i +1
	j = j + 15

print json.dumps(data,indent=2)
out.close()
