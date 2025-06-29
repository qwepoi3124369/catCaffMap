from django import forms
from world.models import Announcement


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['name', 'content', 'owner']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px;'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'style': 'width: 600px;'}),
            'owner': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px;'}),
        }
