from rest_framework import serializers
from watchlist_app.models import WatchList,StreamPlatform,Review

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        #fields = "__all__"
        exclude = ('watchlist',)
        
class WatchListSerializer(serializers.ModelSerializer):
    #reviews = ReviewSerializer(many=True,read_only= True)
    platform = serializers.CharField(source='platform.name')
    class Meta:
        model = WatchList
        fields = "__all__"

class StreamPlatformSerializer(serializers.ModelSerializer):
    #watchlist = WatchListSerializer(many=True,read_only=True)    #1 platform has many movies get all movies
    #watchlist = serializers.StringRelatedField(many=True)   #return only what is defined in __str__
    #watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  #primary key only present
    watchlist = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='moviedetails'
    )
    class Meta:
        model = StreamPlatform
        fields = "__all__"        

# class MovieSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Movie
#         fields = "__all__"
#         #fields = ['id','name','description']
#         #exclude = ['active']
#     def validate(self,data):   #obj level validation
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("both should be diff")
#         else:
#             return data
#     def validate_name(self,value): #field level validation
        
#         if len(value) < 2:
#             raise serializers.ValidationError("name is too short")
#         else:
#             return value    
        

# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("name is too short")
    

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
    
#     def create(self,validated_data):
#         return Movie.objects.create(**validated_data)
#     def update(self,instance,validated_data):
#         instance.name = validated_data.get('name',instance.name)
#         instance.description = validated_data.get('description',instance.description)
#         instance.active = validated_data.get('active',instance.active)
#         instance.save()
#         return instance
#     def validate(self,data):   #obj level validation
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("both should be diff")
#         else:
#             return data
    # def validate_name(self,value): #field level validation
        
    #     if len(value) < 2:
    #         raise serializers.ValidationError("name is too short")
    #     else:
    #         return value