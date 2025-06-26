from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class PersonalDetails(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    full_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField()
    email = models.EmailField(unique=False)
    phone = models.CharField(max_length=10)
    aadhar = models.CharField(max_length=12, unique=True)
    photo = models.ImageField(upload_to='photos/')
    password = models.CharField(max_length=20)  # hashed
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name

class Account(models.Model):
    personal = models.OneToOneField(PersonalDetails, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.personal.full_name} - {self.account_number}"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
        ('transfer', 'Transfer'),
    ]
    sender_account = models.ForeignKey(Account, related_name='sender', on_delete=models.CASCADE)
    receiver_account = models.ForeignKey(Account, related_name='receiver', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.transaction_type.title()} - ₹{self.amount}"