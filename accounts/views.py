from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from accounts.pagination import CustomPagination
from accounts.serializers import UserSerializer
from rest_framework import viewsets, generics, status, views
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from dj_rest_auth.registration.views import RegisterView
from rest_framework import status
from rest_framework.response import Response
from django.urls import reverse_lazy


class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.all()
        page = CustomPagination
        serializer = UserSerializer(queryset, many=True, context=self.get_serializers_context())
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        page = CustomPagination
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user, context=self.get_serializers_context())
        return Response(serializer.data)

    def get_serializers_context(self):
        return {'request': self.request}

    def get_permissions(self):
        permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class CustomRegisterView(RegisterView):
    @method_decorator(ensure_csrf_cookie, csrf_protect)
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            data = {
                "success": "User registered successfully",
                "login": reverse_lazy("rest_login"),
            }
            response.data = data
            return response
        elif response.status_code == status.HTTP_204_NO_CONTENT:
            data = {
                "success": "User registered successfully",
                "login": reverse_lazy("rest_login"),
            }
            response.data = data
            return response
        return Response(response.data, status=response.status_code)
