from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from .forms import PostForm


# Create your views here.
def post_list(request):
    queryset = Post.objects.all()
    paginator = Paginator(queryset, 5)  # show 5 obj per page
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    context = {
        'title': 'list',
        'object_list': objects,
        'page_request_var': page_request_var
    }
    return render(request, 'posts/index.html', context)


def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save()
        messages.success(request, "Successfully Created.")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'title': 'create',
        'form': form
    }
    return render(request, 'posts/post_form.html', context)


def post_detail(request, id=None):
    obj = get_object_or_404(Post, id=id)
    #    print obj.get_absolute_url()
    context = {
        'title': 'detail',
        'object': obj
    }
    return render(request, 'posts/detail.html', context)


def post_update(request, id=None):
    obj = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Successfully Updated.")
        return HttpResponseRedirect(obj.get_absolute_url())
    context = {
        'title': 'detail',
        'object': obj,
        'form': form,
    }
    return render(request, 'posts/post_form.html', context)


def post_delete(request, id):
    obj = get_object_or_404(Post, id=id)
    obj.delete()
    messages.success(request, "Successfully deleted.")
    return redirect("posts:list")
