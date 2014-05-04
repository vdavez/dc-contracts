from pyquery import PyQuery as pq
import re
import csv
import os

base_url=r'http://dclibrary.org/about/contractawards?page='

out_file='dcps_contract_award.csv'

page_num=0
rows=[]

column_headers=['contract_award_data', 'published_date', 
'department', 'cotr', 'amount', 'period', 'caption', 'more_info_pdf']

#For testing the mechanism for looping through pages
def fake_process_page(url):
	print pq(url=url)('body').html()

def process_elem(elem):
	cols=[]
	text=s(elem).text()
	if 'Department' in text and 'Caption' in text:
		for matcher in [r'(.*?)Published', r'.*?Published(.*?)Department',r'.*?Department(.*?)COTR', r'.*?COTR(.*?)Amount',r'.*?Amount(.*?)Period',r'.*?Period(.*?)Caption',r'.*?Caption(.*)']:
			mightMatch=re.search(matcher,text,flags=re.DOTALL)
			textToAdd=u'null'
			if mightMatch and mightMatch.group(1):
				textToAdd=mightMatch.group(1).replace('More Information','').rstrip()
				textToAdd=re.sub('^\s*:\s*','',textToAdd)
			cols.append(textToAdd)
		link=s(s(elem).find('a')[1])
		if link:
			href=link.attr('href')
			if href[0]=='/':
				href=u'http://dclibrary.org'+href
			if len(href)==0:
				href=u'null'
			cols.append(href)
		else:
			cols.append(u'null')
		#Simplify first column
		cols[0]=re.sub('^.*?Number:?\s*?|^.*?Data:?\s*?','',cols[0])
		#get rid of day of week in published date
		cols[1]=re.sub('^.*?, ','',cols[1],flags=re.DOTALL)
		cols=[col.encode('utf-8') for col in cols]
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

contract_ids=[row[0] for row in rows]
#Will contain previously-scraped records that don't exist in newly-scraped records
prev_out_rows=[]
#Append to out_file if it exists
if os.path.isfile(out_file):
	with open(out_file, 'rU') as f:
		reader=csv.reader(f)
		for row in reader:
			if row[0] not in contract_ids and row[0] not in column_headers[0]:
				prev_out_rows.append(row)
	with open(out_file,'w') as f:
		f.truncate()

#output rows to csv
with open(out_file,'a') as f:
	row_writer=csv.writer(f).writerows
	#Write headers
	row_writer([column_headers])
	#Write previously-scraped rows
	if len(prev_out_rows)>0:
		row_writer(prev_out_rows)
	for row in rows:
		row_writer([row])		

	

