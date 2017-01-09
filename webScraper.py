# webScraper.py - scrapes data from AAC accident reports for a given year

import requests, bs4, json

class Accident(object):
	def __init__(self, url, location, year, title):
		self.url = url
		self.location = location
		self.year = year
		self.title = title

def jsonDefault(object):
	return object.__dict__

# stores larger dictionary of Accidents
queue = []

# urls - if you want a different year's records, change it in the URLs below and in the while loop
offset = 0
modURL = 'http://publications.americanalpineclub.org/search/solr?all=&article_publication=anam&article_copyright_date=2016&article_article_type=accident_reports&article_pub_title=&route_name=&offset='
currentURL = 'http://publications.americanalpineclub.org/search/solr?all=&article_publication=anam&article_copyright_date=2016&article_article_type=accident_reports&article_pub_title=&route_name=&offset=0'

while True:
	# download page
	print('Downloading page: %s...' % currentURL)
	res = requests.get(currentURL)
	res.raise_for_status()

	# scrape page for accident reports, given in 'highlight' class
	soup = bs4.BeautifulSoup(res.text, "html.parser")
	accidents = soup.find_all(class_='highlight')
	if len(accidents) == 0:
		print('Page with offset %s is empty, printing results to file.' % offset)
		break

	# populates queue with Accident objects, 50 per page
	for index in range(len(accidents)):
		current = accidents[index]
		newAccident = Accident(current.a['href'], current.small.string, '2016', current.a.string)
		queue.append(newAccident)

	# updates currentURL to next page offset
	offset += 50
	nextURL = modURL + str(offset)
	currentURL = nextURL

# converts queue to JSON and writes it to disk
print('%s accident records found.' % len(queue))
jsonAcc = json.dumps(queue, default=jsonDefault, sort_keys=True, indent=4)
with open('2016.txt', 'w') as outfile:
	json.dump(jsonAcc, outfile, ensure_ascii=False)