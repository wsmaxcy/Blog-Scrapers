################################################################################
# Will Maxcy
# Red State blog scraper
# Last Edited: 4/22/2021
################################################################################

from bs4 import BeautifulSoup as s
from urllib.request import Request, urlopen
import sys
import re
import csv


# scraper of individual blogs
def scrape(url):
	
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

	webpage = urlopen(req).read()

	soup = s(webpage, "lxml")	

	title = soup.find('title')
	date = re.findall(r'[0-9][0-9][0-9][0-9]\/[0-9][0-9]\/[0-9][0-9]',url)
	author = soup.find('meta', attrs={'name':'author'})
	body = soup.find_all('p')
	body = body[:-1]
	
	textTitle = title.get_text().replace(',','')[:-11]
	textDate = date[0].replace('/','-')
	textAuthor = author['content']
	
	textBody = textTitle + ', '+ textAuthor + ", " + textDate + ", "

	for text in body:
		textBody = textBody + text.get_text().replace(',','')+' '

	textBody = textBody + '\n'

	blogTitle = 'C RedState '+textAuthor+' '+textTitle+'.csv'
	invalid = '<>:\"\\|?*\'/'
	for char in invalid:
		blogTitle = blogTitle.replace(char,'')
	
	print("RedState: "+textTitle)

	file = open(sys.path[0]+"/SavedBlogs/"+blogTitle , "w+", encoding = 'utf-8')
	file.write(textBody)
	file.close()
	

	return()


def main():

	for x in range(1,10):
		url = 'https://redstate.com/page/' + str(x) +'?ordinal='+ str((x-1)*9 + 1)+'&id=759800'
		req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		webpage = urlopen(req).read()
		soup = s(webpage, "html.parser")
		links = soup.find_all(class_='wp-card__img')
	
		linkList = []

		
		

		for link in links:
			linkList.append(str('https://redstate.com') + link.find('a').get('href'))

		for link in linkList:
			
			scrape(link)

	return()

main()