from django.urls import path,include
#from watchlist_app.api.views import movie_list,movie_details
from watchlist_app.api.views import StreamPlatformAV,WatchListAV,ReviewList,WatchDetailAV,StreamPlatformDetailAV,ReviewDetail,ReviewCreate,UserReview,Watchlist
urlpatterns = [
    #path("list/",movie_list,name='movielist'),
    path('<int:pk>',WatchDetailAV.as_view(),name='moviedetails'),
    path('list2/',Watchlist.as_view(),name = 'movielist'),
    path('list/',WatchListAV.as_view(),name='movielist'),
    path('stream/',StreamPlatformAV.as_view(),name='stream'),
    path('stream/<int:pk>',StreamPlatformDetailAV.as_view(),name='streamdetail'),
    path('<int:pk>/review-create/',ReviewCreate.as_view(),name='reviewcreate'),  #for particular movieid create review
    path('<int:pk>/review/',ReviewList.as_view(),name='reviewlist'), # get review for a particular movie id
    #path('review/',ReviewList.as_view(),name='reviewlist'),   # get all the reviews
    path('review/<int:pk>',ReviewDetail.as_view(),name='reviewdetail'),
    #path('review/<str:username>',UserReview.as_view(),name='user-reviewdetail'),
    path('review/',UserReview.as_view(),name='user-reviewdetail'),   #filtering using query parameter
]