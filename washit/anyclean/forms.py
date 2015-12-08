from django import forms
from allauth.account.forms import SignupForm
 

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=60, required=True)
    last_name = forms.CharField(max_length=60, required=True)
    email = forms.EmailField(required=True)
    mobile = forms.CharField(max_length=10, required=True)


class VerificationForm(forms.Form):
    otp = forms.CharField(max_length=10, required=True)


class MySignupForm(SignupForm):
    first_name = forms.CharField(label=("First Name"),
                               max_length=30,
                               widget=forms.TextInput(
                                   attrs={'placeholder':
                                          ('First Name'),
                                          'autofocus': 'autofocus'}))
    last_name = forms.CharField(label=("Last Name"),
                               max_length=30,
                               widget=forms.TextInput(
                                   attrs={'placeholder': ('Last Name')}))

    def __init__(self, *args, **kwargs):
        super(MySignupForm, self).__init__(*args, **kwargs)

        self.fields['username'] = forms.CharField(label=("Mobile"),
                               max_length=10,
                               min_length=10,
                               widget=forms.TextInput(
                                   attrs={'placeholder': ('Mobile')}))


class SubscriptionForm(forms.Form):
    email = forms.EmailField(required=True)