from rest_framework import serializers
from django.db import transaction
from django.contrib.auth.models import Group
from .models import CustomUser, TaxPayerProfile, TaxZone, TaxCategory, TaxOfficerProfile


class TaxZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxZone
        fields = ['zone_code', 'zone_name', 'city']


class TaxCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxCategory
        fields = ['category_id', 'tax_type', 'tax_rate']


# Auth Serializer

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_id', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


# Profile Serializers

class TaxPayerProfileSerializer(serializers.ModelSerializer):
    # Nested serializer for the user model (One to One relationship)
    user = CustomUserSerializer()

    tax_zone = serializers.PrimaryKeyRelatedField(
        queryset=TaxZone.objects.all(),
        allow_null=True,
        required=False
    )

    class Meta:
        model = TaxPayerProfile
        fields = [
            'tin', 'user', 'tax_zone', 'first_name', 'last_name', 
            'date_of_birth', 'gender', 'house', 'street', 
            'city', 'zip', 'phone1', 'phone2', 'phone3'
        ]
        extra_kwargs = {
            'tin': {'read_only': True}
        }

    def create(self, validated_data):
        # extract user data from the main data payload
        user_data = validated_data.pop('user')

        # atomic transaction ensures either both are created or neither
        with transaction.atomic():
            # create CustomUser instance
            user_serializer = CustomUserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()

            # Assign Group
            group = Group.objects.get_or_create(name='Taxpayers')
            user.groups.add(group)

            # create TaxPayer instance
            profile = TaxPayerProfile.objects.create(user=user, **validated_data)
            return profile
        
    def update(self, instance, validated_data):
        # extract the user data
        user_data = validated_data.pop('user', None)

        # update the user instance (if pasword is provided)
        if user_data:
            user = instance.user
        if 'password' in user_data:
            user.set_password(user_data['password'])
            user.save()

        # update the profile instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class TaxOfficerProfileSerializer(serializers.ModelSerializer):
    # nested serializer for the user model (One to One relationship)
    user = CustomUserSerializer()

    class Meta:
        model = TaxOfficerProfile
        fields = [
            'officer_id', 'user', 'first_name', 'last_name', 'rank', 'branch',
            'house', 'street', 'city', 'zip'
        ]

        extra_kwargs = {
            'officer_id': {'read_only': True}
        }

    def create(self, validated_data):
        # extract user data from the main data payload
        user_data = validated_data.pop('user')

        # atomic transaction ensures either both are created or neither
        with transaction.atomic():
            # create CustomUser instance
            user_serializer = CustomUserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()

            # Assign Group
            group = Group.objects.get_or_create(name='Officers')
            user.groups.add(group)

            # create TaxOfficer instance
            profile = TaxOfficerProfile.objects.create(user=user, **validated_data)
            return profile
    
    def update(self, instance, validated_data):
        # extract the user data
        user_data = validated_data.pop('user', None)

        # update the user instance (if pasword is provided)
        if user_data:
            user = instance.user
        if 'password' in user_data:
            user.set_password(user_data['password'])
            user.save()

        # update the profile instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance