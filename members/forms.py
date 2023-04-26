from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

        labels = {
            'username': 'Username:',
            'email': 'Email:',
            'first_name': 'First name:',
            'last_name': 'Last name:',
            'password1': 'Password:',
            'password2': 'Password confirmation:'
        }

        help_texts = {
            'username': 'Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.',
            'password1': 'Your password must contain at least 8 characters. Your password can’t be too similar to '
                         'your other personal information. Your password can’t be a commonly used password. Your '
                         'password can’t be entirely numeric.',
        }

        error_messages = {
            'username': {
                'max_length': 'Ensure this value has at most 30 characters.',
            },
        }

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class UserUpdateForm(UserChangeForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    change_password = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    new_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password(self):
        if self.cleaned_data.get('change_password'):
            return self.cleaned_data['password']
        else:
            return None

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'change_password', 'new_password']


