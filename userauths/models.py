from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    id = models.AutoField(primary_key=True)  # Add an id field
    email=models.EmailField(max_length=50,unique=True,null=False)
    username=models.CharField(max_length=50)
    bio=models.CharField(max_length=100)
    is_blocked = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    


    USERNAME_FIELD="email"
    REQUIRED_FIELDS=['username']
    def __str__(self) :
        return self.username
   

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=10, choices=[('HOME', 'Home'), ('WORK', 'Work')])
    first_name = models.CharField(max_length=100,default=None)
    last_name = models.CharField(max_length=100,default=None)
    email = models.CharField(max_length=100,default=None)
    phone = models.CharField(max_length=15,default=None)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)


    def __str__(self):
        return f"{self.address_type} - {self.first_name}"
    

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Wallet for {self.user.username}"

