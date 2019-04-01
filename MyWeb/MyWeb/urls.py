"""MyWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.static import serve

from MyWeb import settings
from blog import views as blog_view



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', blog_view.Index.as_view()),
    path('category/<int:category>', blog_view.CategoryList.as_view(), name='category'),
    path('search/', blog_view.Search.as_view(), name='search'),
    path('detail/<int:pk>', blog_view.ArticleDetail.as_view(), name='detail'),
    path('comment/', blog_view.pub_comment, name='comment'),

    path('summernote/', include('django_summernote.urls')),
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),  # 用于上传图片文件
    #path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),  # 用于加载静态文件

]
