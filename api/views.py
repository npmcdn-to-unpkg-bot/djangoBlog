# -*- coding: utf-8 -*-
from django.shortcuts import render
from blog.models import Article, Tag
from django.http import HttpResponse


# Create your views here.

def get_tag_length(request, tag):
    """
    获取某一个tag下文章的数量
    :param request:
    :param tag:标签
    :return:
    """
    length = Article.objects.filter(tag=tag).count()
    return HttpResponse(length)
