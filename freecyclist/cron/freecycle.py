import urllib, json, requests
import re
from bs4 import BeautifulSoup
from freecyclist import app
from freecyclist.models import db, User, Location, Alert, Keyword, Result

class FreecycleScraper():
	groupsUrl = 'https://www.freecycle.org/browse/UK/London'

	def __init__(self, alert, locations, keywords):
		self.anywhere = False
		self.alert = alert
		self.locations = locations
		self.keywords = keywords

	def find_stuff(self, url):
		r = requests.get(url)
		html = r.content
		soup = BeautifulSoup(html)
		postTable = soup.find(id="group_posts_table")
		rows = postTable.findChildren(['tr'])

		for row in rows:

			cells = row.findChildren('td')
			action_cell = cells[0].getText()
			action_cell_text = action_cell.encode("utf-8").lower()
			description = cells[1].findChildren('a')[0].getText().encode("utf-8").lower()
			url = cells[1].findChildren('a')[0]['href']

			if any(k in description for k in self.keywords):
				exists =  Result.query.filter_by(alert=self.alert, url=url).first()
				if exists:
					print exists.title
					return None
				return Result(alert=self.alert, url=url, title=description, full_text=description)

	def save_result(self, result):
		print 'saving result'
		db.session.add(result)
		db.session.commit()
		self.alert.user.notify(result)

	def get_url_for_location(self, location):
		r = requests.get(self.groupsUrl)
		html = r.content
		groupSoup = BeautifulSoup(html)
		groupUrls = groupSoup.find_all('a', href=re.compile('http://groups.freecycle\.org'))

		url_soups = [ urlSoup for urlSoup in groupUrls if location in urlSoup.getText().lower()]
		for url_soup in url_soups:
			options = '/posts/offer?page=1&resultsperpage=10&showall=off'
			url = url_soup['href'] + options
			return url

	def find(self):
		print 'searching alert ==='
		print [l for l in self.locations]
		print [k for k in self.keywords]
		for l in self.locations:
			url = self.get_url_for_location(l)
			result = self.find_stuff(url)
			if result:
				self.save_result(result)