from datetime import datetime

from django.shortcuts import HttpResponse
from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, "index.html")


def baidu(request):
    return render(request, "baidu.html")


def info(request):
    # 1.普通变量
    username = 'bosch'
    book = [
        {'name': '水浒传', 'author': '施耐庵'},
        {'name': '三国演义', 'author': '罗贯中'}
    ]

    class Person:
        def __init__(self, real_name, real_age):
            self.real_name = real_name
            self.real_age = real_age

        def to_dict(self):
            return self.__dict__

    persons = [
        Person('bosch', 25),
        Person('mike', 29)
    ]

    persons_dicts = [
        person.to_dict()
        for person in persons
    ]
    contexts = {
        'username': username,
        'book': book,
        'persons': persons_dicts
    }

    return render(request, "info.html", context=contexts)


def if_view(request):
    age = 13
    return render(request, "if.html", context={'age': age})


def with_view(request):
    books = [
        {'name': '水浒传', 'author': '施耐庵'},
        {'name': '三国演义', 'author': '罗贯中'}
    ]
    contexts = {
        "books": books
    }
    return render(request, "with.html", context=contexts)


def url_view(request):
    return render(request, "url.html")


def book_detail(requset, book_id):
    return HttpResponse(f"你访问的图书ID是: {book_id}")


def filter_view(request):
    greet = 'hello django'
    date = datetime.now()
    context = {
        'greet': greet,
        'datetime': date,
        'profile': "你看我行不行就可以了",
        'value': [0, 1, 2, 3, 4],
        'html': "<h1>欢迎来到BOSCH</h1>"
    }
    return render(request, "filter.html", context=context)
