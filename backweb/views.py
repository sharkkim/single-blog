from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from backweb.atcform import AddAtcForm, EditAtcForm
from backweb.models import MyUser, Article


def register(request):
    if request.method == 'GET':
        return render(request,'backweb/register.html')
    elif request.method == 'POST':
        #1、先获取要注册的账号、密码和获取密码
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        #2、判断用户名是否被注册过
        user=MyUser.objects.filter(username=username).first()
        if user:
            warming='该账号已经存在，请更换账号重新执行！'
            return render(request,'backweb/register.html',{'error':warming})

        #3、判断密码和确认密码是否相同
        if password1 and password2:
            if password1!=password2:
                warming='密码不一致，请确认！'
                return render(request,'backweb/register.html',{'error':warming})
            else:
                #4、实现注册，保存数据
                user=MyUser()
                user.username=username
                user.password=password2
                user.save()
                return HttpResponseRedirect('/backweb/login/')
        else:
            data={'error':'密码不能为空！'}
            return  render(request,'backweb/register.html',data)


def login(request):
    if request.method == 'GET':
        return render(request,'backweb/login.html')
    if request.method == 'POST':
        username= request.POST.get('username')
        password1 = request.POST.get('password1')
        user=MyUser.objects.filter(username=username).first()
        if user:
            if user.password==password1:
                #登陆成功
                # -----------------1、使用cookie实现登录-------------------
                # #把标识符存放到登陆成功的账号的cookie当中
                # res=HttpResponseRedirect('/my_index/')
                # t_token=functions.get_token()   #这儿是调用functions文件的get_token()函数生成随机token值
                # res.set_cookie('token',t_token,100)
                #         # res.set_cookie('token','123123',100)
                # #向user_token表中插入或更新数据
                # user_token=UserToken.objects.filter(user_id=user.id).first()
                # if user_token:
                #     user_token.token=t_token
                #     user_token.save()
                # else:
                #     UserToken.objects.create(token=t_token,user_id=user.id)

                # --------------------------2、使用session实现登录--------------------------
                #session值
                request.session['user_id']=user.id

                #跳转页面
                return HttpResponseRedirect('/backweb/index/')
            else:
                data = {'error': '密码错误'}
                return  render(request,'backweb/login.html',data)
        else:
            data = {'error': '账号不存在'}
            return render(request, 'backweb/login.html', data)


def logout(request):
    #退出
    #1、删除cookie中的session值
    #2、或者删除django_session表中的数据
    request.session.flush()
    return HttpResponseRedirect('/backweb/login/')

def index(request):
    return render(request,'backweb/index.html')

def article(request):
    # if request.method=='GET':
        #分页显示信息
        #第一种切片分页
        # page=int(request.GET.get('page',1)) #第一页
        # articles=Article.objects.all()[(page-1)*2:page*2]  #切片分页，每页两个Article对象
        # return render(request,'article.html',{'articles':articles})

        #第二种Paginator方法
        #from django.core.paginator import Paginator
        page = int(request.GET.get('page',1))
        articles = Article.objects.filter(user_id=request.session['user_id'])
        paginator=Paginator(articles,4)
        page=paginator.page(page)
        return render(request,'backweb/article.html',{'page':page})

def add_article(request):
    if request.method=='GET':
        return render(request,'backweb/add-article.html')
    elif request.method == 'POST':
    # title=request.POST.get('title')
    # desc=request.POST.get('desc')
    # content=request.POST.get('content')
    # 把提交的数据丢给表单AddAtcForm验证
        form = AddAtcForm(request.POST, request.FILES)
        # 验证参数是否有效，成功为True，失败为False
        if form.is_valid():
            Article.objects.create(title=form.cleaned_data['title'], keywords=form.cleaned_data['keywords'],
                                   content=form.cleaned_data['content'],user_id=request.session['user_id'])
            return HttpResponseRedirect('/backweb/article/')
        else:
            return render(request, 'backweb/add-article.html', {'form': form})


def update_article(request,id):
    if request.method=='GET':
        article=Article.objects.filter(pk=id).first()
        return render(request,'backweb/add-article.html',{'art':article})
    elif request.method=='POST':
        form=EditAtcForm(request.POST,request.FILES)
        if form.is_valid():
            title=form.cleaned_data['title']
            desc=form.cleaned_data['desc']
            content=form.cleaned_data['content']
            article=Article.objects.filter(pk=id).first()
            article.title=title
            article.desc=desc
            article.content=content
            article.save()
            return HttpResponseRedirect('/backweb/article/')

        else:
            #验证失败
            article=Article.objects.filter(pk=id).first()
            return  render(request,
                           'backweb/add-article.html',
                           {'form':form,'article':article})

def delete_article(request,id):
    if request.method=='GET':
        Article.objects.filter(pk=id).delete()
        return HttpResponseRedirect(reverse('backweb:article'))
