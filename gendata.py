from bs4 import BeautifulSoup
import requests
import numpy as np
import time
import random
import json
import os

def extract_style(html):
    locate_style = html.find('Style:')
    subhtml = html[locate_style:]
    start = subhtml.find('">')
    end = subhtml.find('</a>')
    style = subhtml[start+len('">'):end]
    style = style.replace('<br>','')
    style = style.encode('ascii', 'ignore')
    return style

def extract_name(html):
    locate_name = html.find('TITLE>')
    subhtml = html[locate_name:]
    start = subhtml.find('<TITLE>')
    end = subhtml.find('</TITLE>')
    name = subhtml[start+len('<TITLE>'):end]
    name = name.replace('<br>','')
    name = name.encode('ascii', 'ignore')
    return name

def extract_brewery(html):
    locate_brewery = html.find('Brewed by')
    subhtml = html[locate_brewery:]
    start = subhtml.find('">')
    end = subhtml.find('</A>')
    brewery = subhtml[start+len('">'):end]
    brewery = brewery.replace('<br>','')
    brewery = brewery.encode('ascii', 'ignore')
    return brewery

def extract_descript(html):
    locate_descript = html.find('COMMERCIAL DESCRIPTION')  
    subhtml = html[locate_descript:]
    start = subhtml.find('</small>')
    end = subhtml.find('</div>')
    descript = subhtml[start + len('</small>'): end]
    descript = descript.replace('<br>','')
    descript = descript.replace('<br>','')
    descript = descript.encode('ascii', 'ignore')
    return descript

def extract_ratebeer(html):
    #return dictionary for that beer entry
	link_beer = html
	r = requests.get(link_beer)
	htmlbeer = r.text
	name = extract_name(htmlbeer)
	descr = extract_descript(htmlbeer)
	brewery = extract_brewery(htmlbeer)
	style = extract_style(htmlbeer)
	ratebeer_dict = {name: (descr, brewery, style, link_beer)}
	return ratebeer_dict

def addtodict(dic, beerdic):
    beerdic.update(dic)

def append_record(record):
    with open('masterbeer.json', 'a') as f:
        json.dump(record, f)
        f.write(os.linesep)


def gen_beerlist(html):
    with open(html) as file:
        soup = BeautifulSoup(file, ["lxml", "xml"])
    
    result = soup.findAll('A')
    result = result[1:] #first result isn't a beer url
    links = []
    for r in result:
        rlink, rname = extract_url(r)
        html_base = 'http://www.ratebeer.com'
    	rlink = html_base + rlink
        links.append(rlink)
    if len(links) != 0:
    	return links
    else:
    	for link in soup.find_all('a', class_='html-attribute-value html-external-link'):
        	link_val = link.get('href')
       		if link_val.find('/beer/') != -1 and link_val.find('distribution/') == -1:
       			links.append(link_val)

        
        return links[:-1]

def extract_url(list_el):
	link = list_el.get('HREF')
	name = link.split('/')[2]
	return link, name


# Read in list of beer type files
fileinput = 'beer_styles/beer_html_list.txt'
with open(fileinput, 'r') as f:
	read_data = f.read()

#seperate into a list of beer types
beer_types = read_data.split('\n')
#print beer_types

#for type in beer_types[:-1]: last element is -1
for type in beer_types[:-1]:
	print type
	#load in each style file and extract popular beers
	type_file = 'beer_styles/'+ type
	links_beers = gen_beerlist(type_file)
	#make new dictionary 
	beer_dic = {}
	#print links_beers
	for link in links_beers:
		#print link
		time.sleep(2*random.random())
		tmp = extract_ratebeer(link)
		addtodict(tmp, beer_dic)

	append_record(beer_dic)


