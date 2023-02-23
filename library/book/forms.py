from django import forms
from .models import Book
from author.models import Author


class BookFormModel(forms.ModelForm):
    """Send the data to model Book"""
    authors = forms.ModelChoiceField(queryset=Author.objects.all())

    class Meta:
        model = Book
        fields = ['name', 'description', 'count', 'publication_year', 'id', 'authors']


class UpdateBookModelForm(forms.ModelForm):
    authors = forms.ModelChoiceField(queryset=Author.objects.all())

    class Meta:
        model = Book
        fields = ['name', 'description', 'count', 'publication_year', 'id', 'authors']