#This script scrapes https://github.com/clarketm/proxy-list/blob/master/proxy-list.tx to get
#up-to-date proxies
#Needs to be run before spider

import bs4, requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
url = "https://github.com/clarketm/proxy-list/blob/master/proxy-list.txt"
r = requests.get(url, headers=headers)
r

soup = BeautifulSoup(r.content, "html.parser")
list_ips=[]

proxy_list = open("proxy-list.txt", "w")

for i in range(10,410):
    charac="LC"+str(i)
    ips = soup.find_all("td", {"id": charac})
    ips_ip=ips[0].text.split()[0]
    proxy_list.write(ips_ip + "\n")

proxy_list.close()