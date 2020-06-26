from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.template.defaulttags import register
from django.contrib.auth.decorators import login_required
from .models import Profile, Playdate
from .forms import PlaydateForm
import os
import petpy
from petpy import Petfinder


key = os.environ['API_KEY']
secret = os.environ['API_SECRET']
pf = Petfinder(key, secret)

# Create your views here.
def home(request):
  return render(request, 'home.html')

@login_required
def about(request):
  profile = Profile.objects.get(id=request.user.id)
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

@login_required
def get_state_organizations(request):
    profile = Profile.objects.get(id=request.user.id)
    state_organizations = pf.organizations(state=f'{profile.location}')
    return render(request, 'rescues/index.html', { 'state_organizations': state_organizations })

@login_required
def get_some_animals(request):
    profile = Profile.objects.get(id=request.user.id)
    all_animals = pf.animals(animal_type=f'{profile.pet_preference}', status='adoptable', location=f'{profile.location}', sort='distance', distance=500, results_per_page=60)    
    return render(request, 'animals/index.html', { 'all_animals': all_animals, 'profile' : profile })

def get_animal_details(request, animal_id):
    one_animal = pf.animals(animal_id=animal_id)
    playdate_form = PlaydateForm()
    return render(request, 'animals/animals_detail.html', { 'one_animal': one_animal, 'playdate_form': playdate_form })

def add_playdate(request, animal_id):
  profile = Profile.objects.get(id=request.user.id)
  form = PlaydateForm(request.POST)
  animal = pf.animals(animal_id=f'{animal_id}')
  if form.is_valid():
    new_playdate = form.save(commit=False)
    new_playdate.animal_id = animal_id
    new_playdate.shelter_id = animal['animals']['organization_id']
    new_playdate.profile = profile
    new_playdate.save()
  return redirect('animal_details', animal_id=animal_id)

def get_photo(all_playdates):
        photos = []
        for playdate in all_playdates:
          try:
            animal = pf.animals(animal_id=f'{playdate.animal_id}')
            photo = animal['animals']['primary_photo_cropped']['small']
            photos.append({playdate.id: photo})
          except: 
            photos.append({'none'})
        return photos

def get_detail(all_playdates, detail):
    values = []
    for playdate in all_playdates:
      try:
        animal = pf.animals(animal_id=f'{playdate.animal_id}')
        one_detail = animal['animals'][f'{detail}']
        values.append({playdate.id: one_detail})
      except:
        values.append({'none'})
    return values
    
def get_shelter(all_playdates, detail):
    values = []
    for playdate in all_playdates:
      try:
        organization = pf.organizations(organization_id=f'{playdate.shelter_id}')
        one_detail = organization['organizations'][f'{detail}']
        values.append({playdate.id: one_detail})
      except:
        values.append({'none'})
    return values

def get_playdates(request):
    profile = Profile.objects.get(id=request.user.id)
    all_playdates = Playdate.objects.filter(profile=profile)
    def get_animals(all_playdates):
        animals = []
        for playdate in all_playdates:
          try:
            animal = pf.animals(animal_id=f'{playdate.animal_id}')
            animals.append({playdate.id: 'true'})
          except:
            animals.append({playdate.id: 'false'})
        return animals
    animals = get_animals(all_playdates)
    print(animals)
    names = get_detail(all_playdates, 'name')
    photos = get_photo(all_playdates)
    shelters = get_shelter(all_playdates, 'name')
    shelterlinks = get_shelter(all_playdates, 'website')
    return render(request, 'playdates/index.html', { 'all_playdates': all_playdates, 'photos': photos, 'names': names, 'shelters': shelters, 'shelterlinks': shelterlinks, 'animals': animals })

class PlaydateDelete(DeleteView):
    model = Playdate
    success_url = '/playdates/'
    
    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      animal = pf.animals(animal_id=context['object'].animal_id)
      context['animal'] = animal['animals']
      return context

class PlaydateUpdate(UpdateView):
    model = Playdate
    fields = ['date', 'activity']
    success_url = '/playdates/'

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      animal = pf.animals(animal_id=context['object'].animal_id)
      context['animal'] = animal['animals']
      return context

@register.filter
def get_item(detaillist, detailkey):
    for detail in detaillist:
       try:
         for key, value in detail.items():
             if key == detailkey:
               return value
       except:
         return 'Resource does not exist'
        
  