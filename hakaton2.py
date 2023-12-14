'''

№ 2.

- **Цель**: Спарсить [mashina.kg,](https://www.mashina.kg/) разделив на категории:
    1. Название всех моделей.
    2. Цену всех моделей
    3. Изображение всех моделей
    4. Краткое описание всех моделей
    5. Записать все в csv файл
- 🛠 **Рекомендации**
    1. BeautifulSoup4
    2. csv
    3. requests
    
'''


from bs4 import BeautifulSoup as bs
import csv
import requests


def data_csv(data: dict):
    with open('data2.csv', 'w') as file:
        write = csv.writer(file)
        write.writerow((data['title'], data['price'], data['img']))

        
def get_html(url):
    response = requests.get(url)
    return response.text

def get_page(html):
    soup = bs(html, 'lxml')
    page_list = soup.find('div', class_='listing search-page x-3').find_all('div')
    last_page = page_list[-2].text
    return last_page


def get_data(html):
    soup = bs(html, 'lxml')
    cars = soup.find('div', class_='listing-item main')
    for car in cars:
        try:
            title = car.find('span', class_="white font-big").text.strip()
        except:
            title = ''
            
        try:
            price = car.find('span', class_='white custom-margins font-big').text
        except:
            price = ''
        
        try:
            img = car.find('img').get('src')
        except:
            img = ''

        data = {
            'title': title,
            'price': price,
            'image': img
        }
        data_csv(data)
        


def main():
    url = 'https://www.mashina.kg/new/search'
    html = get_html(url)
    number = int(get_page(html))
    i = 1
    while i <= number:
        url = f'https://www.mashina.kg/new/search{i}'
        html = get_html(url)
        get_data(html)
        if i == number:
            number = int(get_page(html))
        i += 1
    

with open('data2.csv', 'w') as file:
    write = csv.writer(file)
    write.writerow(['title ', 'price ', 'image '])


main()