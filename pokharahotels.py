import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import csv

def get_soup(url):
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    return soup(page_html,"html.parser")

def get_pagenumber(url):
    page_soup = get_soup(url)
    pagenumber = page_soup.find(class_="unified ui_pagination standard_pagination ui_section listFooter").get("data-numpages")
    return pagenumber


page_number = get_pagenumber("https://www.tripadvisor.com/Hotels-g293891-Pokhara_Gandaki_Zone_Western_Region-Hotels.html")
page_urls = []
for page in range(1,int(page_number)):
    if page == 1:
        page_urls.append("https://www.tripadvisor.com/Hotels-g293891-Pokhara_Gandaki_Zone_Western_Region-Hotels.html")
    else:
        page_url= "https://www.tripadvisor.com/Hotels-g293891-oa{}-Pokhara_Gandaki_Zone_Western_Region-Hotels.html".format(page * 30)
        page_urls.append(page_url)

hotel_urls = []

for page_url in page_urls:
    page_soup = get_soup(page_url)
    for items in page_soup.find_all(class_="photo-wrapper"):
            url = "https://www.tripadvisor.com{}".format(items.a["href"])
            hotel_urls.append(url)
            print(url)

hotel_list=[]
for hotel_url in hotel_urls:
    page_soup = get_soup(hotel_url)
    url = hotel_url
    title = page_soup.find(class_="hotels-hotel-review-atf-info-parts-Heading__heading--2ZOcD").get_text()
    address = page_soup.find(class_="public-business-listing-ContactInfo__ui_link--1_7Zp public-business-listing-ContactInfo__level_4--3JgmI").get_text()
    price = page_soup.find(class_="hotels-hotel-offers-DominantOffer__price--D-ycN")
    phone = page_soup.find(class_="public-business-listing-ContactInfo__nonWebLinkText--nGymU public-business-listing-ContactInfo__ui_link--1_7Zp public-business-listing-ContactInfo__level_4--3JgmI")
    if phone:
        phone = phone.get_text()
    else:
        phone = "Not Found"
    if price:
        price = price.get_text()
    else:
        price = "Not Found"
    hotel = [title,url,address,phone,price]
    print(hotel)
    hotel_list.append(hotel)

with open('hotelsPokhara.csv','w') as file:
    writer = csv.writer(file)
    writer.writerow(['title','url','address','phone','price'])
    writer.writerows(hotel_list)
