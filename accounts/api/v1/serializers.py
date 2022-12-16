from django.contrib.auth import authenticate
from django.utils.text import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'date_joined',
        ]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label=_('Username'), required=True)
    password = serializers.CharField(label=_('Password'), required=True)

    def validate(self, attrs: dict):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(self.context['request'], username=username, password=password)

        if not user:
            raise serializers.ValidationError(_('Invalid credentials!'))

        attrs.update({'user': user})
        return attrs

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(label=_('Username'), required=True, write_only=True)
    password = serializers.CharField(label=_('Password'), required=True, write_only=True)

    def create(self, validated_data):
        username = validated_data.pop('username', '')
        password = validated_data.pop('password', '')

        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        user_token, _ = Token.objects.get_or_create(user=user)

        return user_token, user

    def update(self, instance, validated_data):
        pass
