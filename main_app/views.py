from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
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
      #This is how we programmatically login
      login(request, user)
      return redirect('setup')
    else:
      error_message = 'Invalid sign up - try again!'
  # A bad POST or it's a GET
  form = UserCreationForm()
  context = {
    'form': form,
    'error_message': error_message
  }
  return render(request, 'registration/signup.html', context)

def user_setup(request):
    return render(request, 'user/setup.html')

def get_state_organizations(request):
    state_organizations = pf.organizations(state=f'{Profile.location}')
    print(state_oranizations)
    return render(request, 'rescues/index.html', { 'state_organizations': state_organizations })

def get_animals(request, organization_id):
    pass
