import requests
from bs4 import BeautifulSoup

def get_url(field):
    template = f'https://www.cbsnews.com/{field}/'
    return template

def scrape_cbs(fields, source='cbs'):
    urls = [get_url(field) for field in fields]
    response = [requests.get(url) for url in urls]
    soup = [BeautifulSoup(res.text, 'html.parser') for res in response]
    cards = [r.find_all('article', class_='item--type-article') for r in soup]

    data_list = []
    for category, card in zip(fields, cards):
        for c in card[:]:
            title = c.find('h4', class_="item__hed").get_text(strip=True)
            url = c.find('a', class_="item__anchor").get('href')
            time = c.find('li', class_="item__date").get_text()
            data = {
                'source': source,
                'title': title,
                'url': url,
                'time': time,
                'category': category
            }
            data_list.append(data)
    
    return data_list
