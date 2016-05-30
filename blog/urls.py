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
from django.conf.urls import url
import views

app_name = 'blog'

urlpatterns = [
    # url(r'^$', views.index, name='blog_index'),
    # url(r'^index$', views.index, name='index'),
    url(r'^$', views.blog_list, name='list'),
    url(r'^login$', views.login, name='login'),
    url(r'^detail/(?P<slug>[-\w]+)', views.detail, name='detail'),
    url(r'^filter/(?P<tag>[\w]+)', views.filter, name='filter'),
]
