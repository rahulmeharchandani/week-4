from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    marks = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

# Create your models here.
