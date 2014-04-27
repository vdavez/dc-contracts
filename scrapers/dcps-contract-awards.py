from pyquery import PyQuery as pq
import re
import csv

base_url=r'http://dclibrary.org/about/contractawards?page='

out_file='dcps_contract_award.csv'

page_num=0
rows=[]

#For testing the mechanism for looping through pages
def fakeProcessPage(url):
	print pq(url=url)('body').html()

def processPage(url):

		#s=pq(file='file:// ....') for testing on a local html file 
		s=pq(url=url)
		for elem in s('.views-row'):
			cols=[]
			text=s(elem).text()
			if 'Department' in text and 'Caption' in text:
				for matcher in [r'\s([^\s]+)\s+Published', r'Published\son\s(.+)Department:',r'Department:\s(.+)COTR', r'COTR:\s(.+)Amount:',r'Amount:\s(.+)Period',r'Period:\s(.+)Caption:',r'Period:\s(.+)\sthrough',r'through(.+)Caption:',r'Caption:\s(.+)']:
					mightMatch=re.search(matcher,text)
					textToAdd=u'null'
					if mightMatch and mightMatch.group(1):
						textToAdd=mightMatch.group(1).replace('More Information','').strip().encode('utf-8')
					cols.append(textToAdd)
				link=s(elem).find('a[title*="More Information"]')
				if link:
					href=link.attr('href')
					if href[0]=='/':
						href=u'http://dclibrary.org'+href
					cols.append(href)
				else:
					cols.append(u'null')
				rows.append(cols)

#Process pages until get to one without any contract data
while True:
	url=base_url+str(page_num)
	print 'scanning page '+url
	s=pq(url=url)
	print s('body').text()[0:50]
	if  'Contract Award Data' not in s('body').text() and 'Contract Number' not in s('body').text():
		print 'not found'
		break
	else:
		processPage(url)
		page_num+=1

#Find out which contracts we already have data for
prev_scraped=[]
#open in universal newline mode. Fixes problem with editing
#in Excel and then saving
with open(out_file, 'rU') as f:
	reader=csv.reader(f)
	for row in reader:
		prev_scraped.append(row[0])


#output rows to csv
with open(out_file,'a') as f:
	row_writer=csv.writer(f).writerows
	#Write headers
	row_writer([['contract_award_data', 'published_date', 
'department', 'cotr', 'amount', 'period', 'period_start', 'period_end', 'caption', 'more_info_pdf']])
	#write rows one at a time, checking to see if already scraped
	for row in rows:
		if row[0] not in prev_scraped:
			row_writer([row])		

	

