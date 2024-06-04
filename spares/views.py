from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserProfileSerializer,VerifyOTPSerializer
from django.contrib.auth import get_user_model
import random
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
import datetime
import jwt


# Create your views here.



User = get_user_model()
#user_registration

def send_otp_email(email, otp):
    subject = 'Your OTP for Registration'
    message = f'Your OTP is: {otp}'
    from_email = 'praveen.codeedex@gmail.com' 
    send_mail(subject, message, from_email, [email])

@api_view(['POST'])
def register(request):
    serializer = UserProfileSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data['email']

        if User.objects.filter(email=email).exists():
            return Response({'message': 'Email already registered', 'status': False}, status=status.HTTP_400_BAD_REQUEST)

        otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])

        user = serializer.save(otp=otp)

        send_otp_email(email, otp)

        return Response({'message': 'OTP sent to email', 'status': True}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def verify(request):
    serializer = VerifyOTPSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data['email']
        otp_entered = serializer.validated_data['otp']

        try:
            user_profile = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'Email not registered','status':False}, status=status.HTTP_400_BAD_REQUEST)

        if user_profile.otp == otp_entered:
            user_profile.otp = None
            user_profile.save()
            return Response({'message': 'OTP verified successfully','status':True}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid OTP','status':False}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            raise ValidationError('Email and password are required.', code='missing_credentials')

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!', False)

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!', False)

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'id': user.id,
            'token': token,
            'message': 'Login successful',
            'status': True
        }
        return response
    

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logout successful',
            'status': True
        }
        return response