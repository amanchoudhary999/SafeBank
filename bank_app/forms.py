from django import forms
from .models import PersonalDetails
from django.forms.widgets import DateInput

class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(),required=True)

    class Meta:
        model = PersonalDetails
        fields = ['full_name', 'gender', 'dob', 'email', 'phone', 'aadhar', 'photo', 'password']
        widgets = {
            'dob': DateInput(attrs={'type': 'date'}),
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    

class LoginForm(forms.Form):
    account_number = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())

class PasswordConfirmForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), label="Enter your password")

class TransferForm(forms.Form):
    receiver_account = forms.CharField(
        max_length=20,
        label="Receiver Account Number"
    )
    amount = forms.DecimalField(
        min_value=1,
        max_digits=10,
        decimal_places=2,
        label="Amount to Transfer",
        widget=forms.NumberInput(attrs={'inputmode': 'decimal', 'step': '0.01'})
    )
class WithdrawForm(forms.Form):
    amount = forms.DecimalField(min_value=1, max_digits=10, decimal_places=2, label="Amount")

class DepositForm(forms.Form):
    amount = forms.DecimalField(
        min_value=1,
        max_digits=10,
        decimal_places=2,
        label="Amount to Deposit",
        widget=forms.NumberInput(attrs={'inputmode': 'decimal', 'step': '0.01'})
    )