from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True, required=True) 
    password = serializers.CharField(write_only=True, required=True)  # Add required=True
    confirm_password = serializers.CharField(write_only=True, required=True)  # Add required=True

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'confirm_password']

    def validate(self, data):
        # Check if password and password2 match
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({'password': 'Passwords do not match'})

        return data

    def create(self, validated_data):
        # Pop password2 as we don't need it when creating the user
        confirm_password = validated_data.pop('confirm_password', None)
        # Create user instance without saving it yet
        user = User(**validated_data)
        # Set password using set_password method
        user.set_password(validated_data['password'])
        # Save the user
        user.save()
        return user

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4)