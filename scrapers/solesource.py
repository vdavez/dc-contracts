#!/usr/bin/env python

#Sole Source Scraper

from pyquery import PyQuery as pq
import json

d = pq(url="http://app.ocp.dc.gov/intent_award/intent_award.asp")

## Here's how this is going to work
# The content is in a table in the div class "contentContainer".
content = d('div').filter('.contentContainer')

# The table has a first row with headers. The second row and all subsequent rows are the contents.

data = []

# Loop through the rows
for row in content.find('tr'):
  cells = row.cssselect('td')

  # skip header row
  if cells[0].text_content() == "Notice Date":
    continue

  # get the link to the Determinations and Findings
  df = row.cssselect('a')

  # append a dict of sole source data to the main data array,
  # with keys named after each cell
  data.append({
    "notice_date": cells[0].text_content(),
    "response_due_date": cells[1].text_content(),
    "description": cells[2].text_content(),
    "vendor": cells[3].text_content(),
    "determinations_and_findings_link": df[0].get('href'),
    "agency": cells[4].text_content(),
    "contact": cells[5].text_content()
  })

# This will spit out prettily formatted JSON (indent of 2 spaces).
print json.dumps(data, indent=2)
