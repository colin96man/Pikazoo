from django.forms import ModelForm
from .models import Playdate

class PlaydateForm(ModelForm):
  class Meta:
    model = Playdate
    fields = ['date', 'activity']
    