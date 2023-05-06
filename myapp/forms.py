from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User, DocFile
from django.contrib.auth.password_validation import validate_password


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        validators=[validate_password]
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
        help_text='Enter the same password as above, for verification.'
    )

    class Meta:
        model = User
        fields = ('email', 'full_name', 'address', 'mobile_number', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is already taken.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class DocFileForm(forms.ModelForm):
    class Meta:
        model = DocFile
        fields = ('file',)
        widgets = {
            'file': forms.FileInput()
        }