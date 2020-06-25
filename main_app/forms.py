from django.forms import ModelForm
from .models import Playdate
import petpy
from petpy import Petfinder

class PlaydateForm(ModelForm):
  class Meta:
    model = Playdate
    fields = ['date', 'activity']



    