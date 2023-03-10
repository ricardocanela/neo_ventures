from rest_framework import serializers
from .models import Company, Demand, Solution
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ('user',) 

class SolutionListSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Solution
        fields = '__all__'

class SolutionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = '__all__'


class DemandListSerializer(serializers.ModelSerializer):
    solutions = serializers.PrimaryKeyRelatedField(
        queryset=Solution.objects.all(), many=True)
    company = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Demand
        fields = '__all__'

class DemandCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Demand
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username"]


# Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
                  'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
