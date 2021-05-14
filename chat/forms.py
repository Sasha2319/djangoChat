from django import forms

class SignUpForm(forms.Form):
    email = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'id': 'SignUpEmail'}))
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id': 'SignUpName'}))
    password = forms.CharField(min_length=8, max_length=20, widget=forms.PasswordInput(attrs={'id': 'SignUpPassword'}))
    dateOfBirth = forms.DateField(label='Date of Birth', required=False, widget=forms.DateInput(attrs={'type': 'date', 'id': 'SingUpDate'}))

class LoginForm(forms.Form):
    loginName = forms.CharField(max_length=50, label='Name', widget=forms.TextInput(attrs={'id': 'LoginName'}))
    loginPassword = forms.CharField(min_length=8, label='Password', max_length=20, widget=forms.PasswordInput(attrs={'id': 'LoginPassword'}))

class ChatIdForm(forms.Form):
    chatId = forms.CharField(max_length=50, label='Chat Id', widget=forms.TextInput)