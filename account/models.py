from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django_countries.fields import CountryField
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Create your models here.


class CustomUser(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=20,
        unique=True,
        help_text=_("Required.20 characters or fewer.\
                Letters and digits only."),
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    
    email = models.CharField(
        _("email address"),
        max_length=30,
        unique=True,
        error_messages={
            "unique": _("A user with that email address already exists."),
        },
    )

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name

    def __str__(self):
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Profile(models.Model):
    """User profile to extend the account profile
    Added images so they can be displayed on the blog if users comment.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    street_address1 = models.CharField(blank=True, max_length=100)
    street_address2 = models.CharField(blank=True, default=00, max_length=100)
    town_or_city = models.CharField(blank=True, max_length=30)
    county = models.CharField(blank=True, default=00, max_length=30)
    postcode = models.CharField(blank=True, max_length=30)
    country = CountryField(blank=True, max_length=30)
    avatar = models.ImageField(blank=True, upload_to='userprofile')

    def image_tag(self):
        if self.avatar:
            return mark_safe(
                '<img src="%s" height="50" width="50">' % self.avatar.url
                )
        return "No image found"

    def __str__(self):
        return self.user.username

    def full_address(self):
        return f'(self.street_address1) (self.street_address2)'
