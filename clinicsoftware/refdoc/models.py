from django.db import models

# Create your models here.
class RefDoc(models.Model):
    name=models.CharField(max_length=50);
    profession=models.CharField(max_length=30);
    address=models.CharField(max_length=100);
    contact=models.IntegerField(null=False);

    def __str__(self):
        return self.name +'\t'+self.profession