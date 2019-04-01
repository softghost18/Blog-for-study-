from django.contrib import admin

from blog.models import * #import models  it's wrong,why? "models" and "admin" are in the same directory.

# Register your models here.
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	list_display=('title','category','pub_time')

admin.site.register((Category,Tag,Comment))