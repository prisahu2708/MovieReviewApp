from watchlist_app.models import WatchList,StreamPlatform,Review
from watchlist_app.api.serializers import WatchListSerializer,StreamPlatformSerializer,ReviewSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from watchlist_app.api.permissions import IsAdminOrReadOnly,ReviewUserOrReadOnly
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle,ScopedRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottle,ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from watchlist_app.api.pagination import WatchlistPagination,WatchlistLOPagination

class UserReview(generics.ListAPIView):   #find reviews for a particular user (filtering by passing value)
    serializer_class = ReviewSerializer
    def get_queryset(self):
    
        username =self.kwargs['username']         
        return Review.objects.filter(review_user__username=username)  #review user is FK field so to access username use__
    def get_queryset(self):    #filtering by passing query parameter      
        username = self.request.query_params.get('username')   #passing query parameter
        return Review.objects.filter(review_user__username=username) 
    
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self,serializer):   #to overwrite create method for adding review for a particular movie
        pk = self.kwargs.get('pk') #1st access to pk sent in url(target movie 1 if pk = 1)
        movie = WatchList.objects.get(pk=pk) #find that movie
        user_ = self.request.user   #current loggedin user
        review_queryset = Review.objects.filter(watchlist=movie,review_user=user_)
        if review_queryset.exists():
            raise ValidationError("Already reviewed this movie")
        
        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating+serializer.validated_data['rating'])/2
            
        movie.number_rating = movie.number_rating + 1 
        movie.save()       
        serializer.save(watchlist=movie,review_user =user_)   #we have to inform serializer about movie and user as we r not giving this data
# class ReviewCreate(generics.CreateAPIView): #create review for a particular movie
#     serializer_class = ReviewSerializer
#     def perform_create(self,serializer):   #to overwrite create method for adding review for a particular movie
#         pk = self.kwargs.get('pk') #1st access to pk sent in url(target movie 1 if pk = 1)
#         movie = WatchList.objects.get(pk=pk) #find that movie
#         print(type(movie))
        
#         serializer.save(watchlist=movie)

class ReviewList(generics.ListAPIView):   
    #queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewListThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'rating']
    def get_queryset(self):   #overwrite queryset to get reviews for a particular movie
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)      #watchlist defined in model as foreignkey
        
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView): 
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'
    
    

    

# class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)    #retrieve single element(here we performed get req cant update it)


# class ReviewList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class StreamPlatformAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request):
        platform = StreamPlatform.objects.all()
        
        #serializer = StreamPlatformSerializer(platform,many = True)
        serializer = StreamPlatformSerializer(platform,many = True,context={'request': request})   # hyperlinkedrelated field
        return Response(serializer.data)
        
    def post(self,request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request,pk):
        try:
            platform = StreamPlatform.objects.get(pk = pk)
        except StreamPlatform.DoesNotExist:        #if particular id is not found
            return Response({'Error': 'Not found'},status=status.HTTP_404_NOT_FOUND)    
        serializer = StreamPlatformSerializer(platform)   #single obj
        return Response(serializer.data,status=status.HTTP_200_OK)  
    def put(self,request,pk):
        platform = StreamPlatform.objects.get(pk = pk)
        serializer = StreamPlatformSerializer(platform,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors) 
class Watchlist(generics.ListAPIView):   
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'platform__name'] 
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['avg_rating']
    pagination_class = WatchlistLOPagination
                  

class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies,many=True) #multiple objs
        print(type(serializer))
        print(serializer.data)
        return Response(serializer.data)
    def post(self,request):
        serializer = WatchListSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request,pk):
        try:
            movie = WatchList.objects.get(pk = pk)
        except WatchList.DoesNotExist:        #if particular id is not found
            return Response({'Error': 'Movie not found'},status=status.HTTP_404_NOT_FOUND)    
        serializer = WatchListSerializer(movie)   #single obj
        return Response(serializer.data,status=status.HTTP_200_OK)  
    def put(self,request,pk):
        movie = WatchList.objects.get(pk = pk)
        serializer = WatchListSerializer(movie,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors)    

# class MovieListAV(APIView):
#     def get(self,request):
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies,many=True)   #multiple objs
#         print(serializer)
#         print(serializer.data)
#         return Response(serializer.data)
#     def post(self,request):
#         serializer = MovieSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
            
        

# @api_view(['GET','POST'])
# def movie_list(request):
    
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies,many=True)  #multiple objs
#         return Response(serializer.data)
#     if request.method == 'POST':
#         serializer = MovieSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
            
        
        
# @api_view(['GET','PUT','DELETE'])
# def movie_details(request,pk):
#     if request.method == 'GET':
        
#         try:
#             movie = Movie.objects.get(pk = pk)
#         except Movie.DoesNotExist:        #if particular id is not found
#             return Response({'Error': 'Movie not found'},status=status.HTTP_404_NOT_FOUND)    
#         serializer = MovieSerializer(movie)   #single obj
#         return Response(serializer.data,status=HTTP_200_OK)
#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk = pk)
#         serializer = MovieSerializer(movie,data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status = status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(serializer.errors)
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)    
        
    