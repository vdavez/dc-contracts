#!/usr/bin/env python

# SoleSourceDiff

# Here's how this is gonna work.
# First, record the date of the update.

from pyquery import PyQuery as pq
import os
from subprocess import call

# Get the new content from the site (c1)
x = pq(url='http://app.ocp.dc.gov/intent_award/intent_award.asp')
c1 = str(x('div').filter('.contentContainer'))

# Now dump the new content (c1) into a file (c1.html)

f = open('c1.html','w')
f.write(c1)

delta = call("diff c0.html c1.html > solesourcediff.html", shell=True)

# Concept is to download a site. Then, on the update, download the site again.
# Run a diff on the "ContentContainer".
# The diff should only be new sole source contracts.
# Then spit out the new line into the json-engine
