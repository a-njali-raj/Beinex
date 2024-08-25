from django import forms
from .models import Comment,Like

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

