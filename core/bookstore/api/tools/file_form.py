from django import forms
from bookstore.models.book import Book

class BookAdminForm(forms.ModelForm):
    book_file = forms.FileField(required=False)

    class Meta:
        model = Book
        fields = '__all__'
