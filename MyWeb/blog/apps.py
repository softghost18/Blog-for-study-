from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'  #应用名称 与创建的应用保持一致
    verbose_name = '我的博客' #WEB站点名称 在admin后台显示该名称
