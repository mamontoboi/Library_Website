from django import forms
from .models import Author
from book.models import Book


class AuthorFormModel(forms.ModelForm):
    """Send the data to model Author"""
    # books = forms.ModelMultipleChoiceField(queryset=Book.objects.all(), required=False)

    class Meta:
        model = Author
        fields = ['name', 'surname']

    # patronymic = forms.CharField(required=False)

    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     if self.cleaned_data['patronymic']:
    #         instance.patronymic = self.cleaned_data['patronymic']
    #     else:
    #         instance.patronymic = ''
    #     if commit:
    #         instance.save()
    #     return instance


class UpdateAuthorFormModel(forms.ModelForm):
    """Send the data to model Author"""
    class Meta:
        model = Author
        exclude = ['books']