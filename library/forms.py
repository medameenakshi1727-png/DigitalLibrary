from django import forms
from .models import Book, Member


class BookSearchForm(forms.Form):
    q = forms.CharField(required=False, label="Search books", widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Title, author, or genre"}
    ))


class IssueBookForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Book.objects.none(), widget=forms.Select(attrs={"class": "form-select"}))
    member = forms.ModelChoiceField(queryset=Member.objects.all(), widget=forms.Select(attrs={"class": "form-select"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["book"].queryset = Book.objects.filter(available_copies__gt=0)


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ["name", "member_id", "email", "phone"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "member_id": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
        }
