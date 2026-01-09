from rest_framework import serializers
from django.db import transaction
from .models import CustomUser, TaxPayerProfile, TaxOfficerProfile

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_id', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'user_id': {'read_only', True}
        }
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class TaxOfficerProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = TaxOfficerProfile
        fields = [
            'officer_id', 'user', 'first_name', 'last_name', 
            'rank', 'branch', 'house_no', 'street', 'city', 'zip'
        ]
        extra_kwargs = {
            'officer_id': {'read_only': True}
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        with transaction.atomic():
            user_serializer = CustomUserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()

            # 2. Create the Profile instance linked to that User
            profile = TaxOfficerProfile.objects.create(user=user, **validated_data)
            return profile


class TaxPayerProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = TaxPayerProfile
        fields = [
            'tin', 'user', 'first_name', 'last_name', 'date_of_birth',
            'gender', 'house', 'street', 'city', 'zip',
            'phone1', 'phone2', 'phone3'
        ]
        extra_kwargs = {
            'tin': {'read_only': True} 
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        with transaction.atomic():
            user_serializer = CustomUserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()

            profile = TaxPayerProfile.objects.create(user=user, **validated_data)
            return profile