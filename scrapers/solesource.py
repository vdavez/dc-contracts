#Sole Source Scraper
from pyquery import PyQuery as pq

d = pq(url="http://app.ocp.dc.gov/intent_award/intent_award.asp")

# print "This is the title of the scraped website:"
# print d("title").text()

## Here's how this is going to work
# The content is in a table in the div class "contentContainer".
# The table has a first row with headers
# The second row and all subsequent rows are the contents.
# Within the fourth column, there is a link. That's the D&F PDF.
