from bs4 import BeautifulSoup as bs
import csv
import requests

def write_to_csv(data: dict):
    with open('data.csv', 'a') as file:
        write = csv.writer(file)
        write.writerow((data['title'], data['price'], data['img'], data['descr']))


def get_html(url):
    response = requests.get(url)
    return response.text



def get_page(html):
    soup = bs(html, 'lxml')
    page_list = soup.find('div', class_='pages fl').find_all('a')
    last_page = page_list[-2].text
    return last_page



def get_data(html):
    soup = bs(html, 'lxml')
    cars = soup.find('div', class_ = 'catalog-list').find_all('a')
    for car in cars:
        try:
            title = car.find('span', class_="catalog-item-caption").text.strip()
        except:
            title = ''
        
        try:
            price = car.find('span', class_="catalog-item-price").text
        except:
            price = ''

        try:
            descr = car.find('span', class_='catalog-item-descr').text.split()
            descr = ' '.join(descr)
        except:
            descr = ''

        try:
            img = car.find('img').get('src')
        except:
            img = ''


        data = {
            'title': title,
            'price': price,
            'img': img,
            'descr': descr
        }

        write_to_csv(data)




def main():
    url = 'https://cars.kg/offers'
    html = get_html(url)
    number = int(get_page(html))
    i = 1
    while i <= number:
        url = f'https://cars.kg/offers/{i}'
        html = get_html(url)
        get_data(html)
        if i == number:
            number = int(get_page(html))
        i += 1




with open('data.csv', 'w') as file:
    write = csv.writer(file)
    write.writerow(['title ', 'price ', 'image ', 'description'])


main()