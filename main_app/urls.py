from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('setup/', views.user_setup, name='setup'),
    path('profile/create/', views.ProfileCreate.as_view(), name='profile_create'),
]