import requests
from bs4 import BeautifulSoup


user_agent_desktop = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '\
'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '\
'Safari/537.36'

headers = { 'User-Agent': user_agent_desktop}


url = 'https://www.camopedia.org/index.php?title=Main_Page'
reqs = requests.get(url, headers=headers)
soup = BeautifulSoup(reqs.text, 'html.parser')

urls = []
for link in soup.find_all('a'):
    print(link.get('href'))
