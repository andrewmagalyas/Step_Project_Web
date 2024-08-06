from django.db import models
from django.contrib.auth.models import User


class SearchHistory(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    description = models.CharField(max_length=255)
    humidity = models.IntegerField()
    search_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} - {self.user.username}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username



