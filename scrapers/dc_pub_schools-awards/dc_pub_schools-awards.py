from pyquery import PyQuery as pq
import re
import csv
import os

url=r'http://dcps.dc.gov/DCPS/About+DCPS/Doing+Business+with+DCPS/Procurement/Solicitations'
out_file='dcps-contract-awards.csv'
s=pq(url=url)
rows=[]


column_headers=[ 'Solicitation Number','Caption' ,'Market Type/NIGP Code','Alternate Contact Person', 'Primary Contact Fax (optional)', 'Alternate Contact Fax', 'Synopsis: This is a summary of the solicitation\xe2\x80\x99s contents', 'Sub-Contracting Requirement (%)', 'RFP Closing Date/Time', 'Pre-Proposal/Bid Conference Date', 'Solicitation Advertising Date', 'Alternate Contact E-mail', 'Solicitation Fee\xc2\xa0 -\xc2\xa0 Board Number', 'Primary Contact E-mail', 'Pre-Proposal/Bid Conference Time', 'Solicitation Number', 'Primary Contact Phone', 'Alternate Contact Phone', 'Solicitation Issuance Date', 'Pre-Proposal/Bid Conference Location', 'Solicitation Pick-Up Location', 'IFB Opening Date/Time', 'Work Site Location', 'Primary Contact Person']
column_headers_readable=['Solicitation Number','Caption','Market Type/NIGP Code', 'Alternate Contact Person', 'Primary Contact Fax (optional)', 'Alternate Contact Fax', 'Synopsis', 'Sub-Contracting Requirement (%)', 'RFP Closing Date/Time', 'Pre-Proposal/Bid Conference Date', 'Solicitation Advertising Date', 'Alternate Contact E-mail', 'Solicitation Fee and Board Number', 'Primary Contact E-mail', 'Pre-Proposal/Bid Conference Time', 'Primary Contact Phone', 'Alternate Contact Phone', 'Solicitation Issuance Date', 'Pre-Proposal/Bid Conference Location', 'Solicitation Pick-Up Location', 'IFB Opening Date/Time', 'Work Site Location', 'Primary Contact Person']

class Row(object):
	def __init__(self, html_table):
		self.html_table=html_table

	def as_dict(self):
		'''returns a representation of the row as a list. If not available,
		creates the representation and then returns it'''
		try:
			self.__as_dict__
		except:
			self.__as_dict__={}
			for row in s(self.html_table).children('tr'):
				key=s(s(row).children('td')[1]).text().strip()
				text=s(s(row).children('td')[2]).text().strip()
				text=re.sub(r"[\xa0-\xff]",'',text)
				if text is not 'Item' and text is not 'Description' and len(text)>0:
					self.__as_dict__[key.encode('utf-8')]=text.encode('utf-8')
		return self.__as_dict__

	def as_list(self,column_headers):
		'''returns a representation of the row as a list. If not available,
		creates the representation and then returns it'''
		try:
			self.__as_list__
		except:
			as_dict=self.as_dict()
			self.__as_list__=['null' for x in range(len(column_headers))]
			for i in range(len(column_headers)):
				if column_headers[i] in as_dict:
					self.__as_list__[i]=as_dict[column_headers[i]]
		return self.__as_list__

s_html_tables=s('table.msonormaltable')

for html_table in s('table.msonormaltable'):
	rows.append(Row(html_table).as_list(column_headers))


solicitation_number=[row[0] for row in rows]
#Will contain previously-scraped records that don't exist in newly-scraped records
prev_out_rows=[]
#Append to out_file if it exists
if os.path.isfile(out_file):
	with open(out_file, 'rU') as f:
		reader=csv.reader(f)
		for row in reader:
			if row[0] not in solicitation_number and row[0] not in column_headers_readable[0]:
				prev_out_rows.append(row)
	with open(out_file,'w') as f:
		f.truncate()

#output rows to csv

with open(out_file,'a') as f:
	row_writer=csv.writer(f).writerows
	row_writer([column_headers_readable])

	#Write previously-scraped rows
	if len(prev_out_rows)>0:
		row_writer(prev_out_rows)
	#Write new rows
	for row in rows:
		row_writer([row])		

