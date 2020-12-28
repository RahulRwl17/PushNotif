from django.db import models

# Create your models here.


class Hospital(models.Model):
    ID = models.AutoField(primary_key=True)
    Hospital_Name = models.CharField(max_length=50)
    Latitude = models.CharField(max_length=10)
    Longitude = models.CharField(max_length=10)
    Location = models.CharField(max_length=100)
    zipcode = models.IntegerField(max_length=6,null=True)

    def __str__(self):
        return self.Hospital_Name

class AccidentReq(models.Model):
    AID = models.AutoField(primary_key=True)
    DeviceID = models.IntegerField(default='1')
    UserName = models.CharField(max_length=20)
    Latitude = models.CharField(max_length=30)
    Longitude =  models.CharField(max_length=30)
    Time = models.TimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.UserName

class Login(models.Model):
    LID = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=15)
    password = models.TextField(max_length=8)

    def __str__(self):
        return self.user_name