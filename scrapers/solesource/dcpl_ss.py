#!/usr/bin/env python3 
from lxml import html
import json
import re

base_url = "http://dclibrary.org/node/31079"
ss = html.parse(base_url)

json_data = open('/home/vzvenyach/Coding/opensourcingdc/static/data/dcpl_ss.json','r+')
d0 = json.load(json_data)
data = []

'''
# Eventually, this is going to be abstracted and rebuilt using classes/modules, but for now this is just a placeholder
class Site(soleSourceCite):
	def __init__(self):
		super(Site, self).__init__() 
		self.ds = '/home/vzvenyach/Coding/opensourcingdc/static/data/dcpl_ss.json'
		self.url = 'http://dclibrary.org/node/31079'
'''

# Go through each row in the sole-source table
content = ss.xpath('//tr')
for row in content:
	cells = row.xpath('td')
	if cells[0].text_content() == "Notice Date" or cells[0].text_content() == u"\xa0":
		continue
	
	if len(cells) > 3:	
		for i in d0:
			ex = i.get('determinations_and_findings_link')
			if ex == cells[3].xpath('.//a/@href')[0]:
				break
		data.append({
			"notice_date": cells[0].text_content(),
			"response_due_date": cells[1].text_content(),
	    		"description": re.sub("\n","",cells[2].text_content()),
			"vendor": re.sub("Determination.*","",cells[3].text_content()),
	      		"determinations_and_findings_link": cells[3].xpath('.//a/@href')[0],
	      		"agency": "District of Columbia Public Library",
			"contact": cells[4].text_content()
		})

output = data + d0
json_data.seek(0,0)
out = json.dump(output, json_data, indent=2, sort_keys=True)