from django.shortcuts import render
from bs4 import BeautifulSoup
from django.http import HttpResponse
import requests


# Create your views here.


def index(request):
    return render(request, 'index.html')


def test(request):
    req = requests.get(f'https://www.tenlong.com.tw/search', params={
        'keyword': request.GET['keyword']
    })
    soup = BeautifulSoup(req.text, 'html.parser')
    prefix_url = 'https://www.tenlong.com.tw'
    books = []

    for book in soup.find('div', class_='search-result-list').find('ul').find_all('li', class_= lambda x: x != 'promo'):
        book_img_url = book.find('a', class_='cover')
        book_detail_div = book.find('div', class_='book-data')

        try:
            book_data = {}
            book_img = book_img_url.find('img')
            book_detail = book_detail_div.find('strong').find('a')
            book_basic = book_detail_div.find('ul', class_='item-info').find('li', class_='basic')
            book_price = book_detail_div.find('ul', class_='item-info').find('li', class_='pricing')
            book_basic_list = ['lang', 'author', 'category', 'publish-date']

            for index, x in enumerate(book_basic_list):
                if((index + 1) == len(book_basic_list)):
                    book_data['publish_date'] = book_basic.find('span', class_=x).text
                else:
                    book_data[x] = book_basic.find('span', class_=x).text

            book_data['img_url'] = book_img['src']
            book_data['name'] = book_detail.text
            book_data['url'] = prefix_url + book_detail['href']
            book_data['price'] = book_price.find('span', class_='price').text
            book_data['status'] = book_price.find('span',class_='status').text
            books.append(book_data)
        except:
            pass

    return render(request, 'books.html', {
        'books': books
    })
