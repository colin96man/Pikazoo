from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Profile

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
      login(request, user)
      return redirect('setup')
    else:
      error_message = 'Invalid sign up - try again!'
  form = UserCreationForm()
  context = {
    'form': form,
    'error_message': error_message
  }
  return render(request, 'registration/signup.html', context)

def user_setup(request):
    return render(request, 'user/setup.html')

class ProfileCreate(CreateView, LoginRequiredMixin):
    model = Profile
    fields = ['user', 'location', 'pet_preference']
    success_url = '/about/'

    def get_initial(self):
      return { 'user': self.request.user }
      