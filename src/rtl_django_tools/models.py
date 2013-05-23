"""
In order to have a user model that uses an email address as the primary
identify but which does not have a `username` field, we have to extend
the `AbstractBaseUser` and re-implement much of what is in `AbstractUser`
with the exception of the `username`.

This feels a bit poor - it's a copy/paste/modify operation, but we didn't
find a more elegant solution.

This model therefore provides a `AbstractBasicUser` class which provides
all of the standard Django User class fields with the exception of
`username` and with the `email` field being primary.

We create a concrete `User` to implement this and `forms.py` and `admin.py`
work with this.

The abstract class means we can easily create other user models from this
one.
"""
import warnings
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin,
                                        SiteProfileNotAvailable)
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _


class BasicUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a BasicUser with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email address must be set')
        email = BasicUserManager.normalize_email(email)
        user = self.model(email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


@python_2_unicode_compatible
class AbstractBasicUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions but WITHOUT a username field.

    Email and password are required. Other fields are optional. Email is the
    USERNAME_FIELD.

    The contents are largely copied from Django's AbstractUser with the
    removal of `username`. This makes it easier to create applications that
    make exclusive use of the email address as the primary user identifier.
    """
    email = models.EmailField(('email address'),
                              blank=True, unique=True, max_length=254)
    first_name = models.CharField(('first name'), max_length=30, blank=True)
    last_name = models.CharField(('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(('staff status'), default=False,
                                   help_text=('Designates whether the user '
                                              'can log into this admin '
                                              'site.'))
    is_active = models.BooleanField(
        ('active'), default=True,
        help_text=('Designates whether this user should be treated as '
                   'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(('date joined'), default=timezone.now)

    objects = BasicUserManager()

    USERNAME_FIELD = 'email'
#    REQUIRED_FIELDS not defined because email and password already mandatory

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    def __unicode__(self):
        return str(self).encode('utf-8')

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def get_profile(self):
        """
        Returns site-specific profile for this user. Raises
        SiteProfileNotAvailable if this site does not allow profiles.
        """
        warnings.warn("The use of AUTH_PROFILE_MODULE to define user profiles "
                      "has been deprecated.",
                      PendingDeprecationWarning)
        if not hasattr(self, '_profile_cache'):
            from django.conf import settings
            if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
                raise SiteProfileNotAvailable(
                    'You need to set AUTH_PROFILE_MODULE in your project '
                    'settings')
            try:
                app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
            except ValueError:
                raise SiteProfileNotAvailable(
                    'app_label and model_name should be separated by a dot in '
                    'the AUTH_PROFILE_MODULE setting')
            try:
                model = models.get_model(app_label, model_name)
                if model is None:
                    raise SiteProfileNotAvailable(
                        'Unable to load the profile model, check '
                        'AUTH_PROFILE_MODULE in your project settings')
                self._profile_cache = \
                    model._default_manager.using(self._state.db).get(
                        user__id__exact=self.id)
                self._profile_cache.user = self
            except (ImportError, ImproperlyConfigured):
                raise SiteProfileNotAvailable
        return self._profile_cache


class User(AbstractBasicUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Email and password are required. Other fields are optional.

    A straight copy with change of base class of Django's User model.
    """
    class Meta:
        swappable = 'AUTH_USER_MODEL'
