from bs4 import BeautifulSoup as s
from urllib.request import Request, urlopen
import sys
import re

def scrape(url):
	
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

	webpage = urlopen(req).read()

	soup = s(webpage, "lxml")

	title = soup.find('title')
	date = re.findall(r'story\/[0-9][0-9][0-9][0-9]\/*[0-9]*[0-9]\/*[0-9]*[0-9]',url)
	
	author = soup.find_all(class_='byline__name')
	
	body = soup.find_all('p')
	
	textTitle = title.get_text().replace(',','')
	textDate = date[0][6:].replace('/','-')
	
	if(textDate[6]=='-'):
		textDate = textDate[:5]+'0'+textDate[5:]

	if(len(textDate)==9):
		textDate = textDate[:8]+'0'+textDate[8:]

	textAuthor = author[1].get_text().replace('\n','').replace('by','')
	textAuthor = re.sub(r'(?<=\s)\s+', '',textAuthor)[1:].rstrip()
	
	

	textBody = textTitle + ', '+ textAuthor + ", " + textDate + ", "

	for text in body:
		textBody = textBody + text.get_text().replace(',','')+' ' 

	textBody = textBody + '\n'
	
	blogTitle = 'L DailyKos '+textAuthor+' '+textTitle+'.csv'
	invalid = '<>:\"\\|?*\'/\n'
	for char in invalid:
		blogTitle = blogTitle.replace(char,'')
	
	print("DailyKos: "+textTitle)

	file = open(sys.path[0]+"/SavedBlogs/"+blogTitle , "w+", encoding = 'utf-8')
	file.write(textBody)
	file.close()

	return()

def main():
	url = 'https://www.dailykos.com/part/story/table/by_current'
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	soup = s(webpage, "html.parser")
	links = soup.find(class_='styled storiesAsGrid').find_all(class_='title')
	linkList = []
	#print(links)


	for link in links:
		linkList.append(link.get('href'))

	for link in linkList:
		scrape('https://www.dailykos.com'+link)

	for x in range(1,10):
		url = 'https://www.dailykos.com/part/story/table/by_current?page='+str(x)
		req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		webpage = urlopen(req).read()
		soup = s(webpage, "html.parser")
		links = soup.find(class_='styled storiesAsGrid').find_all(class_='title')
		linkList = []


		for link in links:
			linkList.append(link.get('href'))
		
		for link in linkList:
			scrape('https://www.dailykos.com'+link)
			
	return()
main()