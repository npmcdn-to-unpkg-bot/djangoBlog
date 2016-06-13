"""zhaochy_cn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers
from django.contrib.auth import views as auth_views
import views

router = routers.DefaultRouter()
router.register(r'article', views.ArticleViewSet, base_name='ArticleViewSet')

app_name = 'blog'

urlpatterns = [
    url(r'^$', views.blog_list, name='list'),
    url(r'^login$', views.login, name='login'),
    url(r'^detail/(?P<slug>[-\w]+)', views.detail, name='detail'),
    url(r'^filter/(?P<tag>[\w]+)', views.filter, name='filter'),
    url(r'^resume/(?P<slug>[-\w]+)', views.cv, name='cv'),
    # url(r'^api/blog/(?P<pk>[0-9]+)/', views.detail, name='aa'),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^login/$', auth_views.login),
    url(r'^api/', include(router.urls)),
]
