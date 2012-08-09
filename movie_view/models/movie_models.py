from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=52)
    year = models.CharField(max_length=4)
