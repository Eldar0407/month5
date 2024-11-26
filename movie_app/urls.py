from django.urls import path
from . import views

urlpatterns = [
    path('', views.MovieCreateView),
    path('<int:id>/', views.MovieDetailView)
]