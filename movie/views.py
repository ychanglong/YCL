from django.shortcuts import HttpResponse


def movie_list(request):
    return HttpResponse("电影列表")

def movie_detail(request,movie_id):
    return HttpResponse(f"你获取的电影id是： {movie_id}")
