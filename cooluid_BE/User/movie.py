# 표준 라이브러리 모듈을 import
from pathlib import Path

# 서드파티 패키지 또는 라이브러리를 import
import requests
from django.core.exceptions import ImproperlyConfigured
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# 로컬 프로젝트 또는 애플리케이션에서 정의한 모듈을 import
from .models import Movie
from .serializers import MovieSerializer


def fetch_movie_data(title, director, nation):
    url = "http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?collection=kmdb_new2" \
          "&ServiceKey=K43I6OH5P50NYLDC901V"

    params = {
        'title': title,
        'director': director,
        'nation': nation
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None 


@api_view(['GET'])
def movie_list(request):
    data = fetch_movie_data(request.data.get('title'), request.data.get('director'), request.data.get('nation'))

    if data:
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response('Failed to fetch movie data', status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def search_movie(request):
    title = request.data.get('title')
    director = request.data.get('director')
    nation = request.data.get('nation')

    try:
        movie = Movie.objects.get(title=title, director=director, nation=nation)
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Movie.DoesNotExist:
        pass

    movie_data = fetch_movie_data(title, director, nation)
    if movie_data:
        return Response(movie_data, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)