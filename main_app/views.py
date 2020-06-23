from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from .models import Profile, Playdate
import os
import petpy
from petpy import Petfinder

key = os.environ['API_KEY']
secret = os.environ['API_SECRET']
pf = Petfinder(key, secret)

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      profile = Profile.objects.get_or_create(user=user)
      login(request, user)
      return redirect(f'/profile/{user.id}/update/')
    else:
      error_message = 'Invalid sign up - try again!'
  form = UserCreationForm()
  context = {
    'form': form,
    'error_message': error_message
  }
  return render(request, 'registration/signup.html', context)

class ProfileUpdate(UpdateView):
    model = Profile
    fields = ['location', 'pet_preference']
    success_url = '/rescues/'

def get_state_organizations(request):
    profile = Profile_id
    profile_location = Profile.location
    state_organizations = pf.organizations(state=f'{profile.profile_location}')
    print(state_oranizations)
    return render(request, 'rescues/index.html', { 'state_organizations': state_organizations })

def get_animals(request, organization_id):
    pass

def get_animal_details(request, animal_id):
    pass