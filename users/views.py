from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserCreateSerializer, UserAuthSerializer, UserConfirmSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import ConfirmCode

@api_view(['POST'])
def registration_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        confirmation_code, created = ConfirmCode.objects.get_or_create(user=user)
        confirmation_code.generate_code()
        return Response({
            "message": "Пользователь зарегистрирован. Проверьте код подтверждения.",
            "confirmation_code": confirmation_code.code
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.validated_data)
    if user is not None:
        token = Token.objects.get(user=user)
        return Response(data={'key': token.key},
                        status=status.HTTP_200_OK)
    return Response(data={'error': 'User not valid!'},
                    status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def confirm_view(request):
    serializer = UserConfirmSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.confirm_user()
        return Response({"message": f"Пользователь {user.username} подтверждён."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


