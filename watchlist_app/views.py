from django.shortcuts import render
from watchlist_app.models import Movie
from django.http import JsonResponse

def movie_list(request):
    movies = Movie.objects.all() # all the objects stored in a list in queryset
    print(movies)
    print(movies.values())
    data = {'movies' : list(movies.values())}
    return JsonResponse(data)
def movie_details(request,pk):
    movie = Movie.objects.get(pk=pk)
    data = {
        'name' : movie.name,
        'description' : movie.description,
        'active' : movie.active
    }
    return JsonResponse(data)