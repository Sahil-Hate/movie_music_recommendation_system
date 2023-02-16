from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Emotion(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Movie(models.Model):
    name = models.CharField(max_length=255)
    genre = models.ForeignKey(Emotion,on_delete=models.CASCADE)
    image = models.ImageField()
    url = models.URLField()

    def __str__(self):
        return self.name


class UserEmotion(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    emotion = models.CharField(max_length=255)

    def __str__(self):
        return str(self.user) + "-" + self.emotion


class Song(models.Model):
    name = models.CharField(max_length=255)
    genre = models.ForeignKey(Emotion,on_delete=models.CASCADE)
    image = models.ImageField()
    url = models.URLField()

    def __str__(self):
        return self.name