import time
import json
from django.shortcuts import render,redirect
from django.http import JsonResponse
import random
import os
from .models import RoomMember
from django.views.decorators.csrf import csrf_exempt
from .serializers import RegisterSerializer, LoginSerializer,RequestPasswordResetSerializer, SetNewPasswordSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from agora_token_builder import RtcTokenBuilder
import requests
from django.http import JsonResponse
from django.conf import settings
import base64
import dotenv
from .models import User
from .utils import generate_otp, send_otp_email


User = get_user_model()


dotenv.load_dotenv()


# APP_ID='2f3131394cc6417b91aa93cfde567a37'
# APP_CERTIFICATE='d66d80fb791f48df8f91fdd513d82d32'
# BASE_URL = "https://api.agora.io/v1"


def acquire_resource(request):
    url = f"https://api.agora.io/v1/apps/{settings.AGORA_APP_ID}/cloud_recording/acquire"
    headers = {
        "Authorization": f"Basic {settings.AGORA_AUTH_HEADER}",
        "Content-Type": "application/json",
    }
    data = {
        "cname": request.GET.get("channel_name", "testChannel"),
        "uid": request.GET.get("uid", "12345"),
        "clientRequest": {},
    }

    response = requests.post(url, headers=headers, json=data)
    return JsonResponse(response.json())

def start_recording(request):
    resource_id = request.GET.get("resource_id")
    channel_name = request.GET.get("channel_name", "testChannel")
    uid = request.GET.get("uid", "12345")
    url = f"https://api.agora.io/v1/apps/{settings.AGORA_APP_ID}/cloud_recording/resourceid/{resource_id}/mode/mix/start"
    
    headers = {
        "Authorization": f"Basic {settings.AGORA_AUTH_HEADER}",
        "Content-Type": "application/json",
    }
    data = {
        "cname": channel_name,
        "uid": uid,
        "clientRequest": {
            "recordingConfig": {
                "channelType": 0,
                "streamTypes": 1,
                "audioProfile": 1,
                "maxIdleTime": 30,
            },
            "storageConfig": {
                "vendor": 1,
                "region": 0,
                "bucket": "agorabucket12",
                "accessKey": os.getenv('accesskey'),
                "secretKey": os.getenv('secretkey'),
                "fileNamePrefix": ["audio", "meeting-records"],
            },
        },
    }

    response = requests.post(url, headers=headers, json=data)
    return JsonResponse(response.json())


def stop_recording(request):
    resource_id = request.GET.get("resource_id")
    sid = request.GET.get("sid")
    channel_name = request.GET.get("channel_name", "testChannel")
    uid = request.GET.get("uid", "12345")
    url = f"https://api.agora.io/v1/apps/{settings.AGORA_APP_ID}/cloud_recording/resourceid/{resource_id}/sid/{sid}/mode/mix/stop"
    
    headers = {
        "Authorization": f"Basic {settings.AGORA_AUTH_HEADER}",
        "Content-Type": "application/json",
    }
    data = {
        "cname": channel_name,
        "uid": uid,
        "clientRequest": {},
    }

    response = requests.post(url, headers=headers, json=data)
    return JsonResponse(response.json())





# Password Reset Request View
class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = RequestPasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(user)
                return Response({
                    "message": "Password reset token generated.",
                    "token": token
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Set New Password View
class SetNewPasswordView(APIView):
    def post(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            try:
                user = User.objects.get(email=email)
                token_generator = PasswordResetTokenGenerator()
                if token_generator.check_token(user, token):
                    user.set_password(new_password)
                    user.save()
                    return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(email=email).exists():
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

        otp = generate_otp()
        user = User.objects.create(email=email, otp=otp)
        user.set_password(password)
        user.save()

        send_otp_email(email, otp)
        return Response({'message': 'OTP sent to your email'}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()

        if user and user.check_password(password):
            otp = generate_otp()
            user.otp = otp
            user.save()
            send_otp_email(email, otp)
            return Response({'message': 'OTP sent to your email'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        user = User.objects.filter(email=email, otp=otp).first()

        if user:
            user.is_verified = True
            user.otp = None  # Clear the OTP after successful verification
            user.save()
            return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)



def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "chatPage.html", context)


def lobby(request):
    return render(request, 'lobby.html')

def room(request):
    return render(request, 'room.html')


def getToken(request):
    appId = '2f3131394cc6417b91aa93cfde567a37'
    appCertificate = 'd66d80fb791f48df8f91fdd513d82d32'
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)

