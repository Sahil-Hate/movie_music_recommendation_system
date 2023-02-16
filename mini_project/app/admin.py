from django.contrib import admin
from .models import Movie,Emotion,UserEmotion,Song

# Register your models here.
admin.site.register(Movie)
admin.site.register(Emotion)
admin.site.register(UserEmotion)
admin.site.register(Song)