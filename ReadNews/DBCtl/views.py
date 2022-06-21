import json
import os
from urllib import response
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core import serializers
from ReadNews import settings
from DBCtl.models import User,Article,NewsType,NewsDetail,News
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
    with open(filePath,'wb') as fp:
        for info in f.chunks():
            fp.write(info)
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
def newstype_add(request):
    # 访问API接口，获取新闻类型
    url = "https://www.mxnzp.com/api/news/types"
    params = {"app_id":"kvdkrgjjtdwadhmi","app_secret":"S01YMmpZMGFjN1JvTFdWUVBLSFM1Zz09"}
    news_type_ret = requests.get(url,params=params)
    news_type = news_type_ret.json()#把response转化为json格式
    data = news_type["data"]#获取data列
    exist_typeId = NewsType.objects.values('typeId')
    #构造一个typeId列表，存放已经在数据有的typeId
    typeId_list = []
    for value in exist_typeId.values():
        typeId_list.append(int(value["typeId"]))#如果不做类型转化，默认添加进去的是str类型，后面获取typeId时拿到的数据是int类型，匹配不上
    # 遍历，判断获取到的id是否已经存在于数据库中，如果有就不进行添加操作
    for i in range(len(data)):
        if data[i]["typeId"] in typeId_list:
            continue
        else:
            typeId = data[i]["typeId"]
            typeName = data[i]["typeName"]
            NewsType.objects.create(typeId=typeId,typeName=typeName)
    return HttpResponse("insert newstype success")

def newstype_select(request):
    json_list = []
    newstypes = NewsType.objects.all()
    print(newstypes)
    # 生成一个列表，列表中的每一个元素都是字典
    for i in newstypes:
        print(model_to_dict(i))
        json_list.append(model_to_dict(i))
    return HttpResponse(json.dumps(json_list), content_type="application/json")

def news_add_typeid(request):
    typeId = request.GET.get("typeId")
    url = "https://www.mxnzp.com/api/news/list"
    params = {"typeId":typeId,"page":"1","app_id":"kvdkrgjjtdwadhmi","app_secret":"S01YMmpZMGFjN1JvTFdWUVBLSFM1Zz09"}
    news_ret = requests.get(url=url,params=params)
    news = news_ret.json()#把response转化为json格式
    print(news)
    if news['code'] == 0 :
        return HttpResponse(news['msg'])
    #data = news["data"]#获取data列
    exist_newsId = News.objects.values('newsId')
    #构造一个newsId列表，存放已经在数据有的newsId
    newsId_list = []
    for value in exist_newsId.values():
        newsId_list.append(value["newsId"])
    # 遍历，判断获取到的id是否已经存在于数据库中，如果有就不进行添加操作
    for i in range(len(news["data"])):
        if news["data"][i]["newsId"] in newsId_list:
            continue
        else:
            newsId = news["data"][i]["newsId"]
            title = news["data"][i]["title"]
            source = news["data"][i]["source"]
            postTime = news["data"][i]["postTime"]
            imgList = news["data"][i]["imgList"][0]
            newsTypeId = NewsType.objects.get(typeId=typeId)
            News.objects.create(newsId=newsId,title=title,source=source,postTime=postTime,imgList=imgList,newsTypeId=newsTypeId)
    return HttpResponse("insert news success")

def news_select_typeid(request):
    typeId = request.GET.get("typeId")
    pagesize = int(request.GET.get("pagesize"))
    offset = int(request.GET.get("offset"))
    json_list = []
    news = News.objects.all().filter(newsTypeId=typeId)[offset:offset+pagesize]
    for i in news:
        json_list.append(model_to_dict(i))#构造字典数组
    return HttpResponse(json.dumps(json_list), content_type="application/json")

def newsdetail_add_newsid(request):
    newsId = request.GET.get("newsId")
    url = "https://www.mxnzp.com/api/news/details"
    params = {"newsId":newsId,"app_id":"kvdkrgjjtdwadhmi","app_secret":"S01YMmpZMGFjN1JvTFdWUVBLSFM1Zz09"}
    news_detail_ret = requests.get(url=url,params=params)
    news_detail = news_detail_ret.json()#把response转化为json格式
    print("news detail:",news_detail)
    if news_detail["code"] == 0:
        return HttpResponse("insert failed")
    data = news_detail["data"]#获取data列
    exist_docid = NewsDetail.objects.values('docid')
    #构造一个docid列表，存已经存在数据库中的newsId，避免重复添加数据
    docid_list = []
    for value in exist_docid.values():
        docid_list.append(value["docid"])
    # 判断获取到的id是否已经存在于数据库中，如果有就不进行添加操作
    if data["docid"] in docid_list:
        return HttpResponse("don't need insert anything")
    else:
        docid = data["docid"]
        images = data["images"]
        title = data["title"]
        source = data["source"]
        content = data["content"]
        ptime = data["ptime"]
        cover = data["cover"]
        newsId = News.objects.get(newsId=newsId)
        NewsDetail.objects.create(docid=docid,images=images,title=title,source=source,content=content,ptime=ptime,cover=cover,newsId=newsId)
        return HttpResponse("insert newsdetail success")

def newsdetail_select_newsid(request):
    newsId = request.GET.get("newsId")
    newsdetail = NewsDetail.objects.get(newsId=newsId)
    json_list = []
    json_list.append(model_to_dict(newsdetail))#构造字典数组
    return HttpResponse(json.dumps(json_list), content_type="application/json")

def user_add(request):
    nickname = request.POST.get("nickname")
    password = request.POST.get("password")
    print("nickname:",nickname,",password:",password)
    User.objects.create(nickname=nickname,password=password)
    return HttpResponse("注册成功,请登录")

def user_login(request):
    nickname = request.POST.get("nickname")
    password = request.POST.get("password")
    try:
        user = User.objects.get(nickname=nickname)
        if user.password == password:
            return HttpResponse("登录成功")
        else:
            return HttpResponse("用户名或密码错误，请重试")
    except:
        return HttpResponse("没有这个用户，请注册")

def user_select(request):
    nickname = request.GET.get("nickname")
    user = User.objects.get(nickname=nickname)
    json_list = []
    json_list.append(model_to_dict(user))
    return HttpResponse(json.dumps(json_list), content_type="application/json")

def user_update(request):
    nickname = request.POST.get("nickname")
    sex = request.POST.get("sex")
    sign = request.POST.get("sign")
    f = request.FILES['avatar']
    filePath = os.path.join(settings.MEDIA_ROOT,f.name)
    with open(filePath,'wb') as fp:
        for info in f.chunks():
            fp.write(info)
    user = User.objects.get(nickname=nickname)
    user.sex = sex
    user.sign = sign
    user.avatar = filePath
    user.save()
    return HttpResponse("update user success")