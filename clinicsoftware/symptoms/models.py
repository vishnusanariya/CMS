from django.db import models

# Create your models here.
class Symptoms(models.Model):
    s_name=models.CharField(max_length=30)
    complexity=models.CharField(max_length=30)

    def __str__(self):
        return self.s_name+' '+self.complexity