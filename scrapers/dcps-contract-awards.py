from pyquery import PyQuery as pq
import re
import csv
import os

base_url=r'http://dclibrary.org/about/contractawards?page='

out_file='dcps_contract_award.csv'

page_num=0
rows=[]

#For testing the mechanism for looping through pages
def fake_process_page(url):
	print pq(url=url)('body').html()

def process_elem(elem):
	cols=[]
	text=s(elem).text()
	if 'Department' in text and 'Caption' in text:
		for matcher in [r'\s+([^\s]+)\s+Published', r'Published\s+on\s+(.+)Department:',r'Department:\s+(.+)COTR', r'COTR:\s+(.+)Amount:',r'Amount:\s+(.+)Period',r'Period:\s+(.+)Caption:',r'Period:\s+(.+)\s+through',r'through(.+)Caption:',r'Caption:\s+(.+)']:
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
		return cols

def process_page(url):
		#s=pq(file='file:// ....') for testing on a local html file 
		s=pq(url=url)
		for elem in s('.views-row'):
			cols=process_elem(elem)
			if(cols):
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
		process_page(url)
		page_num+=1

contract_ids=[rows[0] for row in rows]
#Will contain previously-scraped records that don't exist in newly-scraped records
prev_out_rows=[]
#Append to out_file if it exists
if os.path.isfile(out_file):
	with open(out_file, 'rU') as f:
		reader=csv.reader(f)
		for row in reader:
			if row[0] not in contract_ids:
				prev_out_rows.append(row)

#output rows to csv
with open(out_file,'a') as f:
	row_writer=csv.writer(f).writerows
	#Write headers
	row_writer([['contract_award_data', 'published_date', 
'department', 'cotr', 'amount', 'period', 'period_start', 'period_end', 'caption', 'more_info_pdf']])
	#Write previously-scraped rows
	if len(prev_out_rows)>0:
		row_writer(prev_out_rows)
	for row in rows:
		row_writer([row])		

	

