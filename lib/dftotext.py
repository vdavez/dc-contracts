#!/usr/bin/env python

import json
import os
import urllib
from subprocess import call
import codecs

def dftotext (df_url, ocr="true", *args, **kwargs):
	url = urllib.urlopen(df_url).geturl()
	urllib.urlretrieve(url, "/home/vzvenyach/Coding/dc-contracts/scrapers/dfs/df.pdf")
	if (ocr == "true"):
		call("./pdfocr -i '/home/vzvenyach/Coding/dc-contracts/scrapers/dfs/df.pdf' -o '/home/vzvenyach/Coding/dc-contracts/scrapers/dfs/dfocr.pdf'", shell=True)
	call("pdftotext -layout '/home/vzvenyach/Coding/dc-contracts/scrapers/dfs/dfocr.pdf'", shell=True)
	f = codecs.open('/home/vzvenyach/Coding/dc-contracts/scrapers/dfs/dfocr.txt', encoding='utf-8', errors='ignore', mode='r').read()
	call("rm /home/vzvenyach/Coding/dc-contracts/scrapers/dfs/dfocr.pdf; rm /home/vzvenyach/Coding/dc-contracts/scrapers/dfs/df.pdf; rm /home/vzvenyach/Coding/dc-contracts/scrapers/dfs/dfocr.txt", shell=True)
	return f
