import requests
from bs4 import BeautifulSoup as bs


URL = 'https://www.kivano.kg/mobilnye-telefony'


def get_html(url):
    respons = requests.get(url)
    return respons.text


def get_page_data(html):
    soup = bs(html, 'html.parser')
    body = soup.find_all('div', class_='item product_listbox oh')
    data = []
    for i in body:
        name = i.find('strong').text
        price = i.find('div', class_='listbox_price').find('strong').text
        image = i.find('div', class_='listbox_img pull-left').find('img').get('src')
        description = i.find('div', class_='product_text pull-left').text
        product = [name, price.split(' ')[0], 'https://www.kivano.kg/'+image, description]
        data.append(product)

    return data