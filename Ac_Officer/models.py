from django.db import models
from Ac_Admin.models import Department_Table


# Officer Table
class Officer_Table(models.Model):
    officer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    dept_name = models.ForeignKey(Department_Table, on_delete=models.CASCADE)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=20)
    otp = models.CharField(max_length=10,default=False)
    status = models.CharField(max_length=20,default=False)
