from django import forms
from .models import Listings, Bids, Comments


class newListingsForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ['title', 'description', 'startingBid', 'category', 'img']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title', 'autofocus': 'autofocus'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Description'}),
            'startingBid': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'id': 'startingbid'}),
            'category': forms.Select(attrs={'class': 'form-select', 'id': 'category'}),
            'img': forms.FileInput(attrs={'class': 'form-control', 'id': 'formFile'})
        }

class newBidsForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ['offers']
        widgets = {
            'offers': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 0})
        }

class newCommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'id': 'exampleFormControlInput3'})
        }