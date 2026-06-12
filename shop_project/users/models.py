from django.db import models
from django.contrib.auth.models import User

class UserConfirm(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirm')
    code = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.user.username} - {self.code}"