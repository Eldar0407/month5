from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ConfirmCode

class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.IntegerField()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class UserConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        username = data.get('username')
        code = data.get('code')
        try:
            user = User.objects.get(username=username)
            confirmation_code = user.confirmation_code
            if confirmation_code.code != code:
                raise serializers.ValidationError("Неверный код подтверждения.")
        except (User.DoesNotExist, ConfirmCode.DoesNotExist):
            raise serializers.ValidationError("Пользователь или код подтверждения не найдены.")
        return {"user": user}

    def confirm_user(self):
        user = self.validated_data['user']
        user.is_active = True
        user.confirmation_code.delete()
        user.save()
        return user