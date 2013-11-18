#!/usr/bin/env python

import json
import os

# Get the blob.json file
json_data = open('blob.json')
data = json.load(json_data)

for i in data:
    date = i.get('date_filed').replace(r'/','-')
    file_name = 'opinions/txt/' + i.get('case_number') + '_' + date + '.txt'
    
'''    try:
        f = open(file_name,'r')
        txt = f.read()
        f.close()
    except IOError:
        txt = ''

    i['opinion_text'] = txt
'''

print json.dumps(data,indent=2)
