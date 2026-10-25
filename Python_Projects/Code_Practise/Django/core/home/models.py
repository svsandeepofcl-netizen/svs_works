import uuid

from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=100)
    age=models.IntegerField()
    gender=models.CharField(max_length=10, default='male')
    email=models.EmailField(max_length=254)
    address=models.TextField(max_length=1000)
    description=models.TextField(max_length=1000, default='Default Data')
    slugField=models.SlugField(default='0x0x0x0')
    UID=models.UUIDField(default=uuid.uuid4)
    fileUpload=models.FileField(upload_to='uploads/', default='uploads/')