from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer, UserLoginSerializer

from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    list=extend_schema(
        summary="List all users",
        description="Returns a list of all users.",
        responses=UserSerializer,
    ),
    retrieve=extend_schema(
        summary="Get a user by ID",
        description="Returns a single user by its ID.",
        responses=UserSerializer,
    ),
    create=extend_schema(
        summary="Create a user",
        description="Creates a new user.",
        request=UserSerializer,
        responses=UserSerializer,
    ),
    update=extend_schema(
        summary="Update a user",
        description="Updates an existing user.",
        request=UserSerializer,
        responses=UserSerializer,
    ),
    destroy=extend_schema(
        summary="Delete a user",
        description="Deletes a user.",
    ),
    login=extend_schema(
        summary="Temporary login",
        description="Returns user by username.",
        request=UserLoginSerializer,
        responses=UserSerializer,
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

    def login(self, request):
        username = request.data['username']
        user = User.objects.get(username=username)
        serializer = UserSerializer(user)

        return Response(serializer.data)
