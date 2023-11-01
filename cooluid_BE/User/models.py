from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, custom_user_id, about, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, custom_user_id=custom_user_id, about=about, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, custom_user_id, about, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(self, email, custom_user_id, about, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    custom_user_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    grade = models.PositiveSmallIntegerField(default=10)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default_profile.jpg')
    is_active = models.BooleanField(default=True)
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions')
    about = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.custom_user_id
    

class RegistrationCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)

    def __str__(self):
        return self.email
    
class EmailSignInCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)

    def __str__(self):
        return self.email
    
class Movie(models.Model):
    title = models.CharField(max_length=255)
    movie_code = models.CharField(max_length=255)
    director = models.CharField(max_length=100, blank=True, null=True)
    nation = models.CharField(max_length=100, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    poster_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"



class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    isPublic = models.BooleanField(default=False)
    movie_title = models.CharField(max_length=255)
    movie_director = models.CharField(max_length=255)
    posterurl = models.URLField()  # Store the movie's poster URL
    movieId = models.CharField(max_length=20)  # Store the movie's ID or code
    # Add other fields as needed

    def __str__(self):
        return self.title
