from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import RegexValidator
# from phonenumber_field.modelfields import PhoneNumberField
from .managers import UserManager
from ProjectDeskSolutions3 import settings


class Organization(models.Model):
    title = models.CharField(verbose_name="Name of Organization",
                             max_length=50, unique=True, blank=False, null=False)
    description = models.TextField(verbose_name="Describe your Organization")
    url = models.URLField(verbose_name="Organization URL",
                          null=True, blank=True, default=None)

    def __str__(self):
        return self.title


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name="Email",
                              unique=True, null=False, blank=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    # Register form se admin hi create hoga organization ka
    is_admin = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey(
        Organization, verbose_name="Organization", on_delete=models.CASCADE, null=True, blank=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True

    def get_group_permissions(self, obj):
        querset = User.objects.get(id=obj.id)
        return querset

    @property
    def get_user(self):
        return self.email

# CompanyAdmins can then add their own departments, or add new users to their system but after adding departments


class Department(models.Model):
    department_name = models.CharField(
        max_length=60, null=False, blank=False, verbose_name="Department Name")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Added By", null=False, blank=True)

    def __str__(self):
        return self.department_name


class Profile(models.Model):
    # change this to user
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, null=False)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True, blank=False)
    address = models.TextField(verbose_name="Address", default=None)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(max_length=13, validators=[
                             phone_regex], blank=True)
    is_manager = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)
