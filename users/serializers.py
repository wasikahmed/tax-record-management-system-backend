from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import transaction
from django.contrib.auth.models import Group
from rest_framework.exceptions import AuthenticationFailed

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
    

# Custom Login Serializer
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_id'] = serializers.IntegerField(required=False)
        self.fields['tin'] = serializers.IntegerField(required=False)
        self.fields['officer_id'] = serializers.IntegerField(required=False)

    def validate(self, attrs):
        password = attrs.get('password')
        tin = attrs.get('tin')
        officer_id = attrs.get('officer_id')
        user = None

        if tin:
            try:
                profile = TaxPayerProfile.objects.get(tin=tin)
                user = profile.user
            except TaxPayerProfile.DoesNotExist:
                raise AuthenticationFailed("No Taxpayer found with this TIN.")
        
        elif officer_id:
            try:
                profile = TaxOfficerProfile.objects.get(officer_id=officer_id)
                user = profile.user
            except TaxOfficerProfile.DoesNotExist:
                raise AuthenticationFailed("No Officer found with this ID.")
        
        elif attrs.get('user_id'):
            try:
                user = CustomUser.objects.get(user_id=attrs.get('user_id'))
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("User ID not found.")
        
        else:
            # FIX 2: Better error message
            raise AuthenticationFailed("Must provide 'tin' or 'officer_id'.")

        
        # Authenticate
        if user and user.check_password(password):
            if not user.is_active:
                raise AuthenticationFailed("User account is disabled.")

            # generate token   
            refresh = self.get_token(user)

            # add custom claims to token
            if hasattr(user, 'taxpayerprofile'):
                refresh['role'] = 'taxpayer'
                refresh['tin'] = user.taxpayerprofile.tin
            elif hasattr(user, 'taxofficerprofile'):
                refresh['role'] = 'officer'
                refresh['officer_id'] = user.taxofficerprofile.officer_id
            elif user.is_superuser:
                refresh['role'] = 'admin'
            
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': refresh.get('role', 'unknown')
            }
            return data
    
        raise AuthenticationFailed("Invalid credentials.")