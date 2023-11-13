from django.db import models
from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        superuser = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=30, unique=True, null=False, blank=False)
    email = models.EmailField(
        max_length=30, unique=True, null=False, blank=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'user'
