from django import forms

from map.models import User

class AudioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["inputAudioPath"]