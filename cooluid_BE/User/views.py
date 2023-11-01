from django.contrib.sessions.models import Session
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.shortcuts import redirect

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from pathlib import Path
import requests
from django.core.exceptions import ImproperlyConfigured

from .utils.mail import send_code_mail_signup, send_code_mail_signin
from .utils.util import generate_code
from .models import RegistrationCode, EmailSignInCode, User, Movie, Post
from .serializers import UserSerializer, MovieSerializer, PostSerializer


def get_posts(request):
    posts = Post.objects.all() 
    data = [{'id': post.id, 'title': post.title, 'content': post.content, 'posterUrl' : post.posterurl} for post in posts]

    return JsonResponse(data, safe=False)

class SendMailSignUp(APIView):
    def post(self, request):
        email = request.data.get('email')
        if email:
            code = generate_code()
            send_code_mail_signup(email, code=code)

            registration_code = RegistrationCode(email=email, code=code)
            registration_code.save()

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class CreatePostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class SendMailSignIn(APIView):
    def post(self, request):
        email = request.data.get('email')
        if email:
            code = generate_code()
            send_code_mail_signin(email, code=code)

            email_signin_code = EmailSignInCode(email=email, code=code)
            email_signin_code.save()

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


def get_email_by_code(request):
    code = request.GET.get('code')
    try:
        register_code = RegistrationCode.objects.get(code=code)
        email = register_code.email
        return JsonResponse({'email': email})
    except RegistrationCode.DoesNotExist:
        return JsonResponse({'error': 'Code not found'}, status=404)


def email_signin(request):
    code = request.GET.get('code')
    try:
        email_signin_code = EmailSignInCode.objects.get(code=code)
        email = email_signin_code.email
        try:
            user = User.objects.get(email=email)
            if register_or_login_user(request, user):
                return JsonResponse({'success': True, 'message': 'Authentication successful'})
            else:
                return JsonResponse({'success': False, 'message': 'User is already authenticated'})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Please complete the registration process'})
    except EmailSignInCode.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Invalid access'})


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            print("serializer:",serializer)
            user = serializer.save()
            success = register_or_login_user(request, user)
            if success:
                return Response({"success": True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def register_or_login_user(request, user):
    if not request.user.is_authenticated:
        request.session.create()
        request.session["custom_user_id"] = user.custom_user_id
        request.session.save()
        login(request, user)
        return True
    return False



@api_view(['POST'])
def logout_view(request):
    print(request)
    logout(request)
    print("여기까지 옴 12121")
    return JsonResponse({'message': '로그아웃 성공'})

# def check_login_status(request):
#     if request.user.is_authenticated:
#         user_data = {
#             'username': request.user.custom_user_id,
#             'email': request.user.email,
#             'is_staff': request.user.is_staff,
#         }
#         return JsonResponse({'user': user_data})
#     else:
#         return JsonResponse({'user': None})


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
def check_session(request):
    if request.session.get('custom_user_id'):
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
    


def fetch_movie_data(title, director, nation):
    print("fetch_movie_data 들어옴")
    url = "http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?collection=kmdb_new2" \
          "&ServiceKey=K43I6OH5P50NYLDC901V"

    params = {
        'title': title,
        'director': director,
        'nation': nation
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        print("fetch_movie_data 정상처리로 들어옴")
        data = response.json()
        extracted_data = extract_movie_info(data)
        return extracted_data
        
    else:
        print("fetch_movie_data else로 들어옴")
        return None 


@api_view(['GET'])
def movie_list(request):
    data = fetch_movie_data(request.data.get('title'), request.data.get('director'), request.data.get('nation'))

    if data:
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response('Failed to fetch movie data', status=status.HTTP_400_BAD_REQUEST)

def extract_movie_info(data):
    movie_list = []

    for result in data['Data'][0]['Result']:
        # Remove !HS and !HE from title
        title = result['title'].replace('!HS', '').replace('!HE', '')

        # Split poster URLs by '|', take the first one if available
        poster_urls = result.get('posters', '').split('|')
        poster_url = poster_urls[0] if poster_urls else ''

        movie_info = {
            'movieId': result['movieId'],
            'title': title.strip(),
            'titleEng': result.get('titleEng', ''),  # Some entries might not have titleEng
            'titleOrg': result.get('titleOrg', ''),  # Some entries might not have titleOrg
            'directorNm': result['directors']['director'][0]['directorNm'],  # Assuming there's at least one director
            'posterUrl': poster_url,
        }
        print(movie_info)
        movie_list.append(movie_info)

    return movie_list

@api_view(['POST'])
def search_movie(request):
    print("search_moive 들어옴")
    title = request.data.get('title')
    director = request.data.get('director')
    nation = request.data.get('nation')

    try:
        print("search_moive try 들어옴")
        movie = Movie.objects.get(title=title, director=director, nation=nation)
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Movie.DoesNotExist:
        print("search_moive except 들어옴")
        pass

    movie_data = fetch_movie_data(title, director, nation)
    if movie_data:
        print("search_moive if 첫번째 들어옴")
        return Response(movie_data, status=status.HTTP_200_OK)
    else:
        print("search_moive else 첫번째 들어옴")
        return Response({'message': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)