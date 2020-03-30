import requests
from bs4 import BeautifulSoup
import mysql.connector
import pandas as pd

f =open('restaurants2_url.txt', encoding='utf-8')
restaurants_urls = f.read().split(",")
restaurants_urls = list(set([x.strip("[]' ") for x in restaurants_urls]))

headers = {'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36', 'Accept-Language': 'en-US,en;q=0.8'}

add_restaurant = 	("INSERT INTO restaurants "
					"(name, neighborhood, avg_rating, #_of_ratings, avg_cost, cash_cards?) "
					"VALUES (%s, %s, %f, %d, %d, %s)")

add_cuisine = 	("INSERT INTO cuisines "
				"(name) "
				"VALUES (%s)")

add_info = 	("INSERT INTO infos "
			"(name) "
			"VALUES (%s)")

add_type = 	("INSERT INTO types "
			"(name) "
			"VALUES (%s)")

add_rest_type =	("INSERT INTO rest_type "
				"(rest_ID, type_ID) "
				"VALUES ((%d, %d)")

add_rest_cuisine =	("INSERT INTO rest_cuisine "
					"(rest_ID, cuisine_ID) "
					"VALUES ((%d, %d)")

add_rest_info =	("INSERT INTO rest_info "
				"(rest_ID, info_ID) "
				"VALUES (%d, %d)")

restaurants = pd.DataFrame(columns=['ID', 'name', 'neighborhood', 'avg_rating', '#_of_ratings', 'avg_cost', 'cash_cards?', 'type', 'cuisine', 'more_infos'])

for i in range(0, 3):
	response = requests.get(restaurants_urls[i], headers=headers)
	html = response.content
	soup = BeautifulSoup(html, 'lxml')
	print(restaurants_urls[i])

	rest_name = soup.h1.string
	neighborhood = soup.find('h1').next_sibling.contents[0].next_sibling.string
	avg_rating = soup.find('p', string=['REVIEW', 'REVIEWS']).previous_sibling.previous_sibling.string
	num_of_ratings = soup.find('p', string=['REVIEW', 'REVIEWS']).previous_sibling.string
	avg_cost = soup.find('h5', string='Average Cost').next_sibling.string
	cash_cards = soup.find('h5', string='More Info').previous_sibling.string
	target_div = soup.find('h1').next_sibling
	rest_type = target_div.find_all('a', title=True)
	rest_type = [typology.string for typology in rest_type]
	cuisines = target_div.find_all('a', title=False)
	cuisines = [cuisine.string for cuisine in cuisines]
	more_infos = soup.find('h5', string='More Info').next_sibling.find_all('p')
	more_infos = [info.string for info in more_infos]
	
	rest_data = {
	'ID' : i,
	'name' : rest_name,
	'neighborhood' : neighborhood,
	'avg_rating' : avg_rating,
	'#_of_ratings' : num_of_ratings,
	'avg_cost' : avg_cost,
	'cash_cards?' : cash_cards,
	'type' : rest_type,
	'cuisine' : cuisines,
	'more_infos' : more_infos
	}

	restaurants.append(rest_data, ignore_index=True)

print(restaurants)