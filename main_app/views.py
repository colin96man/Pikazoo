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
  profile = Profile.objects.get(id=request.user.id)
  print(profile)
  return render(request, 'about.html', { 'profile': profile })

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      profile = Profile.objects.create(id=user.id, user=user)
      profile.save()
      login(request, user)
      return redirect(f'/profile/{profile.id}/update/')
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
    success_url = '/animals/'

def get_state_organizations(request):
    profile = Profile.objects.get(id=request.user.id)
    print(profile.location, "PROFILE")
    print('this is what we are looking at', profile.pet_preference)
    state_organizations = pf.organizations(state=f'{profile.location}')
    return render(request, 'rescues/index.html', { 'state_organizations': state_organizations })

def get_some_animals(request):
    profile = Profile.objects.get(id=request.user.id)
    print(profile.location)
    print(profile.pet_preference)
    all_animals = pf.animals(animal_type=f'{profile.pet_preference}', status='adoptable', location=f'{profile.location}', sort='distance')
    print(all_animals)
    return render(request, 'animals/index.html', { 'all_animals': all_animals })

def get_animal_details(request, animal_id):
    pass