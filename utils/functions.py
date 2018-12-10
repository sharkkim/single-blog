import  random
from django.http import HttpResponseRedirect
from backweb.models import UserToken


def get_token():
    s='1234567890qwertyuioplkjhgfdsazxcvbnm'
    token=''
    for _ in range(5):
        token+=random.choice(s)
    return token


#定义登录验证的装饰器
def is_login(func):

    #1、外层函数内嵌内层函数
    def check_status(request):
        token=request.COOKIES.get('token')
        if token:
            user_token=UserToken.objects.filter(token=token).first()
            if  user_token:
                # 3、内层函数调用外层函数的参数
                return func(request)
            else:
                return HttpResponseRedirect('/login/')
        else:
            return HttpResponseRedirect('/login/')

    #2、外层函数返回内层函数
    return check_status

