from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from users.models import SudokuStatisticModel


class UserSignUpSerializer(serializers.ModelSerializer):
    token = serializers.StringRelatedField(read_only=True, source='auth_token')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'token']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        self.create_statistic(user=user)
        return user

    def create_statistic(self, user):
        """Here creates statistical models for all games"""
        SudokuStatisticModel.objects.create(user=user)
