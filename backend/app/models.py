from django.db import models
from django_cryptography.fields import encrypt

class Client(models.Model):
    encrypted_email = encrypt(models.EmailField())
    encrypted_phone = encrypt(models.CharField(max_length=20))
    date_joined = models.DateTimeField(auto_now_add=True)

class Project(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    encrypted_details = encrypt(models.JSONField())
    ai_agents = models.ManyToManyField('AIAgent')
    completed = models.BooleanField(default=False)
