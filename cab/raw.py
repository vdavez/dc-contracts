#!/usr/bin/env python
import os
import json

json_data = open('blob.json')
data = json.load(json_data)
dir = 'raw'

for i in data:
	filename = i.get('row_id') + '.json'
	log_path = os.path.join(dir,filename)
	with open(log_path,'w') as f:
		outstr = json.dumps(i,indent=2)
		f.write(outstr)