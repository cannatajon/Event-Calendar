from django.forms import ModelForm
from .models import Event


class StartEnd(ModelForm):
    class Meta:
        model = Event
        fields = ['start_time', 'end_time']
