from django.db import models

# Create your models here.

class Visit(models.Model):
    username = models.CharField(max_length=200)
    computername = models.CharField(max_length=200)
    ip = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    zip = models.CharField(max_length=200)
    lat = models.CharField(max_length=200)
    lon = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='visit'
        verbose_name_plural='visits'

    def __str__(self):
        return self.username