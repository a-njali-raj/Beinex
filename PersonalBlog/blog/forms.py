from django import forms
from .models import Comment ,User

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

