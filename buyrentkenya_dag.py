from datetime import datetime
from airflow.decorators import dag, task
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.sqlite.hooks.sqlite import SqliteHook
import pandas as pd
from bs4 import BeautifulSoup
import requests
import sqlite3

default_args = {
    'owner': 'Hackathon',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

@dag(dag_id="Buy_Rent_Kenya_Dag", 
     description="Buy Rent Kenya Dag",
     schedule_interval="5 12 * * *", 
     start_date=datetime(2024, 2, 12),
     default_args=default_args,
     catchup=False)
def buy_rent_kenya_dag():
    create_table_sqlite_task = create_sqlite_task()
    scraping_task = scraping()
    store_to_db = storeNumber(scraping_task)

    create_table_sqlite_task >> scraping_task >> store_to_db

def create_sqlite_task():
    return SqliteOperator(
        task_id='create_table_sqlite',
        sql=r"""
        CREATE TABLE IF NOT EXISTS BuyRentKenyaHouses (
            house_id INTEGER PRIMARY KEY,
            title TEXT,
            location TEXT,
            bed_rooms INT,
            bath_rooms INT,
            price TEXT,
            description TEXT
        );
        """,
        sqlite_conn_id="sqlite"
    )

@task
def scraping():
    url = "https://www.buyrentkenya.com/houses-for-rent"
    agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"

    HEADERS = ({'User-Agent':agent,'Accept-Language':'en-US, en;q=0.5'})

    response = requests.get(url,headers=HEADERS)

    soup = BeautifulSoup(response.content,'html.parser')

    titles = []
    locations = []
    no_of_bathrooms = []
    no_of_bedrooms = []
    descriptions = []
    prices = []
    links= []

    houses = soup.find_all("div",class_="listing-card")
    for house in houses:
        title = house.find("span",class_="relative top-[2px] hidden md:inline").text.strip()
        location = house.find("p",class_="ml-1 truncate text-sm font-normal capitalize text-grey-650").text.strip()
        no_of_bedroom = house.find_all("span",class_="whitespace-nowrap font-normal")[0].text.strip()
        no_of_bathroom = house.find_all("span",class_="whitespace-nowrap font-normal")[1].text.strip()
        description = house.find("a",class_="block truncate text-grey-500 no-underline").text.strip()
        price = house.find("p",class_="text-xl font-bold leading-7 text-grey-900").text.strip()
        link = house.find("a",class_="text-black no-underline").get("href")

        titles.append(title)
        locations.append(location)
        no_of_bathrooms.append(no_of_bathroom)
        no_of_bedrooms.append(no_of_bedroom)
        descriptions.append(description)
        prices.append(price)
        links.append(link)

    print(f"The First Page No Of Titles is {len(titles)}")

    for page in range(2,64):
        url = f"https://www.buyrentkenya.com/houses-for-rent?page={page}"
        agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"

        HEADERS = ({'User-Agent':agent,'Accept-Language':'en-US, en;q=0.5'})

        response = requests.get(url,headers=HEADERS)
        print(url)
        houses = soup.find_all("div",class_="listing-card")
        for house in houses:
            title = house.find("span",class_="relative top-[2px] hidden md:inline").text.strip()
            location = house.find("p",class_="ml-1 truncate text-sm font-normal capitalize text-grey-650").text.strip()
            no_of_bedroom = house.find_all("span",class_="whitespace-nowrap font-normal")[0].text.strip()
            no_of_bathroom = house.find_all("span",class_="whitespace-nowrap font-normal")[1].text.strip()
            description = house.find("a",class_="block truncate text-grey-500 no-underline").text.strip()
            price = house.find("p",class_="text-xl font-bold leading-7 text-grey-900").text.strip()
            link = house.find("a",class_="text-black no-underline").get("href")

            titles.append(title)
            locations.append(location)
            no_of_bathrooms.append(no_of_bathroom)
            no_of_bedrooms.append(no_of_bedroom)
            descriptions.append(description)
            prices.append(price)   
            links.append(link) 

    print(f"The  Total no of Titles we have scraped is {len(titles)}")    

    data = {
        "Titles": titles,
        "Locations": locations,
        "No Of Bathrooms": no_of_bathrooms,
        "No Of Bedrooms": no_of_bedrooms,
        "Prices": prices,
        "Description": descriptions,
        "Link": links
    }
    df = pd.DataFrame(data)
    print(df.shape)
    df.to_csv("buy_rent_kenya_dag.csv",index=False)
    return data


@task
def storeNumber(data):
    conn =  sqlite3.connect("buyrentkenya.db")
    df = pd.DataFrame(data)
    df.to_sql("BuyRentKenyaHouses",conn,if_exists="replace",index=False)
    conn.close()

    
buy_rent_kenya_dag = buy_rent_kenya_dag()

