from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from django.http import JsonResponse

from .models import User
from .serializers import UserSerializer, UserLoginSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all users",
        description="Returns a list of all users.",
        responses={
            200: OpenApiResponse(
                response=UserSerializer(many=True),
                description="List of users",
            ),
            400: OpenApiResponse(description="Bad Request"),
        },
    ),
    retrieve=extend_schema(
        summary="Get a user by ID",
        description="Returns a single user by their ID.",
        responses={
            200: OpenApiResponse(
                response=UserSerializer,
                description="User details",
            ),
            404: OpenApiResponse(description="User not found"),
        },
    ),
    create=extend_schema(
        summary="Create a user",
        description="Creates a new user.",
        request=UserSerializer,
        responses={
            201: OpenApiResponse(
                response=UserSerializer,
                description="Created user",
            ),
            400: OpenApiResponse(description="Validation error"),
        },
    ),
    update=extend_schema(
        summary="Update a user",
        description="Updates an existing user.",
        request=UserSerializer,
        responses={
            202: OpenApiResponse(
                response=UserSerializer,
                description="Updated user",
            ),
            400: OpenApiResponse(description="Validation error"),
            404: OpenApiResponse(description="User not found"),
        },
    ),
    destroy=extend_schema(
        summary="Delete a user",
        description="Deletes a user.",
        responses={
            204: OpenApiResponse(description="User deleted successfully"),
            404: OpenApiResponse(description="User not found"),
        },
    ),
    login=extend_schema(
        summary="Login a user",
        description="Logs in a user by username and returns their details.",
        request=UserLoginSerializer,
        responses={
            200: OpenApiResponse(
                response=UserSerializer,
                description="Logged in user details",
            ),
            400: OpenApiResponse(description="Invalid username"),
        },
    ),
    health_check=extend_schema(
        summary="Health check",
        description="Returns the health status of the service.",
        responses={
            200: OpenApiResponse(description="Service is healthy"),
        },
    ),
)
class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user)

        return Response(serializer.data)


    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        user = User.objects.get(id=pk)
        serializer = UserSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        user = User.objects.get(id=pk)
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data['username']
        user = User.objects.get(username=username)
        serializer = UserSerializer(user)

        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='health')
    def health_check(self, request):
        health_status = {"status": "healthy"}
        return JsonResponse(health_status, status=200)