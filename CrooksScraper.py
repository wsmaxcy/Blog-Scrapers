from bs4 import BeautifulSoup as s
from urllib.request import Request, urlopen
import sys
from datetime import datetime
import re

def scrape(url):

	
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

	webpage = urlopen(req).read()

	soup = s(webpage, "lxml")	

	title = soup.find('title')
	date = soup.find(class_='post-created')
	author = soup.find(class_='node-byline')
	body = soup.find_all('p')

	textDate = datetime.strptime(date.get_text(), '%B %d, %Y')
	textDate = textDate.strftime('%Y-%m-%d')
	
	
	textTitle = title.get_text()[:-19].replace(',','')
	textDate = (date.get_text().split()[0]).replace('/','-')
	textDate = datetime.strptime(date.get_text(), '%B %d, %Y')
	textDate = textDate.strftime('%Y-%m-%d')
	textAuthor = author.get_text().replace('\n','')
	textBody = textTitle + ', '+ textAuthor + ", " + textDate + ", "

	for text in body:
		textBody = textBody + text.get_text().replace(',','')+' '

	textBody = textBody + '\n'

	blogTitle = 'L CrooksAndLiars '+textAuthor+' '+textTitle+'.csv'
	invalid = '<>:\"\\|?*\'/'
	for char in invalid:
		blogTitle = blogTitle.replace(char,'')
	
	print("CrooksAndLiars: "+textTitle)

	file = open(sys.path[0]+"/SavedBlogs/"+blogTitle , "w+", encoding = 'utf-8')
	file.write(textBody)
	file.close()
	

	return()

def main():

	for x in range(0,80):
		url = 'https://crooksandliars.com/?page=' + str(x)
		req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		webpage = urlopen(req).read()
		soup = s(webpage, "html.parser")
		links = soup.find_all(class_='node-image with-comment-count')
		linkList = []
		
		
		for link in links:
			linkList.append(link.find('a').get('href'))
			

		for link in linkList:
			
			scrape(link)

	return()
main()