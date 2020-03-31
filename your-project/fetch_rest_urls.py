import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
import time
import random as rd

headers = {'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
response = requests.get('https://www.zomato.com/grande-lisboa', headers=headers)
html = response.content
soup = BeautifulSoup(html, 'lxml')
meal_types_results = soup.find_all('a', class_='column ta-center start-categories-item')
meal_types_links = [link['href'] for link in meal_types_results]
fine_dining_url = meal_types_links.pop(-1)
print(fine_dining_url)

restaurants = []

try:
	for link in meal_types_links:
		response = requests.get(link, headers=headers)
		html = response.content
		soup = BeautifulSoup(html, 'lxml')
		div = soup.find('div', 'col-l-4 mtop pagination-number')
		pages = div.contents[0].b.find_next_siblings('b')[0].string
		print("Working on url meal type " + link + '...')
		try:
			for i in range(1, int(pages) + 1):
				print('Page ' + str(i) + ' of ' + pages, end='\r')
				response = requests.get(link + '?page=' + str(i), headers=headers)
				restaurants_html = response.content
				restaurants_soup = BeautifulSoup(restaurants_html, 'lxml')
				restaurants_results = restaurants_soup.find_all('a', class_='result-title hover_feedback zred bold ln24 fontsize0')
				restaurants.extend([link['href'] for link in restaurants_results])
				time.sleep(rd.randrange(1,4))
		except:
			print("Something went wrong in getting the restaurants' url.")
except:
	print('Something went wrong in getting the number of pages.')

response = requests.get(fine_dining_url, headers=headers)
html = response.content
soup = BeautifulSoup(html, 'lxml')
div = soup.find('div', 'col-l-4 mtop pagination-number')
pages = div.contents[0].b.find_next_siblings('b')[0].string
print("Working on url meal type " + fine_dining_url + '...')

try:
	for i in range(1, int(pages) + 1):
		print('Page ' + str(i) + ' of ' + pages, end='\r')
		response = requests.get(fine_dining_url + '&page=' + str(i), headers=headers)
		restaurants_html = response.content
		restaurants_soup = BeautifulSoup(restaurants_html, 'lxml')
		restaurants_results = restaurants_soup.find_all('a', class_='result-title hover_feedback zred bold ln24 fontsize0')
		restaurants.extend([link['href'] for link in restaurants_results])
		time.sleep(rd.randrange(1,4))
except:
	print("Something went wrong in getting the restaurants' url.")

print(restaurants)