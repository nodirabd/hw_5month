import random # dlya generatsii sluchaynogo koda
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .serializers import RegisterValidateSerializer, AuthValidateSerializer, ConfirmValidateSerializer
from .models import UserConfirm


class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegisterValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = User.objects.create_user(
            username=username,
            password=password,
            is_active=False
        )

        random_code = str(random.randint(100000, 999999))
        UserConfirm.objects.create(user=user, code=random_code)

        return Response(
            status=status.HTTP_201_CREATED,
            data={'user_id': user.id, 'code': random_code}
        )


class ConfirmAPIView(APIView):
    def post(self, request):
        serializer = ConfirmValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        code = serializer.validated_data['code']

        try:
            confirm_record = UserConfirm.objects.get(user_id=user_id, code=code)
            user = confirm_record.user
            user.is_active = True
            user.save()
            confirm_record.delete()
            return Response(
                status=status.HTTP_200_OK,
                data={'message': 'Успешно подтверждено!'}
            )
        except UserConfirm.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': 'incorrect code or user_id does not exist'}
            )


class AuthorizationAPIView(APIView):
    def post(self, request):
        serializer = AuthValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})

        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
            data={'error': 'data is not correct or user is not active'}
        )