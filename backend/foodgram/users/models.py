from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


# Create your models here.
class User(AbstractUser):
    """Кастомная модель пользователя"""

    username = models.CharField(
        verbose_name="имя пользователя",
        max_length=150,
        validators=[
            RegexValidator(regex=r"^[\w.@+-]+$"),
        ],
    )
    email = models.EmailField(
        verbose_name="E-Mail",
        max_length=254,
    )
    first_name = models.CharField(
        verbose_name="имя",
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name="фамилия",
        max_length=150,
    )
    avatar = models.ImageField(
        verbose_name="аватар",
        upload_to="users/",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = ["username"]
        constraints = [
            models.UniqueConstraint(
                fields=["email"],
                name="unique_email",
            ),
            models.UniqueConstraint(
                fields=["username"],
                name="unique_username",
            ),
        ]

    def __str__(self):
        return self.username
