from django.db import models
import uuid

class Book(models.Model):
    uid = models.CharField(unique=True, default=str(uuid.uuid4()))
    title = models.CharField()
    author = models.CharField(null=True, blank=True)
