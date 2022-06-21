from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class BaseInfo(APIView):
    def get(self,request): #查询学生信息
        print(request.query_params)
        ret = {'code':101,'message':'query a student successfully'}
        return Response(ret)
    
    def post(self,request): #插入学生信息
        print(request.data)
        ret = {'code':101,'message':'add a student info successfully'}
        return Response(ret)
    
    def put(self,request): #修改学生信息
        print(request.data)
        ret = {'code':101,'message':'update a student info successfully'}
        return Response(ret)
    
    def delete(self,request): #删除学生信息
        print(request.data)
        ret = {'code':101,'message':'delete a student info successfully'}
        return Response(ret)
