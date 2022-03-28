from django.shortcuts import render
from bs4 import BeautifulSoup
from django.http import HttpResponse
import requests
import json


# Create your views here.


def index(request):
    return render(request, 'index.html')


def get_keyword_books(request):
    return render(request, 'books.html', {
        'url': 'https://www.tenlong.com.tw/search',
        'keyword': request.POST['keyword']
    })


def get_ajax_books(request, ajax_id):
    req_params = json.loads(request.body)

    data = get_request_text(req_params['url'], {
        'keyword': req_params['keyword'],
        'page': req_params['page']
    })

    books = get_books(data) if ajax_id == 0 else get_sale_book(data)

    return HttpResponse(json.dumps(books))


def get_request_text(url, params=None):
    if params is None:
        params = {}
    req = requests.get(url, params=params)

    return req.text


def get_books(request_text):
    soup = BeautifulSoup(request_text, 'html.parser')
    prefix_url = 'https://www.tenlong.com.tw'
    books = []

    for book in soup.find('div', class_='search-result-list').find('ul').find_all('li'):
        book_div = book.find('div')
        book_data = {}

        try:
            book_img_url = book_div.find('a', class_='cover').find('img')
            book_detail_div = book_div.find('div', class_='book-data')

            book_detail = book_detail_div.find('strong').find('a')
            book_info = book_detail_div.find('ul', class_='item-info')
            book_basic = book_info.find('li', class_='basic')
            book_price = book_info.find('li', class_='pricing')

            book_data['img_url'] = book_img_url['src']
            book_data['name'] = book_detail.text
            book_data['url'] = prefix_url + book_detail['href']
            book_data['price'] = book_price.find('span', class_='price').text
            book_data['status'] = book_basic.find(
                'span', class_='publish-date').text
            books.append(book_data)
        except:
            pass

    return books


def get_sale_book(request_text):
    soup = BeautifulSoup(request_text, 'html.parser')
    books = []

    try:
        for book in soup.find('div', class_='list-wrapper').find('ul').find_all('li', class_='single-book'):
            book_data = {}

            book_name = book.find('strong', class_='title').find('a')
            book_img_url = book.find('a', class_='cover').find('img')['src']
            book_price = book.find('div', class_='pricing')
            book_url = book_name['href']

            book_data['name'] = book_name.text
            book_data['img_url'] = book_img_url
            book_data['url'] = 'https://www.tenlong.com.tw' + book_url
            book_data['price'] = book_price.text.replace('\n', '')
            books.append(book_data)

    except:
        pass

    return books


def get_sale_books(request, sale_id):
    sale_ids = [1127, 1126, 1125, 1124, 1123, 1122, 1121]
    prefix_url = f"https://www.tenlong.com.tw/special/{sale_ids[sale_id]}"

    return render(request, 'books.html', {
        'url': prefix_url
    })
