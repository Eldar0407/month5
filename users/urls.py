from django.urls import path
from . import views
from .views import confirm_view

urlpatterns = [
    path('registration/', views.registration_api_view),
    path('authorization/', views.authorization_api_view),
    path('confirm/', confirm_view, name='confirm_user'),
]