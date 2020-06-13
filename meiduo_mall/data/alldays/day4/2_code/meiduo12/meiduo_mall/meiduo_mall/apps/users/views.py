from django.shortcuts import render,redirect
from django.views import View
from django import http
import re
from meiduo_mall.utils.my_login_required import MyLoginRequiredMiXinView
from .models import User
from django.contrib.auth import authenticate, login,logout
from django_redis import get_redis_connection

class RegisterView(View):
    def get(self,request):
        return render(request,'register.html')

    def post(self,request):
        #1,获取参数
        user_name = request.POST.get("user_name")
        pwd = request.POST.get("pwd")
        cpwd = request.POST.get("cpwd")
        phone = request.POST.get("phone")
        msg_code = request.POST.get("msg_code")
        allow = request.POST.get("allow")

        #2,校验参数
        #2,1 为空校验
        if not all([user_name,pwd,cpwd,phone,msg_code,allow]):
            return http.HttpResponseForbidden("参数不全")

        #2,2 两次密码校验
        if pwd != cpwd:
            return http.HttpResponseForbidden("两次密码不一致")

        #2,3 手机号格式校验
        if not re.match(r'1[3-9]\d{9}',phone):
            return http.HttpResponseForbidden("手机号格式有误")

        #2,4 短信验证码校验
        redis_conn = get_redis_connection("code")
        redis_sms_code = redis_conn.get("sms_code_%s"%phone)
        if not redis_sms_code:
            return http.HttpResponseForbidden("短信验证码已过期")
        if msg_code != redis_sms_code.decode():
            return http.HttpResponseForbidden("短信验证码错误")

        #2,5 协议校验
        if allow != 'on':
            return http.HttpResponseForbidden("必须同意协议")

        #3,创建用户对象,保存到数据库中
        user = User.objects.create_user(username=user_name,password=pwd,mobile=phone)

        #4,返回响应
        response = redirect("http://www.taobao.com")
        return response

class CheckUsernameView(View):
    def get(self,request,username):
        #1,根据用户名,查询用户数量
        count = User.objects.filter(username=username).count()

        #2,返回响应
        data = {
            "count":count
        }
        return http.JsonResponse(data)

class CheckMobileView(View):
    def get(self,request,mobile):
        #1,根据手机号,查询用户数量
        count = User.objects.filter(mobile=mobile).count()

        #2,返回响应
        data = {
            "count":count
        }
        return http.JsonResponse(data)

class LoginUserView(View):
    def get(self,request):
        return render(request,'login.html')

    def post(self,request):
        #1,获取参数
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        remembered = request.POST.get("remembered")

        #2,校验参数
        #2,0 为空校验
        if not all([username,password]):
            return http.HttpResponseForbidden("参数不全")

        #2,1 用户名格式校验
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$',username):
            return http.HttpResponseForbidden("用户名格式有误")

        #2,2 密码格式校验
        if not re.match(r'^[0-9A-Za-z]{8,20}$',password):
            return http.HttpResponseForbidden("密码格式有误")

        #2,3 校验用户名和密码的正确性
        user = authenticate(request, username=username, password=password)

        if not user:
            return http.HttpResponseForbidden("账号或者密码错误")

        #3,状态保持
        login(request, user)

        #3,1设置状态保持的时间
        if remembered == "on":
            request.session.set_expiry(3600*24*2) #两天有效
        else:
            request.session.set_expiry(0)

        #4,返回响应
        response = redirect('/')
        response.set_cookie("username",user.username,3600*24*2)
        return response

class LogoutUserView(View):
    def get(self,request):
        #1,清除session
        logout(request)

        #2,清除cookie
        response = redirect('/')
        response.delete_cookie("username")
        return response

class UserCenterView(MyLoginRequiredMiXinView):

    def get(self,request):
        #方式一:
        #1,判断用户是否登陆了
        # if request.user.is_authenticated:
        #     return render(request, 'user_center_info.html')
        # else:
        #     response = redirect("/login")
        #     response.delete_cookie("username")
        #     return response

        #方式二:
        return render(request, 'user_center_info.html')