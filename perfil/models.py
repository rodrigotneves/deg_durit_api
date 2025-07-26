from django.contrib.auth import get_user_model
from django.db import models

# from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Perfil(models.Model):
    codigo_vendedor = models.CharField(
        "Código do Vendedor", max_length=10, blank=True
    )  # noqa: E501
    user_model = get_user_model()
    user = models.OneToOneField(user_model, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

    def __str__(self):
        nome = f"{self.user.first_name} {self.user.last_name}".strip()
        return nome if nome else self.user.username or self.user.email
