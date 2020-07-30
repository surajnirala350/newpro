from django.db import models


# Admin table
class Admin_Table(models.Model):
    admin_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=20)


# Department table
class Department_Table(models.Model):
    dept_name = models.CharField(primary_key=True,max_length=30)


# Contact Us Table
class Contact_Us(models.Model):
    name = models.CharField(primary_key=True,max_length=50)
    email = models.EmailField(max_length=100)
    mobile = models.CharField(max_length=15)
    message = models.TextField()
    date = models.DateField(auto_now_add=True)