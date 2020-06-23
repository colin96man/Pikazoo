from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/<int:pk>/update/', views.ProfileUpdate.as_view(), name='profile_update'),
    path('rescues/', views.get_state_organizations, name='index'),
    path('rescues/<slug:organization_id>/detail/', views.get_animals, name='rescue_detail'),
    path('animals/<int:animal_id>/', views.get_animal_details, name='animal_details'),
]