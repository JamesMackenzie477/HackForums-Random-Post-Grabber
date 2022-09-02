from colorama import init, Fore
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import random
import webbrowser
import time
import os

def get_posts(fid, posts=10):
	# creates headers for requests
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:20.0) Gecko/20121202 Firefox/20.0'}
	# creates a list to store each posts url
	post_urls = []
	# sets number to increment when post is found
	number = 0
	# enters a loop while the number of found posts is lees than how much the user entered
	while number < posts:
		# gets random page number
		pagenum = random.randint(0, 483)
		# sets forum parameters
		forum = {'fid': fid, 'page': pagenum}
		# gets the forum
		r = requests.get('https://hackforums.net/forumdisplay.php', params=forum, headers=headers)

		# adds the html to beautifulsoup for parsing
		soup = BeautifulSoup(r.content, 'html.parser')

		# parses html for posts
		for post in soup.find_all('tr'):
			prefix = post.find('span', {'class': 'prefix'})
			if prefix:
				if prefix.text in ('[Release]', '[Source]', '[Tutorial]'):
					title = post.find_all('a')[1]
					number += 1
					# prints thread title
					print(Fore.LIGHTYELLOW_EX + str(number) + '.', Fore.LIGHTCYAN_EX + prefix.text, Fore.LIGHTGREEN_EX + title.text)
					# adds thread to url list
					post_urls.append(urljoin('https://hackforums.net/', title['href']))

		# sleeps for 800 miliseconds so hackforums does not block out IP
		time.sleep(0.8)

	return post_urls

def main():
	# changes console color to red
	print(Fore.LIGHTRED_EX, end='\r')
	# gets amount of post to grab from user
	amount = int(input('How many posts would you like to grab? '))
	# clears command line
	os.system('cls')

	posts = get_posts(fid='129', posts=amount)

	# sets console color to red
	print(Fore.LIGHTRED_EX)

	while True:
		try:
			# prompts user for the post number
			option = int(input('Please select a post number: '))
		except TypeError:
			print('Invalid post number entered.')
			continue

		# opens post in browser
		try:
			posturl = posts[option - 1]
			webbrowser.open(posturl)
		except IndexError:
			print('Invalid post number entered.')

if __name__ == '__main__':
	# initalises colorama
	init()
	# calls main
	main()