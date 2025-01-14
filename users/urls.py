from django.urls import path

from .views import UserViewSet


urlpatterns = [
    path('users', UserViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('users/login', UserViewSet.as_view({
        'post': 'login',
    })),
    path('users/health', UserViewSet.as_view({
        'get': 'health_check',
    })),
    path('users/<str:pk>', UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
]