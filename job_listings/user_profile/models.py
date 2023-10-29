from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    link = models.URLField()
    payment = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    

    