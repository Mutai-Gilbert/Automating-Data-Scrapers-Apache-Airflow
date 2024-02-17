import pandas as pd
from bs4 import BeautifulSoup
import requests

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
print(links)

# for page in range(2,56):
#     url = f"https://www.buyrentkenya.com/houses-for-rent?page={page}"
#     agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"

#     HEADERS = ({'User-Agent':agent,'Accept-Language':'en-US, en;q=0.5'})

#     response = requests.get(url,headers=HEADERS)
#     print(url)
#     houses = soup.find_all("div",class_="listing-card")
#     for house in houses:
#         title = house.find("span",class_="relative top-[2px] hidden md:inline").text.strip()
#         location = house.find("p",class_="ml-1 truncate text-sm font-normal capitalize text-grey-650").text.strip()
#         no_of_bedroom = house.find_all("span",class_="whitespace-nowrap font-normal")[0].text.strip()
#         no_of_bathroom = house.find_all("span",class_="whitespace-nowrap font-normal")[1].text.strip()
#         description = house.find("a",class_="block truncate text-grey-500 no-underline").text.strip()
#         price = house.find("p",class_="text-xl font-bold leading-7 text-grey-900").text.strip()
        
#         titles.append(title)
#         locations.append(location)
#         no_of_bathrooms.append(no_of_bathroom)
#         no_of_bedrooms.append(no_of_bedroom)
#         descriptions.append(description)
#         prices.append(price)    
        
# print(f"The  Total no of Titles we have scarped is {len(titles)}")    

   
# data = {
#     "Titles": titles,
#     "Locations": locations,
#     "No Of Bathrooms": no_of_bathrooms,
#     "No Of Bedrooms": no_of_bedrooms,
#     "Prices": prices,
#     "Description": descriptions
# }
# df = pd.DataFrame(data)
# print(df.shape)
# #print(df.head(10))
# df.to_csv("buy_rent_kenya.csv",index=False)
