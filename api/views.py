import json
import requests
import threading
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from http import HTTPStatus
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from time import sleep

from .models import Image, User, Tier
from .serializers import TierSerializer, ImageSerializer, UploadImageSerializer

class TierList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = TierSerializer
    queryset = Tier.objects.all()

class TierDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = TierSerializer
    queryset = Tier.objects.all()

@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Login': '/login_user/',
        'Logout': '/logout_user/',
        'Tier (Admin Only)': '/tier/',
        'Tier Detail View (Admin Only)': '/tier/<int:pk>/',
        'List of uploaded images': '/image-list/',
        'Upload Image': '/upload/',
        'Generate link to image (Enterprise tier only)': '/generate_link/?image_id=()&expiration_time=(300-3000)/'
    }
    return Response(api_urls)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def image_list(request):
    images = Image.objects.filter(user=request.user)
    serializer = ImageSerializer(images, context={'request':request}, many=True)
    return Response(serializer.data)

class ImageViewSet(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UploadImageSerializer
        return ImageSerializer

    def get_queryset(self):
        queryset = Image.objects.filter(user=self.request.user)
        return queryset

    def post(self, request, *args, **kwargs):
        file = request.data['image']
        image = Image.objects.create(image=file, user=request.user)
        result = {
            'thumbnail200_link': request.build_absolute_uri(image.image_200.url)
        }

        current_user_tier = request.user.tier

        if current_user_tier.link_to_thumbnail400_file:
            result['thumbnail400_link'] = request.build_absolute_uri(image.image_400.url)
        if current_user_tier.link_to_original_file:
            result['link_to_original_file'] = request.build_absolute_uri(image.image.url)
        
        return Response(result, status=HTTPStatus.OK)
    
@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    if request.user.is_authenticated:
        return Response(f"You are already logged in as {request.user.username}")
     
    data = {}
    req_body = json.loads(request.body)
    username = req_body['username']
    password = req_body['password']
    try:
        account = User.objects.get(username=username)
    except BaseException as e:
        raise ValidationError({"400": f'{str(e)}'})
    
    token = Token.objects.get_or_create(user=account)[0].key
   
    if password != account.password:
        raise ValidationError({"message": "Incorrect Login credentials"})

    if account:
        if account.is_active:
            login(request, account)
            data["message"] = "user logged in"
            data["username"] = account.username
            res = {"data": data, "token": token}

            return Response(res)
        else:
            raise ValidationError({"400": f'Account not active'})
    else:
        raise ValidationError({"400": f'Account doesnt exist'})
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    request.user.auth_token.delete()
    logout(request)
    return Response("User Logged out Successfully")

def delete_link(expiration_time, link_id):
    sleep(expiration_time)
    url = f"https://api.short.io/links/{link_id}"
    headers = {'authorization': 'sk_NRiUdNPDicteRo2D'}
    response = requests.request("DELETE", url, headers=headers)
    print(response.text)

@api_view(["GET"])
def generate_link(request):
    if not request.user.tier.generate_expiring_link:
        return Response("You don't have permissions to do that. You must have an 'Enterprise' tier to be able to generate a link")
    
    image_id = int(request.query_params.get('image_id'))
    expiration_time = int(request.query_params.get('expiration_time'))

    if expiration_time < 300 or expiration_time > 30000:
        return Response("Expiration time must be between 300 and 30000 seconds")
    
    url = "https://api.short.io/links"

    image = Image.objects.get(id=image_id)
    image_absolute_url = request.build_absolute_uri(image.image.url)

    payload = json.dumps({
        "allowDuplicates":False,
        "domain":"86fu.short.gy",
        "originalURL":image_absolute_url})
    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'authorization': "sk_NRiUdNPDicteRo2D"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    r = json.loads(response.text)
    link_id = r['idString']
    short_URL = r['shortURL']

    t = threading.Thread(target=delete_link, args=[expiration_time, link_id])
    t.setDaemon(False)
    t.start()

    result = {
        "short_URL": short_URL,
        "expiration_time": f"{expiration_time} seconds"
    }

    return Response(result)
