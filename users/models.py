from django.db import models
from django.contrib.auth.models import User
from random import randint

class ConfirmCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="confirmation_code")
    code = models.CharField(max_length=6, blank=True, null=True)


    def generate_code(self):
        self.code = f'{randint(100000, 999999)}'
        self.save()


    def __str__(self):
        return f'{self.user.username} - {self.code}'
