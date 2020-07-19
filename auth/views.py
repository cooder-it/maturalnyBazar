from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate

# Create your views here.

# Sprawdzamy przy rejestracji czy istnieje
# @api_view(['GET'])
# def check_if_user_exist(request, username):
#     user = User.objects.get(username=username)
#     if user != None:
#         return Response({"exists": True})
#     return Response({"exists": False})


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username  = request.data['username']
    password  = request.data['password']
    userAuth = authenticate(username=username, password=password)
    if userAuth:
        user = User.objects.get(username=username)
        token = Token.objects.get(user = user)
        return Response({
            "token": token.key,
            "username": user.username,
            "email": user.email
            })
    return Response({
        "token": "error"
        })


@api_view(['POST'])
def register_user(request):
    username  = request.data['username']
    password  = request.data['password']
    email     = request.data['email']
    try:
        userName  = User.objects.get(username=username)
    except:
        userName = None
    try:
        userEmail = User.objects.get(email=email)
    except:
        userEmail = None
   
    if (userName != None):
        return Response({
            "usernameExists": True,
            "emailExists": False,
            "success": False,
        })
    if (userEmail != None):
        return Response({
            "usernameExists": False,
            "emailExists": True,
            "success": False,
        })

    user  = User.objects.create_user(username, email, password)
    token = Token.objects.create(user=user)
    user.save()
    return Response({
        "usernameExists": False,
        "emailExists": False,
        "success": True,
    })
