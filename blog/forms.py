from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Write your comment...'
        })
    )

    class Meta:
        model = Comment
        fields = ['content']
