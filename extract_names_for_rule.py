import requests
from bs4 import BeautifulSoup

URL = "https://script.spoken-tutorial.org"
MAIN_PAGE = "/index.php/Main_Page"

page = requests.get(URL+MAIN_PAGE)
soup = BeautifulSoup(page.content, "html.parser")

elements = [sp.find('a') for sp in soup.find_all('p')]
links = []
for element in elements:
    if element is not None:
        link = element.attrs['href']
        if link.startswith('/index.php/'):
            links.append(link)
links = links[2:]
for link in links:
    print(link)
    current_page = requests.get(URL+link)
    current_soup = BeautifulSoup(current_page.content, "html.parser")
    print(''.join([ele.get_text() for ele in current_soup.find_all('p')]))
    break
# print('\n'.join(links))
