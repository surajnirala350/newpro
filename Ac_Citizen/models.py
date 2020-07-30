from django.db import models


# Citizen Table
from Ac_Admin.models import Department_Table


class Citizen_Table(models.Model):
    citz_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    address = models.TextField()
    gender = models.CharField(max_length=10)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    otp = models.CharField(max_length=20,default=False)
    status = models.CharField(max_length=20,default=False)


# Complaint Table
class Complaint_Table(models.Model):
    comp_id = models.AutoField(primary_key=True)
    dept_name = models.ForeignKey(Department_Table,on_delete=models.CASCADE)
    citz_id = models.ForeignKey(Citizen_Table,on_delete=models.CASCADE)
    cmp_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20,null=True)
    message = models.TextField()
    image = models.ImageField(upload_to='complaints',default=False)
    close_date = models.DateField(null=True)


# Feedback table
class Feedback_Table(models.Model):
    feed_id = models.AutoField(primary_key=True)
    citz_id = models.ForeignKey(Citizen_Table,on_delete=models.CASCADE)
    dept_name = models.ForeignKey(Department_Table,on_delete=models.CASCADE)
    feed_date = models.DateField(auto_now_add=True)
    feed_message = models.TextField()
    image = models.ImageField(upload_to='feedbacks',default=False)


# Reject Table
class Reject_Table(models.Model):
    reject_id = models.AutoField(primary_key=True)
    citz_id = models.ForeignKey(Citizen_Table,on_delete=models.CASCADE)
    message = models.TextField()
    rej_date = models.DateField(auto_now_add=True)


# Reply Table
class Reply_Table(models.Model):
    reply_id = models.AutoField(primary_key=True)
    feed_id = models.ForeignKey(Feedback_Table, on_delete=models.CASCADE)
    message = models.TextField()
    rep_date = models.DateField(auto_now_add=True)
