from django.contrib import admin
from blog.models import Article, Tag
from zcy_md.admin import MarkdownModelAdmin


# Register your models here.


class ArticleAdmin(MarkdownModelAdmin):
    list_display = ("title", "tag", "created", "modified")
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
