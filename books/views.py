from django.shortcuts import render
from bs4 import BeautifulSoup
from django.http import HttpResponse
import requests


# Create your views here.


def index(request):
    return render(request, 'index.html')


def test(request):
    req = requests.get(f'https://www.tenlong.com.tw/search', params={
        'keyword': request.POST['keyword']
    })
    soup = BeautifulSoup(req.text, 'html.parser')
    img_prefix_url = 'https://www.tenlong.com.tw'
    books = []

    for book in soup.find('div', class_='search-result-list').find('ul').find_all('li', class_=lambda x: x != 'promo'):
        book_data = {
            'name': '',
            'url': '',
            'img_url': ''
        }
        book_img_url = book.find('a', class_='cover')

        if(book_img_url is not None):
            book_img = book_img_url.find('img')
            book_data['name'] = book_img['alt'][:len(book_img['alt']) - 6]
            book_data['url'] = img_prefix_url + book_img_url['href']

            if('src' in book_img.attrs):
                book_data['img_url'] = book_img['src']
            books.append(book_data)

    return render(request, 'books.html', {
        'books': books
    })
