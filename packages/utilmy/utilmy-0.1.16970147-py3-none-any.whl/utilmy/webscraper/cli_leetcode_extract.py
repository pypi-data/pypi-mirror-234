"""  Leetcode HTML website
Docs::

    pip install fire

	cd myfolder
	python  cli_leetcode_extract.py  run --url  https://ttzztt.gitbooks.io/lc/content/design-tic-tac-toe.html
	python  cli_leetcode_extract.py  render


	#run(startURL) #<-- uncomment this to download html files
	render() #<-- uncomment this to render markdown files


    https://ttzztt.gitbooks.io/lc/content/design-tic-tac-toe.html


"""
import markdownify 
import os
from bs4 import BeautifulSoup
import requests

startURL = 'https://ttzztt.gitbooks.io/lc/content/design-tic-tac-toe.html'
base = 'https://ttzztt.gitbooks.io/lc/content/'
path = '' # <-- path to the directory where the files are stored


def getFirstHtml(url):
	html = requests.get(url).text
	soup = BeautifulSoup(html, 'html.parser')
	return soup


def getAllHtml(soup: BeautifulSoup):
  	return soup.find_all('a', href=True)


def downloadHtml(soup: BeautifulSoup):
	i = 0
	for link in soup:
		i += 1
		if 'html' in link['href']:
			print(link['href'])
			completeName = os.path.join(path, link['href'])
			try:
				
				#if file already exists, skip it
				if os.path.isfile(completeName):
					continue

				f = open(completeName, 'w', encoding='utf-8')
				html = requests.get(base + link['href']).text
				format = BeautifulSoup(html, 'html.parser')
				f.write(format.prettify())
			except FileNotFoundError:
				#create subdirectory
				os.mkdir(os.path.join(path, link['href'].split('/')[0]))

				f = open(completeName, 'w', encoding='utf-8')
				html = requests.get(base + link['href']).text
				format = BeautifulSoup(html, 'html.parser')
				f.write(format.prettify())
			except Exception as e:
				print(e)
				pass
		# if i == 10:
		# 	break

def run(url):
	soup = getFirstHtml(url)
	urls = getAllHtml(soup)
	downloadHtml(urls)


file_names = [file for file in os.listdir(path) if file.endswith('.html')]


def clearNewLines(raw_html):
	cleantext = raw_html.replace('\n\n\n\n\n\n', '')
	return cleantext

def clearScript(raw_html):

	soup = BeautifulSoup(raw_html, 'html.parser')
	#remove all scripts

	bookSummary = soup.find('div', class_='book-summary')
	if bookSummary:
		bookSummary.decompose()



	for s in soup.select('script'):
		s.extract()

	for s in soup.select('style'):
		s.extract()


	h2 = soup.find('h2')
	if h2:
		h2.extract()

	title = soup.find('title')
	if title:
		title.extract()

	searchResult = soup.find('div', class_='search-results')
	if searchResult:
		searchResult.decompose()

	soup = BeautifulSoup(str(soup.prettify()), 'html.parser')

	text = soup.find_all('strong')
	for t in text:
		t.unwrap()

	soup = clearNewLines(str(soup.prettify()))
	soup = BeautifulSoup(soup, 'html.parser')
	return soup.prettify()


def render():
	result = open("results.txt", "a", encoding="utf-8")

	for file in file_names:
		f = open(os.path.join(path, file), "r", encoding="utf8")
		md = f.read()

		md = clearScript(md)

		text = clearNewLines(markdownify.markdownify(md, strong_em_symbol = '---', escape_asterisks=False, escape_underscores=False, strip = ['a']))

		result.write("\n------------------------\n")
		result.write(text)


	result.close()



if __name__ == "__main__":
    import fire
    fire.Fire()



