from os import environ
import os
import requests
from django.shortcuts import get_object_or_404, redirect
from rest_framework import authentication, viewsets
from rest_framework import serializers
from rest_framework.decorators import api_view
from accounts.models import User
from rest_framework.response import Response
from rest_framework.permissions import *
from django.conf import settings
from accounts.serializers import UserInfo
from allauth.socialaccount.models import SocialAccount
from articles.models import Review
from bobfull.settings import BASE_DIR
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse
from rest_framework import status
from json.decoder import JSONDecodeError
from rest_framework_simplejwt.authentication import JWTAuthentication
from restaurant.models import RestaurantLike

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class UserViewSet(viewsets.ModelViewSet):
    # authentication_classes = [JWTAuthentication]
    # 관리자만 전체 유저 정보 볼 수 있게
    # permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

# 기본 설정
BASE_URL = 'https://bobfull-backend.shop/'
GOOGLE_CALLBACK_URI = BASE_URL + 'accounts/google/callback/'
KAKAO_CALLBACK_URI = BASE_URL + 'accounts/kakao/callback/'

# state = getattr(settings, 'STATE')
state = os.getenv("STATE")

# 구글 로그인
# google_login 실행
def google_login(request):
    """
    Code Request
    """
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = os.getenv("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")

# 받은 Code로 Google에 Access Token 요청
def google_callback(request):
    client_id = os.getenv("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = os.getenv("SOCIAL_AUTH_GOOGLE_SECRET")
    code = request.GET.get('code')
    """
    Access Token Request
    """
    GOOGLE_CALLBACK_URI_FRONT = 'https://master.d3n2xysrd0lvj9.amplifyapp.com/accounts/google/callback/'
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI_FRONT}&state={state}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get('access_token')

    # Access Token으로 Email 값을 Google에게 요청
    """
    Email Request
    """
    email_req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code
    if email_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
    email_req_json = email_req.json()
    email = email_req_json.get('email')

    # 전달받은 Email, Access Token, Code를 바탕으로 회원가입/로그인 진행
    """
    Signup or Signin Request
    """
    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'google':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        # 기존에 Google로 가입된 유저
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/google/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()
        return JsonResponse(accept_json)
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/google/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        accept_json = accept.json()
        return JsonResponse(accept_json)

class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client

# 카카오
def kakao_login(request):
    rest_api_key = os.getenv("KAKAO_REST_API_KEY")
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )

def kakao_callback(request):
    rest_api_key = os.getenv("KAKAO_REST_API_KEY")
    code = request.GET.get("code")
    redirect_uri = "https://master.d3n2xysrd0lvj9.amplifyapp.com/oauth/callback/kakao"
    """
    Access Token Request
    """
    token_req = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")
    """
    Email Request
    """
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
    profile_json = profile_request.json()
    kakao_account = profile_json.get('kakao_account')
    """
    kakao_account에서 이메일 외에
    카카오톡 프로필 이미지, 배경 이미지 url 가져올 수 있음
    print(kakao_account) 참고
    """
    # print(kakao_account)
    email = kakao_account.get('email')
    """
    Signup or Signin Request
    """
    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 kakao가 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'kakao':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        # 기존에 Google로 가입된 유저
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()
        return JsonResponse(accept_json)
        
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
        accept_json = accept.json()
        print(accept_json)  
        return JsonResponse(accept_json)

class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI

# 유저 페이지 확인 (유저정보 및 유저 작성한 글 확인 )
@api_view(["GET", "PUT"])
def my_page(request, user_pk):
    user_info = get_object_or_404(User, pk=user_pk)
    if request.method == "GET" and user_pk == request.user.pk:
        serializers = UserInfo(user_info)
        user_restaurant_likes = RestaurantLike.objects.filter(user_id=request.user)
        user_reviews = Review.objects.filter(user=request.user)
        restaurant_datas = []
        # print(user_restaurant_likes[0].restaurant.name)
        # 좋아요 데이터 넣기
        for restaurant in user_restaurant_likes:
            restaurant_datas.append(
                {
                    "name": restaurant.restaurant.name,
                    # "name": "가게",
                    "restaurant_pk": restaurant.restaurant.pk,
                    "address": restaurant.restaurant.address,
                    # "address": "주소",
                    "category": restaurant.restaurant.category.name
                    # "category": "카테고리",
                }
            )
        # print(restaurant_datas)
        # 리뷰 데이터 넣기
        for review in user_reviews:
            restaurant_datas.append(
                {
                    "content": review.content,
                    "restaurant_pk": review.restaurant.pk,
                }
            )
        # all_data = {"restaurant_datas": restaurant_datas, "userinfo": serializers.data}
        all_data = {"userinfo": serializers.data}
        return Response(all_data)

    # 유저정보 수정 put메서드 사용 (raise_exception=True<- (commit=True)와 같은 역활
    elif request.method == "PUT":
        if request.user.is_authenticated:
            serializers = UserInfo(data=request.data, instance=user_info)
            if serializers.is_valid(raise_exception=True):
                serializers.save()
                return Response(serializers.data)