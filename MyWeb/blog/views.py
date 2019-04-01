from django.shortcuts import render
from django.views.generic import ListView,DetailView
from blog.models import *
from django.db.models import Q  # 帮助完成查询条件设置
from blog.forms import CommentForm
from django.shortcuts import HttpResponse


# Create your views here.
class Index(ListView):
    model = Article
    template_name = 'index.html'
    queryset = Article.objects.all().order_by('-id')  # 获取到全部文章并按编号降序排列。
    paginate_by = 5  # 设置分页时每页的文章数量

class CategoryList(ListView):
    model = Article
    template_name = 'category.html'
    paginate_by = 5

    def get_queryset(self):  # 定义通过分类查询的QuerySet
        return Article.objects.filter(category=self.kwargs['category']).order_by('-id')  # 按参数传入的分类id进行查询并按文章编号降序排序

    def get_context_data(self, **kwargs):  # 增加额外要传递给模板的数据
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(id=self.kwargs['category'])  # 通过分类id查询分类对象
        context['category'] = category.name  # 将分类对象的名称存入传递给模板的数据中
        return context


class Search(ListView):
    model = Article
    template_name = 'search.html'
    paginate_by = 5

    def get_queryset(self):
        SearchKey = self.request.GET['SearchKey']  # 获取查询关键字
        if SearchKey:
            return Article.objects.filter(Q(title__icontains=SearchKey) | Q(content__icontains=SearchKey)).order_by('-id')
            # 查询标题或者内容包含关键字的数据对象
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = self.request.GET['SearchKey'] # 获取关键字存入传入模板的数据中
        return context


class ArticleDetail(DetailView):
    model = Article
    template_name = 'detail.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(article=self.kwargs['pk']) # 通过文章id查询评论内容
        context['comment_list'] = self.comment_sort(comments) # 将排序归类后的文章列表存入传送到模板的数据中
        comment_form = CommentForm()  # 创建评论表单对象
        context['comment_form'] = comment_form  # 将表单对象传送到模板的数据中
        try:
            context['session']={
                'name':self.request.session['name'],
                'email':self.request.session['email'],
                'content':self.request.session['content']
            }
        except:
            pass
        return context

    # 对评论进行排序（顶级评论按时间排序，回复评论按根据所属评论按时间排序）
    def comment_sort(self, comments):  
        self.comment_list = []  # 排序后的评论列表
        self.top_level = []  # 顶级评论列表
        self.sub_level = {}  # 回复评论字典（按所属评论构建字典）
        for comment in comments:  # 遍历所有评论
            if comment.reply == None:  # 如果没有回复目标
                self.top_level.append(comment)  # 存入顶级评论列表
            else:  # 否则
                self.sub_level.setdefault(comment.reply.id, []).append(comment)  # 以回复目标（父级评论）的id为key存入字典
        for top_comment in self.top_level:  # 遍历顶级评论
            self.format_show(top_comment)  # 将该顶级评论及其所有后代，即衍生的评论，加入最终评论列表
        return self.comment_list  # 返回最终的评论列表

    # 递归函数（将参数评论加入最终列表；如果其没有回复评论则跳出，否则获取其回复评论并遍历、递归） similar to tree
    def format_show(self, top_comment):  
        self.comment_list.append(top_comment)  # 将参数评论存入列表
        try:
            self.kids = self.sub_level[top_comment.id]  # 获取参数评论的所有回复评论
        except KeyError:  # 如果不存在回复评论
            pass  # 结束递归
        else:  # 否则
            for kid in self.kids:  # 遍历回复评论
                self.format_show(kid)  # 进行下一层递归（将参数评论加入最终列表，获取其所有回复评论，遍历递归）



def pub_comment(request):  # 发布评论函数
    if request.method == 'POST':  # 如果是post请求
        request.session['name']=request.POST.get('name')
        request.session['email']=request.POST.get('email')
        comment = Comment()  # 创建评论对象
        comment.article = Article.objects.get(id=request.POST.get('article'))  # 设置评论所属的文章
        if request.POST.get('reply') != '0':  # 如果回复的不是文章而是他人评论
            comment.reply = Comment.objects.get(id=request.POST.get('reply'))  # 设置回复的目标评论
        form = CommentForm(request.POST, instance=comment)  # 将用户的输入和评论对象结合为完整的表单数据对象
        #form = CommentForm(request.POST)
        if form.is_valid():  # 如果表单数据校验有效
            try:
                form.save()  # 将表单数据存入数据库
                result = '200'  # 提交结果为成功编码
                request.session['content']=""
            except:  # 如果发生异常
                result = '100'  # 提交结果为失败编码
                request.session['content']=request.POST.get('content')

        else:  # 如果表单数据校验无效
            result = '100'  # 提交结果为失败编码
        return HttpResponse(result)  # 返回提交结果到页面
    else:  # 如果不是post请求
        return HttpResponse('非法请求！')  # 返回提交结果到页面