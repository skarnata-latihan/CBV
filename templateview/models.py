from django.db import models


# Create your models here.

class Post(models.Model):
    name = models.CharField(max_length=100)
    count = models.IntegerField(null=True)

    def __str__(self):
        return self.name