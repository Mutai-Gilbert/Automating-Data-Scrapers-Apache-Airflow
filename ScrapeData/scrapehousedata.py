import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import html


def extract(page):
    url = f'https://www.buyrentkenya.com/houses-for-rent?page={page}'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def transform(soup):
    divs = soup.find_all('div', class_='listing-card')
    joblist = []
    for item in divs:
        title_element = item.select_one('h2 a')
        location_element = item.select_one('div.flex.flex-wrap.gap-x-2.gap-y-1 div p')
        description_element = item.select_one('h5 a')
        price_element = item.select_one('div div div p a')

        title = title_element.text.strip() if title_element else "Title not found"
        location = location_element.text.strip() if location_element else "Location not found"
        description = description_element.text.strip() if description_element else "Description not found"
        price = price_element.text.strip() if price_element else "price not found"
        print(title, location, description, price)

        job = {
            'title': title,
            'location': location,
            'description': description,
            'price': price,
        }

        joblist.append(job)
    return joblist


pages = []
for i in range(0, 100, 10):
    c = extract(i)
    pages.append(transform(c))

df = pd.DataFrame(pages)
df.to_csv('jobs.csv')
