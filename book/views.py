from django.shortcuts import HttpResponse
from django.shortcuts import render


# Create your views here.

# 通过查询字符串 (query string)
# path中携带

# 127.0.0.1:8000/book?id=1
def book_detail_query_string(request):
    book_id = request.GET['id']
    return HttpResponse(f'book is : {book_id}')


def book_detail_path(request,book_id):
    return HttpResponse(f'book is : {book_id}')

def book_detail_str(request,book_id):
    return HttpResponse(f'book is : {book_id}')
