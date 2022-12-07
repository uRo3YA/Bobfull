from django import forms
from .models import Message
from django.forms import TextInput

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content',)
        widgets = {
            'content': TextInput(attrs={
                'placeholder': '보낼 메세지를 입력하세요',
            })
        }
        labels = {
            'content': ''
        }