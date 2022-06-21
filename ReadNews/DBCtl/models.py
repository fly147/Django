from django.db import models

# Create your models here.
class Article(models.Model):
    id = models.AutoField(primary_key=True,verbose_name="文章ID")
    articleTitle = models.CharField(max_length=50,verbose_name="文章标题")
    articleContent = models.CharField(max_length=1000,verbose_name="文章内容")
    articleTime = models.CharField(max_length=50,default='',verbose_name="文章发布时间")
    articleImagePath = models.CharField(max_length=100,verbose_name="图片地址")

class NewsType(models.Model):
    typeId = models.CharField(max_length=10,primary_key=True,verbose_name="新闻类型ID")
    typeName = models.CharField(max_length=10,verbose_name="新闻类型名称")

class News(models.Model):
    newsId = models.CharField(max_length=30,primary_key=True,verbose_name="新闻ID")
    title = models.CharField(max_length=100,verbose_name="新闻标题")
    source = models.CharField(max_length=20,verbose_name="新闻来源")
    postTime = models.CharField(max_length=30,verbose_name="新闻发布时间")
    imgList = models.TextField(verbose_name="新闻图片",blank=True)
    digest = models.TextField(verbose_name="新闻摘要")
    newsTypeId = models.ForeignKey(NewsType,on_delete=models.CASCADE)

class NewsDetail(models.Model):
    docid = models.CharField(max_length=30,primary_key=True,verbose_name="新闻唯一ID")
    images = models.TextField(verbose_name="新闻详情图片列表")
    title = models.CharField(max_length=100,verbose_name="新闻标题")
    source = models.CharField(max_length=20,verbose_name="新闻来源")
    content = models.TextField(verbose_name="新闻内容")
    ptime = models.CharField(max_length=30,verbose_name="新闻发布时间")
    cover = models.CharField(max_length=100,verbose_name="新闻封面图片")
    newsId = models.ForeignKey(News,on_delete=models.CASCADE)
