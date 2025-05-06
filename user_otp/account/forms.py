from django import forms
from account.models import CustomUser

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'mobile', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")


class OtpVerificationForm(forms.Form):
    email_otp = forms.CharField(max_length=6, label="Email OTP")
    mobile_otp = forms.CharField(max_length=6, label="Mobile OTP")


class LoginForm(forms.Form):
    identifier = forms.CharField(label="Username / Email / Mobile")
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    otp = forms.CharField(required=False)
    login_type = forms.ChoiceField(
        choices=[
            ('password', 'Password Login'), 
            ('otp', 'OTP Login')
        ],
        widget=forms.RadioSelect
    )
