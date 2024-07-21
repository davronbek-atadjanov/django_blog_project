from django import forms
from .models import Post, Tags, Review


class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'category','image')


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'image')


class TagForm(forms.ModelForm):
    class Meta:
        model = Tags
        fields = ['name']
class CommentForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['body']
