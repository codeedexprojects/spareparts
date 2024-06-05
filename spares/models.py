from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(email, name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    otp = models.CharField(max_length=32, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    otp_secret_key = models.CharField(max_length=32, blank=True, null=True)



    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    

class VehicleCategories(models.Model):
    Vehicle = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.vehicle

class brands(models.Model):
    vehicle_Brand = models.CharField(max_length=100,null=True)
    vehicle_category = models.ForeignKey(VehicleCategories,on_delete=models.CASCADE)
    is_car = models.BooleanField(default=True)

class Top_categories(models.Model):
    Cat_name = models.CharField(max_length=100,null=True,blank=True)

class partscategory(models.Model):
    v_brand = models.ForeignKey(brands,on_delete=models.CASCADE,null=True)
    v_category = models.ForeignKey(VehicleCategories,on_delete=models.CASCADE,null=True)
    parts_Cat = models.ForeignKey(Top_categories, on_delete=models.CASCADE,null=True)
    part_image = models.ImageField(upload_to='part_images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class Address(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address_line = models.CharField(max_length=255)
    pincode = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    other_details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.full_name} - {self.address_line}, {self.city}, {self.state} - {self.pincode}"
    







