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
    success_url = '/rescues/index.html'

def get_state_organizations(request):
    profile = Profile.objects.get(id=request.user.id)
    state_organizations = pf.organizations(state=f'{profile.location}')
    return render(request, 'rescues/index.html', { 'state_organizations': state_organizations })

def get_animals(request, organization_id):
    profile = Profile.objects.get(id=request.user.id)
    organization_animals = pf.animals(organization_id=organization_id, animal_type=f'{profile.pet_preference}')
    print(organization_animals)
    return render(request, 'rescues/rescue_detail.html') #{ 'organization_animals': organization_animals })

def get_animal_details(request, animal_id):
    pass