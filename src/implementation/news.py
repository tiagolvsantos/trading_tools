from  bs4 import BeautifulSoup
import requests

url = "https://seekingalpha.com/market-news"
page = requests.get(url)
soup = BeautifulSoup(page.text)

news = soup.find(name="ul", attrs={'class':"item-list",'id':'latest-news-list'})
root = "https://seekingalpha.com"
id_list = [i['id'] for i in news.find_all(name='li', attrs={'class':'item'})]
heading_list = [i.text for i in news.find_all('a')]
url_list = [root+i['href'] for i in news.find_all('a')]
date_list = [i['data-last-date'] for i in news.find_all(name='li', attrs={'class':'item'})]
date_list2 = [i.split()[0] for i in date_list]
id_list2 = [i.split('-')[2] for i in id_list]