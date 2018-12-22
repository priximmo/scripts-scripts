#!/usr/bin/python3
# coding=utf-8
import curl
from curl import Curl
import lxml.html as lhtml
import sys

counter = 0

def get_counter(i) -> int:
	global counter
	counter=counter+i
	return counter

cities = ['Dallas',
		  'Richardson',
		  'Addison',
	]

links = []

def crawlCraigz(iterations):
	global cities
	global links
	
	if get_counter(0) is not 0 and iterations*120 != get_counter(0):
		return
	
	cl = Curl(base_url="", fakeheaders=[
		'Cookie: cl_b=5GEZ9Y0F6RGXNBZ5tq5GrwngXVs; cl_def_hp=dallas',
		])
	
	page = cl.get("http://dallas.craigslist.org/search/roo",{
		's': get_counter(120),
		'search_distance': 13,
		'postal': 75214,
		'min_price': 400,
		'max_price': 600,
		'availabilityMode': 0,
		})

	doc = lhtml.document_fromstring(page)
	for l in doc.iterlinks():
		for c in cities:
			linktext = l[2]
			linktext = linktext[14::]
			if c in str(l[0].text) or c.lower() in linktext:
				links.append(l[2]+'\n')
				print(l[2])
	
	return crawlCraigz(iterations)

outfile = sys.argv[1]
pages = sys.argv[2]

with open(outfile, "w+") as filo:
	crawlCraigz(pages)
	filo.write(''.join(links))
