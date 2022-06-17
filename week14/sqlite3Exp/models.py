from operator import mod
from django.db import models

# Create your models here.
class StudentInfo(models.Model):
    studentId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    age = models.IntegerField()

class Hobby(models.Model):
    hobbyId = models.AutoField(primary_key=True)
    hobby = models.CharField(max_length=50)
    student = models.ForeignKey(StudentInfo,on_delete=models.CASCADE)
