from django import forms
from .models import CharaimageModel

class ChatForm(forms.Form):
    user_dialogue = forms.CharField(label="", max_length=100)

class SettingsForm(forms.Form):
    system_dialogue = forms.CharField(label="system dialogue", max_length=255)
    name = forms.CharField(label="name", max_length=50)

class CharaimageModelForm(forms.ModelForm):
    charaimage = forms.FileField(label="画像または動画", required=True)
    class Meta:
        model = CharaimageModel
        fields = '__all__'