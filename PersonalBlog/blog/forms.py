from django import forms
from .models import Comment,Follow

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class FollowForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput())