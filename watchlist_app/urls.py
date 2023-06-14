from django.urls import path,include
from watchlist_app.views import movie_list,movie_details
urlpatterns = [
    path("list/",movie_list,name='movielist'),
    path('<int:pk>',movie_details,name='moviedetail'),
]