import django.contrib.auth.models
import django.db.models



class UserManager(django.contrib.auth.base_user.BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password .
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(django.contrib.auth.models.AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    email = django.db.models.EmailField(
        'email',
        unique=True,
        help_text='Must be a valid email address.',
        error_messages={
            'unique': 'A user with that email already exists.',
        },
    )
