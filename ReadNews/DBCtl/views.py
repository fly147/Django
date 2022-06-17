import json
import os
from urllib import response
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core import serializers
from ReadNews import settings
from DBCtl.models import Article,NewsType,NewsDetail,News
from django.forms.models import model_to_dict
import requests

# Create your views here.
#往文章表插入一条新数据
def article_insert(request):
    articleTitle = request.POST.get("articleTitle")
    articleContent = request.POST.get("articleContent")
    articleTime = request.POST.get("articleTime")
    f = request.FILES['uploadedfile']
    filePath = os.path.join(settings.MEDIA_ROOT,f.name)
    with open(filePath,'wb') as fp:
        for info in f.chunks():
            fp.write(info)
    Article.objects.create(articleTitle=articleTitle,articleContent=articleContent,articleTime=articleTime,articleImagePath=filePath)
    return HttpResponse("insert success")

# 文章表分页查询
def article_select_page(request):
    pagesize = int(request.GET.get("pagesize"))
    offset = int(request.GET.get("offset"))
    json_list = []
    articles = Article.objects.all()[offset:offset+pagesize]
    for i in articles:
        json_list.append(model_to_dict(i))
    return HttpResponse(json.dumps(json_list), content_type="application/json")

# 文章表通过ID查询
def article_select_id(request):
    id = int(request.GET.get("id"))
    article = Article.objects.filter(id=id).first()
    json_list = []
    json_list.append(model_to_dict(article))
    return HttpResponse(json.dumps(json_list),content_type="application/json")

# 文章表更新数据
def article_update(request):
    id = int(request.POST.get("id"))
    articleTitle = request.POST.get("articleTitle")
    articleContent = request.POST.get("articleContent")
    articleTime = request.POST.get("articleTime")
    f = request.FILES['picture']
    filePath = os.path.join(settings.MEDIA_ROOT,f.name)
    print(filePath)
    obj = Article.objects.get(id=id)
    obj.articleTitle = articleTitle
    obj.articleContent = articleContent
    obj.articleTime = articleTime
    obj.articleImagePath = filePath
    obj.save()
    return HttpResponse("update success")

# 文章表通过ID删除一条记录
def article_delete(request):
    id = int(request.GET.get("id"))
    Article.objects.filter(id=id).delete()
    return HttpResponse("delete success")

# 新闻类型表新增记录
def NewsType_add(request):
    url = "https://www.mxnzp.com/api/news/types"
    params = {"app_id":"kvdkrgjjtdwadhmi","app_secret":"S01YMmpZMGFjN1JvTFdWUVBLSFM1Zz09"}
    news_type_ret = requests.get(url,params=params)
    news_type = news_type_ret.json()
    data = news_type["data"]
    exist_typeId = NewsType.objects.values('typeId')
    for i in range(len(data)):
        if exist_typeId:
            continue
        else:
            typeId = data[i]["typeId"]
            typeName = data[i]["typeName"]
            NewsType.objects.create(typeId=typeId,typeName=typeName)
    return HttpResponse("insert newstype success")