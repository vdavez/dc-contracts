#Sole Source Scraper
from pyquery import PyQuery as pq

d = pq(url="http://app.ocp.dc.gov/intent_award/intent_award.asp")

## Here's how this is going to work
# The content is in a table in the div class "contentContainer".
content = d('div').filter('.contentContainer')

# The table has a first row with headers. The second row and all subsequent rows are the contents.

out = ""

# Loop through the rows
for i in content.items('TR'):
  for c in i.items('TD'):
    out = out + '"' + c.text() + '",'
  out = out + '\n'

#This will spit out a poorly formed CSV. The last character the line is a comma...
print out


# Within the fourth column, there is a link. That's the D&F PDF.
