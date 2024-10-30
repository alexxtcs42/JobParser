import sqlite3
import random
import requests
from bs4 import BeautifulSoup
from lxml import html
from fake_useragent import UserAgent
import time


proxy_list = [{"http": "http://51.161.99.114:29758", "https": "https://51.161.99.114:29758"},
              {"http": "http://58.22.95.34:1080", "https": "https://58.22.95.34:1080"},
              {"http": "http://103.84.134.1:1080", "https": "https://103.84.134.1:1080"},
              {"http": "http://46.101.163.117:36587", "https": "https://46.101.163.117:36587"},
              {"http": "http://62.82.107.247:5678", "https": "https://62.82.107.247:5678"}]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Chrome/64.0.3282.186', }

url_login = "https://www.avito.ru/#login"
url_openings = "https://www.avito.ru/all/vakansii/razrabotcik-ASgBAgICAUTUzBGm~YoD"
url_resumes = "https://www.avito.ru/all/rezume/it_internet_telekom-ASgBAgICAUSUC~yeAQ?q=разработчик"
# url = "https://gdal.org/en/latest/index.html"

connection = sqlite3.connect('parser_database.db')

session = requests.session()
my_ip = "http://ident.me"
response_ip_1 = requests.get(my_ip)
print("ip address: ", response_ip_1.text)
time.sleep(2)
# proxy = random.choice(proxy_list)
proxy = {"http": "http://104.23.126.8:80", "https": "https://104.23.126.8:80"}
response_ip_2 = requests.get(my_ip)
print("ip address with proxy: ", response_ip_2.text)
session.proxies.update(proxy)
response = session.get(url_login, headers=headers)
session.headers.update({'Referer': url_login})
session.headers.update({'User-Agent':
                            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Chrome/64.0.3282.186'})
time.sleep(2)
_xsrf = session.cookies.get('_xsrf', domain=".avito.ru")
time.sleep(2)
post_request = session.post(url_login, {
     'backUrl': url_openings,
     'username': '+7 910 554-16-19',
     'password': 'JobParserHz_228',
     '_xsrf': _xsrf,
     'remember': 'yes',
})
if post_request.status_code == 200:
    soup = BeautifulSoup(post_request.text, 'html.parser')
    root = soup.html.body
    print(root.text)
else:
    print(f'error {post_request.status_code}')

connection.close()
