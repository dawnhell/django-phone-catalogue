from django.db import models


class Phone(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=200)
    price = models.IntegerField(default=100)
    deviceType = models.CharField(max_length=200)
    os = models.CharField(max_length=200)
    imageUrl = models.CharField(max_length=200)
    description = models.CharField(max_length=500)


class Color(models.Model):
    code = models.CharField(max_length=100)
