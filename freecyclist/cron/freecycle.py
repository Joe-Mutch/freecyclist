import urllib, json, requests
import re
from bs4 import BeautifulSoup
from freecyclist import app
from freecyclist.models import db, User, Location, Alert, Keyword, Result

class AlertChecker():
	groupsUrl = 'https://www.freecycle.org/browse/UK/London'

	def __init__(self, alert):
		self.anywhere = False
		self.alert = alert
		self.locations = []
		self.keywords = []

		for l in alert.locations:
			self.locations.append(l.name)
		for k in alert.keywords:
			self.keywords.append(k.name)


	def find_stuff(self, url):
		r = requests.get(url)
		html = r.content
		soup = BeautifulSoup(html)
		postTable = soup.find(id="group_posts_table")
		rows = postTable.findChildren(['tr'])

		for row in rows:

			cells = row.findChildren('td')
			actionCell = cells[0].getText()
			actionCellText = actionCell.encode("utf-8").lower()
			description = cells[1].findChildren('a')[0].getText().encode("utf-8")
			url = cells[1].findChildren('a')[0]['href']

			if 'offer' in actionCellText:
				for stuff in self.keywords:
					if stuff in description.lower():

						exists = Result.query.filter_by(alert=self.alert, url=url).first()
						if not exists:
							result = Result(alert=self.alert, url=url, title=description, full_text=description)
							db.session.add(result)
							db.session.commit()
							self.alert.user.notify(result)

	def search_locations(self, locations):
		r = requests.get(self.groupsUrl)
		html = r.content
		groupSoup = BeautifulSoup(html)
		groupUrls = groupSoup.find_all('a', href=re.compile('http://groups.freecycle\.org'))
		for urlSoup in groupUrls:
			location = urlSoup.getText().lower()
			if 'camden' in location or self.anywhere:
				options = '/posts/offer?page=1&resultsperpage=10&showall=off'
				url = urlSoup['href'] + options
				self.find_stuff(url)

	def find(self):
		for l in self.locations:
			self.search_locations(l)