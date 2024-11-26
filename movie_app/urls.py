from django.urls import path
from . import views

urlpatterns = [
    path('', views.MovieViewSet.as_view({
        'get': 'list', 'post': 'create'
    })),
    path('<int:pk>/', views.MovieViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
    })),
    path('directors/', views.DirectorListAPIView.as_view()),
    path('directors/<int:id>/', views.DirectorDetailAPIView.as_view()),
    path('reviews/', views.ReviewViewSet.as_view({
        'get': 'list', 'post': 'create'
    })),
    path('reviews/<int:pk>/', views.ReviewViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
    }))
]