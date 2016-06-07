from __future__ import unicode_literals
from django.utils.encoding import smart_unicode
from django.db import models
from zcy_md.models import MarkdownField


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=200, primary_key=True)

    def __unicode__(self):
        return smart_unicode(self.name)

    # def __str__(self):
        # print smart_unicode(self.name)
        # return smart_unicode(self.name)


        # class Meta:
        #     def get_Article_num(self):
        #         return Article.objects.filter(tag=self.name).count()


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = MarkdownField()
    slug = models.SlugField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    tag = models.ForeignKey('blog.Tag', on_delete=models.SET_NULL, null=True)

    def __unicode__(self):
        return smart_unicode(self.title)

    class Meta:
        ordering = ['-modified']


class Resume(models.Model):
    title = models.CharField(max_length=200)
    content = MarkdownField()
    slug = models.SlugField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return smart_unicode(self.title)
