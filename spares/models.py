from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings




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
    full_name = models.CharField(max_length=255, blank=True,)
    phone_number = models.CharField(max_length=20, blank=True,)
    address_line = models.CharField(max_length=255,  blank=True,)
    pincode = models.CharField(max_length=20, blank=True,)
    state = models.CharField(max_length=100, blank=True,)
    city = models.CharField(max_length=100, blank=True,)



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
    Brand_logo = models.ImageField(upload_to='part_images/', null=True, blank=True)
    is_car = models.BooleanField(default=True)

class Top_categories(models.Model):
    Cat_name = models.CharField(max_length=100,null=True,blank=True)

class partscategory(models.Model):
    v_brand = models.ForeignKey(brands,on_delete=models.CASCADE,null=True)
    v_category = models.ForeignKey(VehicleCategories,on_delete=models.CASCADE,null=True)
    parts_name = models.CharField(max_length=100,null=True,blank=True)
    parts_Cat = models.ForeignKey(Top_categories, on_delete=models.CASCADE,null=True)
    part_image = models.ImageField(upload_to='part_images/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_offer = models.BooleanField(default=False)
    product_rating = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(1.0), MaxValueValidator(5.0)], default=1)




    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(partscategory, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    part = models.ForeignKey(partscategory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.part.parts_name} (x{self.quantity}) in {self.user.name}'s cart"
    


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    part = models.ForeignKey(partscategory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    ordered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')








