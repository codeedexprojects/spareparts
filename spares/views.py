from django.shortcuts import render
from rest_framework import generics,permissions
from rest_framework.permissions import AllowAny
from .serializers import UserProfileSerializer,VerifyOTPSerializer,VehicleCategoriesSerializer, BrandsSerializer,\
      PartsCategorySerializer, TopCategorySerializer , ReviewSerializer, CartSerializer ,UserSerializer, OrderSerializer,\
      UserAddressSerializer
from django.contrib.auth import get_user_model
import random
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
import datetime
from django.db import transaction
import jwt
from django.db.models import Q
from .models import VehicleCategories,brands,partscategory,Top_categories,Review,Cart,Order



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
    

class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

class UserProfileCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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

class AddToCartView(APIView):
    def post(self, request, user_id, parts_id):
        user = get_object_or_404(User, pk=user_id)
        part = get_object_or_404(partscategory, pk=parts_id)

        cart_item, created = Cart.objects.get_or_create(user=user, part=part)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        serializer = CartSerializer(cart_item, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)





class UserCartView(APIView):
    def get(self, request, user_id):
        cart_items = Cart.objects.filter(user_id=user_id)
        total_cart_price = 0
        for cart_item in cart_items:
            cart_item.total_price = cart_item.quantity * cart_item.part.price
            total_cart_price += cart_item.total_price
        serializer = CartSerializer(cart_items, context={'request': request}, many=True)
        response_data = {
            'message': 'Products Retrieved Successfully',
            'cart_items': serializer.data,
            'total_cart_price': total_cart_price
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
class UpdateCartView(APIView):
    def put(self, request, user_id, cart_item_id):
        cart_item = get_object_or_404(Cart, pk=cart_item_id, user_id=user_id)
        serializer = CartSerializer(cart_item, data=request.data)

        # Calculate the price for the specific cart item
        cart_price = cart_item.quantity * cart_item.part.price if cart_item.part.price else 0

        if serializer.is_valid():
            serializer.save()

            # Calculate the total cart price
            cart_items = Cart.objects.filter(user_id=user_id)
            total_cart_price = sum(item.quantity * item.part.price for item in cart_items if item.part.price)

            response_data = {
                'message': 'Updated Cart Successfully',
                'cart_items': serializer.data,
                'total_cart_price': total_cart_price,
                'cart_price': cart_price,
                'status': True
            }

            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteCartItemView(APIView):
    def delete(self, request, user_id, cart_item_id):
        cart_item = get_object_or_404(Cart, pk=cart_item_id, user_id=user_id)
        cart_item.delete()
        cart_items = Cart.objects.filter(user_id=user_id)
        response_data = {
            'message': 'Removed From Cart Successfully',
            'status':True
        }

        return Response(response_data, status=status.HTTP_200_OK)


    
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


class CheckoutView(APIView):
    def post(self, request, user_id, cart_id):
        try:
            with transaction.atomic():
                total_price = 0
                cart_item = get_object_or_404(Cart, user_id=user_id, id=cart_id)

                # Calculate total price
                product = cart_item.part
                total_price += product.price * cart_item.quantity

                # Create order
                order = Order(
                    user=cart_item.user,
                    part=cart_item.part,
                    quantity=cart_item.quantity,
                    total_price=product.price * cart_item.quantity,
                    status='Pending'
                )
                order.save()

                # Delete the cart item
                cart_item.delete()

                return Response({'message': 'Checkout successful', 'total_price': total_price}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class MyOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Order.objects.filter(user_id=user_id).order_by('-ordered_at')


class PartCategorySearchView(generics.ListAPIView):
    serializer_class = PartsCategorySerializer

    def get_queryset(self):
        search_query = self.request.query_params.get('search_query', None)
        if search_query:
            return partscategory.objects.filter(
                Q(parts_name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        return partscategory.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'results': serializer.data})
    

class UserAddressView(generics.RetrieveAPIView):
    serializer_class = UserAddressSerializer

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)