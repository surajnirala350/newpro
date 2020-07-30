from django.db import models
from Ac_Admin.models import Department_Table


# NGO Table
class NGOS_Table(models.Model):
    ngo_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=1000)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=20)


# Suggestion Table
class Suggestion_Table(models.Model):
    sugs_id = models.AutoField(primary_key=True)
    dept_name = models.ForeignKey(Department_Table,on_delete=models.CASCADE)
    sug_date = models.DateField(auto_now_add=True)
    message = models.TextField()


# Article Table
class Article_Table(models.Model):
    art_id = models.AutoField(primary_key=True)
    art_date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=50)
    message = models.TextField()
    ngo_id = models.ForeignKey(NGOS_Table,on_delete=models.CASCADE)
    approve = models.BooleanField(null=True)