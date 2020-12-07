from django.shortcuts import render
from bs4 import BeautifulSoup
from django.http import HttpResponse
import requests
import json


# Create your views here.


def index(request):
    return render(request, 'index.html')


def get_keyword_books(request):
    request_text = get_request_text(request.POST['keyword'])

    data = get_books(request_text)

    return render(request, 'books.html', {
        'books': data,
        'keyword': request.POST['keyword']
    })


def get_ajax_books(request):
    json_data = json.loads(request.body)
    data = get_request_text(json_data['keyword'], json_data['page'])
    books = get_books(data)

    return HttpResponse(json.dumps(books))


def get_request_text(keyword, page=1):
    req = requests.get(f'https://www.tenlong.com.tw/search', params={
        'keyword': keyword,
        'page': page
    })

    return req.text


def get_books(request_text):
    soup = BeautifulSoup(request_text, 'html.parser')
    prefix_url = 'https://www.tenlong.com.tw'
    books = []

    for book in soup.find('div', class_='search-result-list').find('ul').find_all('li', class_=lambda x: x != 'promo'):
        book_img_url = book.find('a', class_='cover')
        book_detail_div = book.find('div', class_='book-data')

        try:
            book_data = {}
            book_img = book_img_url.find('img')
            book_detail = book_detail_div.find('strong').find('a')
            book_basic = book_detail_div.find(
                'ul', class_='item-info').find('li', class_='basic')
            book_price = book_detail_div.find(
                'ul', class_='item-info').find('li', class_='pricing')
            book_basic_list = ['lang', 'author', 'category', 'publish-date']

            for index, x in enumerate(book_basic_list):
                if((index + 1) == len(book_basic_list)):
                    book_data['publish_date'] = book_basic.find(
                        'span', class_=x).text
                else:
                    book_data[x] = book_basic.find('span', class_=x).text

            book_data['img_url'] = book_img['src']
            book_data['name'] = book_detail.text
            book_data['url'] = prefix_url + book_detail['href']
            book_data['price'] = book_price.find('span', class_='price').text
            book_data['status'] = book_price.find('span', class_='status').text
            books.append(book_data)
        except:
            pass

    return books
