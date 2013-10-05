#!/usr/bin/env python

#Sole Source Scraper

from pyquery import PyQuery as pq
import json
import os
import string

ss = pq(url="http://app.ocp.dc.gov/RUI/information/scf/SolNumRespond.asp")

## Here's how this is going to work
# The content is in a table in the div class "contentContainer".
# But the table is actually a table within the table, so now it looks for the second table
content = ss('div').filter('.contentContainer').find('table').eq(1)

# The table has a first row with headers. The second row and all subsequent rows are the contents.

data = []
#json_data = open('solesource.json','r+')
#d0 = json.load(json_data)

# Loop through the rows
for row in content.find('tr'):
  cells = row.cssselect('td')

  # skip header row
  if cells[0].text_content() == "Solicitation Number":
    continue

  # get the link to the Determinations and Findings
  df = row.cssselect('a')
  
# Now, we look through the existing json_data to see whether there is already the id in the file

#  # First, there's the list, with n items... so json_data[0] is the first dict, json_data[1] is the second dict
#  for i in d0:
#  # Then you have the D&F value in the dict = the D&F value of the cell, run away, 
#    ex = i.get('determinations_and_findings_link')
#    if ex == df[0].get('href'):
#      continue
  
  # otherwise, append a dict of sole source data to the main data array,
  # with keys named after each cell
  data.append({
    "solicitation_number": cells[0].text_content().strip(),
    "caption": cells[1].text_content().strip(),
    "closing_date": cells[2].text_content().strip(),
    "closing_time": cells[3].text_content().strip(),
    "solicitation_link": df[0].get('href').strip(),
    "issuance_date": cells[4].text_content().strip(),
    "agency": cells[5].text_content().strip(),
    "market_type": cells[6].text_content().strip(),
    "status": cells[7].text_content().strip()
  })

# This will spit out prettily formatted JSON (indent of 2 spaces).
output = json.dumps(data, indent=2)
print output


# And this will replace the existing JSON file with the modified one
#json_data.seek(0,0)
#json_data.write(output)
#json_data.close()

# This will now push directly to github
#from subprocess import call
#call('git commit -a -m "auto-update"', shell=True)
#call('git push', shell=True)
