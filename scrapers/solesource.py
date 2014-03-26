#!/usr/bin/env python

#Sole Source Scraper

from pyquery import PyQuery as pq
import json
import re
import mailhelper
import os

ss = pq(url="http://app.ocp.dc.gov/intent_award/intent_award.asp")

## Here's how this is going to work
# The content is in a table in the div class "contentContainer".
content = ss('div').filter('.contentContainer')

# The table has a first row with headers. The second row and all subsequent rows are the contents.

data =[]
json_data = open('scrapers/solesource.json','r+')
d0 = json.load(json_data)

# Loop through the rows
for row in content.find('tr'):
  cells = row.cssselect('td')

  # skip header row
  if cells[0].text_content() == "Notice Date":
    continue

  # get the link to the Determinations and Findings
  df = row.cssselect('a')
  
# Now, we look through the existing json_data to see whether there is already the id in the file

  # First, there's the list, with n items... so json_data[0] is the first dict, json_data[1] is the second dict
  for i in d0:
  # Then you have the D&F value in the dict = the D&F value of the cell, run away, 
    ex = i.get('determinations_and_findings_link')
    if ex == df[0].get('href'):
      break 
    # otherwise, append a dict of sole source data to the main data array,
    # with keys named after each cell
  else:
    data.append({
      "notice_date": cells[0].text_content(),
      "response_due_date": cells[1].text_content(),
      "description": cells[2].text_content(),
      "vendor": cells[3].text_content(),
      "determinations_and_findings_link": df[0].get('href'),
      "agency": cells[4].text_content(),
      "contact": cells[5].text_content()
    })
  continue
# This will spit out prettily formatted JSON (indent of 2 spaces).

output = data + d0
out = json.dumps(output, indent=2)

if (data != []):
  mailhelper.maildata(data)
else:
  mailhelper.maildata('test')

# And this will replace the existing JSON file with the modified one
json_data.seek(0,0)
json_data.write(out)
json_data.close()

# This will now push directly to github
from subprocess import call
call('git commit -a -m "auto-update"', shell=True)
call('git push', shell=True)
