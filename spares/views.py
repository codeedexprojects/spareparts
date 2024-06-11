from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserProfileSerializer,VerifyOTPSerializer,VehicleCategoriesSerializer, BrandsSerializer,\
      PartsCategorySerializer, AddressSerializer, TopCategorySerializer , ReviewSerializer , CartSerializer
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
from .models import VehicleCategories,brands,partscategory,Address,Top_categories,Review,Cart



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
    

class VehicleCategoriesList(generics.ListCreateAPIView):
    queryset = VehicleCategories.objects.all()
    serializer_class = VehicleCategoriesSerializer

class VehicleCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = VehicleCategories.objects.all()
    serializer_class = VehicleCategoriesSerializer

class BrandsList(generics.ListCreateAPIView):
    queryset = brands.objects.all()
    serializer_class = BrandsSerializer

class BrandDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = brands.objects.all()
    serializer_class = BrandsSerializer

class BrandFilterByIsCarView(generics.ListAPIView):
    serializer_class = BrandsSerializer

    def get_queryset(self):
        is_car = self.kwargs['is_car']
        return brands.objects.filter(is_car=is_car)

class PartsCategoryList(generics.ListCreateAPIView):
    queryset = partscategory.objects.all()
    serializer_class = PartsCategorySerializer

class PartsFilterbyIsofferView(generics.ListCreateAPIView):
    serializer_class = PartsCategorySerializer

    def get_queryset(self):
        is_offer = self.kwargs['is_offer']
        return partscategory.objects.filter(is_offer=is_offer)

class PartsCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = partscategory.objects.all()
    serializer_class = PartsCategorySerializer



class PartsCategoryFilterByVehicle(generics.ListAPIView):
    serializer_class = PartsCategorySerializer

    def get_queryset(self):
        vehicle_id = self.kwargs['vehicle_id']
        return partscategory.objects.filter(v_category_id=vehicle_id)

class PartsCategoryFilterByBrand(generics.ListAPIView):
    serializer_class = PartsCategorySerializer

    def get_queryset(self):
        brand_id = self.kwargs['brand_id']
        return partscategory.objects.filter(v_brand_id=brand_id)
    
#address   

class AddressListCreateView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

#Categories

class TopCategoryListCreateView(generics.ListCreateAPIView):
    queryset = Top_categories.objects.all()
    serializer_class = TopCategorySerializer



class TopCategoryDetailview(generics.RetrieveUpdateDestroyAPIView):
    queryset = Top_categories.objects.all()
    serializer_class = TopCategorySerializer

#review

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

#cart

class CartListCreateView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    
class PartsCategoryFilterByVehicleType(generics.ListAPIView):
    serializer_class = PartsCategorySerializer

    def get_queryset(self):
        is_car = self.kwargs['is_car']
        return partscategory.objects.filter(v_brand__is_car=is_car)
    
class PartsCategoryFilterByTopCategories(generics.ListAPIView):
    serializer_class = PartsCategorySerializer

    def get_queryset(self):
        parts_Cat = self.kwargs['parts_Cat']
        return partscategory.objects.filter(parts_Cat=parts_Cat)

