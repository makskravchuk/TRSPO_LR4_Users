from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer, TokenSerializer


# Create your views here.
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserAPIView(APIView):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(data=serializer.data)

    def post(self, request):
        user = UserSerializer(data=request.data)
        if user.is_valid(raise_exception=True):
            user.save()
        return Response(status=201)

    def put(self, request, pk):
        try:
            instance = User.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = UserSerializer(data=request.data, instance=instance)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"user": serializer.data})

    def delete(self, request, pk):
        try:
            User.objects.filter(pk=pk).delete()
        except:
            return Response({"error": "Object does not exists"})
        return Response(status=200)


@api_view(['POST'])
def get_user_id(request):
    user_id = get_user(request)
    if user_id:
        return Response({'user_id':user_id})
    return Response({'error': 'Недійсний токен'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def is_admin(request):
    user_id = get_user(request)
    if user_id:
        user = User.objects.get(pk=user_id)
        return Response({"is_admin": user.is_superuser})
    return Response({'error': 'Недійсний токен'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def is_authenticated(request):
    user_id = get_user(request)
    if user_id:
        user = User.objects.get(pk=user_id)
        return Response({"is_authenticated": user.is_authenticated})
    return Response({'error': 'Недійсний токен'}, status=status.HTTP_401_UNAUTHORIZED)


def get_user(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        token_obj = Token.objects.get(key=serializer.validated_data['token'])
        user_id = token_obj.user_id
        return user_id
    return None
