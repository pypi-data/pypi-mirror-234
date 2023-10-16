from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, username=None, **extra_fields):
        if not email:
            raise ValueError('The email must be set')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, username=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, username, **extra_fields)

    def create_superuser(self, email, password, username=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, username, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = 'accrete_user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        verbose_name=_('Username'),
        max_length=150,
        help_text=_(
            '150 characters or fewer.'
            'Letters, digits and @/./+/-/_ only.'
        ),
        blank=True,
        null=True,
        validators=[username_validator],
    )

    first_name = models.CharField(
        verbose_name=_('First Name'),
        max_length=150,
        blank=True,
        null=True
    )

    last_name = models.CharField(
        verbose_name=_('Last Name'),
        max_length=150,
        blank=True,
        null=True
    )

    email = models.EmailField(
        verbose_name=_('Email Address'),
        unique=True
    )

    is_staff = models.BooleanField(
        verbose_name=_('Staff Status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into the admin site.'
        ),
    )

    is_active = models.BooleanField(
        verbose_name=_('Active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active.\n'
            'Unselect this instead of deleting accounts.'
        ),
    )

    date_joined = models.DateTimeField(
        verbose_name=_('Date Joined'),
        default=timezone.now
    )

    language_code = models.CharField(
        verbose_name=_('Language'),
        max_length=10,
        null=True,
        blank=True
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username or self.email
