################################################################################
# Will Macxy
# Hot Air Blog Scraper
# Last Updated : 4/22/2021
################################################################################

from bs4 import BeautifulSoup as s
from urllib.request import Request, urlopen
import sys
import re
import csv


# Main function to scrap individual blogs, used by the main function
def scrape(url):

	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

	webpage = urlopen(req).read()

	soup = s(webpage, "lxml")	

	#variable names
	title = soup.find('title')
	date = re.findall(r'[0-9][0-9][0-9][0-9]\/[0-9][0-9]\/[0-9][0-9]',url)
	author = soup.find('meta', attrs={'name':'author'})
	body = soup.find_all('p')
	body = body[:-1]

	#cleaning of text
	textTitle = title.get_text().replace(',','')[:-8]
	textDate = date[0].replace('/','-')
	textAuthor = author['content']

	textBody = textTitle + ', '+ textAuthor + ", " + textDate + ", "

	#creation of text body
	for text in body:
		textBody = textBody + text.get_text().replace(',','')+' '

	textBody = textBody + '\n'
	
	#creation of file and file name
	blogTitle = 'C HotAir '+textAuthor+' '+textTitle+'.csv'
	invalid = '<>:\"\\|?*\'/'
	for char in invalid:
		blogTitle = blogTitle.replace(char,'')
	
	#terminal output
	print('HotAir: '+textTitle)

	#wrint of file
	file = open(sys.path[0]+"/SavedBlogs/"+blogTitle , "w+", encoding = 'utf-8')
	file.write(textBody)
	file.close()
	

	return()

#main function, used to fine dynamic blog listing page
def main():
	
	#start page, 50 entries per page
	startPage = 0
	#number of blog posts on page request, 50 max
	numPosts = 50

	#variable names
	url = 'https://hotair.com/?action=th_infinite_scroll&infinite_paged='+str(startPage)+'&infinite_posts_per_page='+str(numPosts)+'&infinite_pagetype=archive'
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	soup = s(webpage, "html.parser")
	links = soup.find_all(class_='wp-card__img mt-2')
	linkList = []
	
	#loop that calls individual blog post urls
	for link in links:
		linkList.append(str('https://hotair.com') + link.find('a').get('href'))

	#loop that scrapes individual bloog posts
	for link in linkList:
		scrape(link)

	
	return()

main()