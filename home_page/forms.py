from django import forms


class SingIn(forms.ModelForm):
    e_mail = forms.CharField(label='E-mail', max_length=20)
    password = forms.CharField(label='Password', max_length=20)


class SignUp(forms.ModelForm):
    nickaname = forms.CharField(label='Nickname', max_length=20)
    e_mail = forms.CharField(label='E_mail', max_length=20)
    password = forms.CharField(label='Password', max_length=20)
    password2 = forms.CharField(label='Confirm', max_length=20)