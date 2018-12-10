from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from backweb.models import MyUser


class LoginStatusMiddleware(MiddlewareMixin):

    # ----------------------session-------------------
    #1、获取cookie中的session值
    #2、查询django_session
    def process_request(self,request):
        if request.path in ['/backweb/login/', '/backweb/register/']:
            return None
        user_id=request.session.get('user_id')
        if user_id:
            user=MyUser.objects.filter(pk=user_id).first()
            request.user=user
            return  None
        else:
            return  HttpResponseRedirect('/backweb/login/')
    #-----------------------cookie--------------------
    # def process_request(self,request):
    #     print('test1 request')
    #     #在做登陆和注册时不需要登录校验，否则会报错，说重定向次数过多
    #     if  request.path in['/login/','/register/']:
    #         return None
    #     #登录校验时执行
    #     else:
    #         token = request.COOKIES.get('token')
    #         if token:
    #             user_token = UserToken.objects.filter(token=token).first()
    #             if user_token:
    #                 return None
    #             else:
    #                 return HttpResponseRedirect('/login/')
    #         else:
    #             return HttpResponseRedirect('/login/')

    def process_response(self,request,response):
        return response