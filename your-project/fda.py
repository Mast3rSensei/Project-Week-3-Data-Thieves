import requests
from bs4 import BeautifulSoup
import mysql.connector
import pandas as pd
import time

headers = {'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36', 'Accept-Language': 'en-US,en;q=0.8'}

response = requests.get('https://www.zomato.com/grande-lisboa/restaurante-ba%C3%ADa-cascais-centro-lisboa', headers=headers)
html = response.content
soup = BeautifulSoup(html, 'lxml')

rest_name = soup.h1.string
neighborhood = soup.find('h1').next_sibling.contents[0].next_sibling.string
avg_rating = soup.find('p', string=['REVIEW', 'REVIEWS']).previous_sibling.previous_sibling.string
num_of_ratings = soup.find('p', string=['REVIEW', 'REVIEWS']).previous_sibling.string
avg_cost = soup.find('h5', string='Average Cost').next_sibling.string
cash_cards = soup.find('h5', string='More Info').previous_sibling.string
target_div = soup.find('h1').next_sibling.div
print(target_div)
rest_type = target_div.find_all('a', title=True)

rest_type = [typology.string for typology in rest_type]
print(rest_type)
cuisines = target_div.find_all('a', title=False)
cuisines = [cuisine.string for cuisine in cuisines]
print(cuisines)
more_infos = soup.find('h5', string='More Info').next_sibling.find_all('p')
more_infos = [info.string for info in more_infos]