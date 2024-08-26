from django import forms
from .models import Comment,Follow, User

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class FollowForm(forms.Form):
    user_to_follow = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)
    
    def save(self):
        user_to_follow = self.cleaned_data['user_to_follow']
        
        if self.current_user == user_to_follow:
            raise forms.ValidationError('You cannot follow yourself.')
        
        follow_exists = Follow.objects.filter(user=self.current_user, followed_user=user_to_follow).exists()
        
        if follow_exists:
            Follow.objects.filter(user=self.current_user, followed_user=user_to_follow).delete()
        else:
            Follow.objects.create(user=self.current_user, followed_user=user_to_follow)
        
        return not follow_exists  # Return True if following was successful