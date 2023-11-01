from rest_framework import serializers
from .models import User, Movie, Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("custom_user_id", "email", "about")

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("title", "director", "nation")

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'