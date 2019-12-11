
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader

# Create your views here.
import datetime
from django.contrib.auth import authenticate, login, logout

from word_cloub import models


def index(request):
    return render(request, 'index.html')


# 注册
def register(request):
    '''template = loader.get_template('register.html')
    context = {
        'captcha' :CaptchaField(label='验证码'),
    }'''
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        cpassword = request.POST.get('cpwd')
        code = request.POST.get('code')
        # 校验用户名是否重复n
        try:
            user = models.User.objects.get(name=username)
        except models.User.DoesNotExist:
            # 用户名不存在
            user = None
        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})
        if not all([username, password, cpassword]):
            return render(request, 'register.html', {'errmsg': '请完善数据'})
        '''if code != code.captcha:
            return render(request, 'register.html', {'errmsg': '验证码错误'})'''
        new_user = models.User.objects.create()
        new_user.name = username
        new_user.password = password
        new_user.save()
        return render(request, 'index.html')


# 登录
def login_views(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = models.User.objects.get(name=username)
            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return JsonResponse({'res': 1})
            else:
                return JsonResponse({'res': 0})
        except:
            return render(request, 'login.html', {'errmsg': '用户名不存在'})

def logout_views(request):
        if not request.session.get('is_login', None):
            # 如果本来就未登录，也就没有登出一说
            return HttpResponseRedirect("/index/")
        request.session.flush()
        # 或者使用下面的方法
        # del request.session['is_login']
        # del request.session['user_id']
        # del request.session['user_name']
        return HttpResponseRedirect("/index/")


# 关于我们
def about(request):
    return render(request, 'about.html')


# 联系我们
def contact(request):
    return render(request, 'contact.html')


# 主题词云使用说明书
def instruction(request):
    return render(request, 'instruction.html')


# 制作词云
def work(request):
    return render(request, 'work.html')
   #生成词云图片
