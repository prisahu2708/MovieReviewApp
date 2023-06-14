from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from watchlist_app.api import serializers
from watchlist_app import models

class StreamPlatform(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="example",password="password@123")
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(name="Netflix", about = "1 Platform",website="http://netflix.com")
    
    def test_platform_create(self):
        data = {
            "name": "Netflix",
            "about": "1 streaming platform",
            "website": "http://netflix.com"
        }
        response = self.client.post(reverse('stream'),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
    def test_platform_list(self):
        response = self.client.get(reverse('stream'))
        print(response.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK) 
    
    def test_platform_ind(self):
        response = self.client.get(reverse('streamdetail',args=(self.stream.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK) 

class WatchlistTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="example",password="password@123")
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(name="Netflix", about = "1 Platform",website="http://netflix.com")
        self.watchlist=models.WatchList.objects.create(platform=self.stream,title="Examplemovie",storyline="Example",active="True")
        
    
    def test_watchlist_create(self):
        data = {
            "platform":self.stream,
            "title":"example movie",
            "storyline":"example story",
            "active":True
            
        }
        response = self.client.post(reverse('movielist'),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
    def test_watchlist_list(self):
        response = self.client.get(reverse('movielist'))
        self.assertEqual(response.status_code,status.HTTP_200_OK) 
            
    def test_watchlist_ind(self):
        response = self.client.get(reverse('moviedetails',args=(self.watchlist.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK) 
        
class ReviewTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="example",password="password@123")
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(name="Netflix", about = "1 Platform",website="http://netflix.com")
        self.watchlist=models.WatchList.objects.create(platform=self.stream,title="Examplemovie",storyline="Example",active="True")
        self.watchlist2=models.WatchList.objects.create(platform=self.stream,title="Examplemovie",storyline="Example",active="True")
        self.review=models.Review.objects.create(review_user=self.user,rating=5,description="GreatMovie",watchlist=self.watchlist2)
        
    def test_review_create(self):
        data = {
            "review_user":self.user,
            "rating":5,
            "description":"great movie",
            "watchlist":self.watchlist,
        }
        response = self.client.post(reverse('reviewcreate',args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        
        response = self.client.post(reverse('reviewcreate',args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_review_update(self):
        data = {
            "review_user":self.user,
            "rating":4,
            "description":"great movie",
            "watchlist":self.watchlist2,
        }
        response = self.client.put(reverse('reviewdetail',args=(self.review.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)  
           
           
               
    
                  
        
