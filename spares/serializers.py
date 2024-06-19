from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import VehicleCategories, brands, partscategory, Top_categories , Review, Cart, Order


User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True, required=True) 
    password = serializers.CharField(write_only=True, required=True)  
    confirm_password = serializers.CharField(write_only=True, required=True) 

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'confirm_password']

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({'password': 'Passwords do not match'})

        return data

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password', None)
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4)

class VehicleCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleCategories
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'full_name', 'phone_number', 'address_line', 'pincode', 'state', 'city']

class BrandsSerializer(serializers.ModelSerializer):
    vehicle_Brand = serializers.CharField()
    is_car = serializers.BooleanField(default=True)
    class Meta:
        model = brands
        fields = '__all__'

class PartsCategorySerializer(serializers.ModelSerializer):
    parts_Cat = serializers.PrimaryKeyRelatedField(queryset=Top_categories.objects.all())
    part_image = serializers.ImageField()
    v_brand = serializers.PrimaryKeyRelatedField(queryset=brands.objects.all())
    v_category = serializers.PrimaryKeyRelatedField(queryset=VehicleCategories.objects.all())
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    

    class Meta:
        model = partscategory
        fields = '__all__'





class TopCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Top_categories
        fields = '__all__'
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating',  'created_at']


class CartSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    part = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'part', 'quantity', 'created_at', 'updated_at']

    def get_part(self, obj):
        return PartsCategorySerializer(obj.part, context=self.context).data
    

class CheckoutSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    cart_id = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    part = PartsCategorySerializer()

    class Meta:
        model = Order
        fields = ['id', 'user', 'part', 'quantity', 'total_price', 'ordered_at', 'status']


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['address_line']