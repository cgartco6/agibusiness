from django.db import models
from django_cryptography.fields import encrypt

class ClientProject(models.Model):
    project_id = encrypt(models.CharField(max_length=64))
    assets = encrypt(models.JSONField()))
    created_at = models.DateTimeField(auto_now_add=True)
