from django.shortcuts import render
from django.shortcuts import HttpResponse
from sqlite3Exp.models import StudentInfo
# Create your views here.
def addStudent(request):
    name = request.GET.get("name")
    age = request.GET.get("age")
    StudentInfo.objects.create(name=name,age=age)
    return HttpResponse('成功添加一个新的学生')
