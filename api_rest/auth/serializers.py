from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required = True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="This username is already taken")]
    )
    password = serializers.CharField(
        write_only = True,
        required = True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        
        return user