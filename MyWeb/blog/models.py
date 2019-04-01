from django.db import models
from django.contrib.auth.models import User
from django_summernote.fields import SummernoteTextField

# Create your models here.
class Category(models.Model): 
	id=models.IntegerField(primary_key=True)
	name=models.CharField('类别',max_length=20,unique=True)

	class Meta:
		verbose_name=verbose_name_plural='类别'

	def __str__(self):
		return self.name

class Tag(models.Model):
	name=models.CharField('标签',max_length=20,unique=True)

	class Meta:
		verbose_name=verbose_name_plural='标签'

	def __str__(self):
		return self.name

class Article(models.Model):
	id=models.AutoField(primary_key=True)
	author=models.ForeignKey(User,on_delete=models.DO_NOTHING,verbose_name='作者')  #关系及约束：文章与作者是多对一的关系，作者删了，文章不删
	title=models.CharField('标题',max_length=50)
	content=SummernoteTextField('内容')
	pub_time=models.DateField('日期',auto_now=True)
	category=models.ForeignKey(Category,on_delete=models.SET_DEFAULT,default=1,verbose_name='类别') #关系及约束：文章与类别是多对一的关系，类别删了，文章变为默认类别“未分类”
	tag=models.ManyToManyField(Tag,verbose_name='标签') #关系及约束：文章与标签是多对多的关系

	class Meta:
		verbose_name=verbose_name_plural='文章'

	def __str__(self):
		return self.title

class Comment(models.Model):
	id=models.AutoField(primary_key=True)
	name=models.CharField('昵称',max_length=20)
	email=models.EmailField('邮箱')
	content=models.TextField('内容')
	publish=models.DateField('时间',auto_now=True)
	article=models.ForeignKey(Article, on_delete=models.CASCADE,verbose_name='文章') #关系及约束：评论与文章是多对一的关系，文章删了，相关评论也删除
	reply=models.ForeignKey('self',on_delete=models.DO_NOTHING,null=True, blank=True, verbose_name='回复') #关系及约束：评论与回复是一对多的关系，回复删除，评论不删

	class Meta:
		verbose_name=verbose_name_plural='评论'

	def __str__(self):
		return self.content