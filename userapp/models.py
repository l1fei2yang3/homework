from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=20)
    name=models.CharField(max_length=20)
    pwd=models.CharField(max_length=20)
    gender=models.BooleanField()
    class Meta:
        db_table="t_user"
