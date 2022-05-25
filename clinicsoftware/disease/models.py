from django.db import models

# Create your models here.
class Disease(models.Model):
    d_name=models.CharField(max_length=30)
    complexity=models.CharField(max_length=30)

    def __str__(self):
        return self.d_name+' '+self.complexity