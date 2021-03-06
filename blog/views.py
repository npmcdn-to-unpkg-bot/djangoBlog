# coding=utf8

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
import datetime
from rest_framework import viewsets
from serializers import ArticleSerializer
from models import *


# Create your views here.

def index(request):
    return render(request, 'blog/index.html')


def blog_list(request):
    """
    blog index
    获取博客的文章列表
    """
    now = datetime.datetime.now()
    queryset = Article.objects.all().filter(publish=True)
    paginator = Paginator(queryset, 5)  # show 5 obj per page
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    tags = Tag.objects.all()
    context = {
        "object_list": objects,
        "tags": tags,
        'page_request_var': page_request_var
    }
    return render(request, 'blog/list.html', context)


def filter(request, tag=None):
    tags = Tag.objects.all()
    # start_date = datetime.date(2016, 5, 30)
    # end_date = datetime.date(2016, 6, 30)
    queryset = Article.objects.filter(tag=tag, publish=True).order_by('created')
    # print Tag.objects.filter(name=tag).count()
    # print queryset.count()
    context = {
        "object_list": queryset,
        "tags": tags
    }
    return render(request, 'blog/list.html', context)


def login(request):
    # if request.user.is_authenticated()
    if request.method == 'GET':
        return render(request, 'blog/login.html')
    elif request.method == 'POST':
        return render(request, 'blog/index.html')


def detail(request, slug):
    # print slug
    try:
        obj = Article.objects.get(slug=slug, publish=True)
        # print obj.get_absolute_url()
    except Exception, e:
        print (e.message)
        # return render(request,)
        return render(request, 'blog/list.html')
    context = {
        "object": obj
    }
    return render(request, 'blog/detail.html', context)


def cv(request, slug):
    queryset = Resume.objects.all()
    try:
        obj = Resume.objects.get(slug=slug)
    except Exception, e:
        return render(request, 'blog/list.html')
    context = {
        "object": obj
    }
    return render(request, 'blog/detail.html', context)


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.all()
