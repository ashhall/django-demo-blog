from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 
            'email', 
            'text')

        widgets = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'text':forms.Textarea(
                attrs={'class':'editable medium-editor-textarea'}
            )
        }


class BlogSearchForm(forms.Form):
    query = forms.CharField()