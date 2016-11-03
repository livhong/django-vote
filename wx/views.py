#encoding=utf-8

import hashlib
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseServerError, Http404
from django.views.generic import View
from django.core.urlresolvers import reverse

from poll.models import User
from .WechatBaseModule import WechatApi
from poll.serializer import UserSerializer

from .base_view import InterceptorView as BaseView

from . import setting

class WechatApiView(View):
    APP_ID = setting.APP_ID
    APP_SECTRET = setting.APP_SECRET
    HOST = setting.HOST
    wechat_api = WechatApi(appid=APP_ID, appsecret=APP_SECTRET)

class AuthView(WechatApiView):
    def get(self, request):
        path = request.GET.get('path')

        if path:
            if 'user' in request.session:
                return redirect(path)
            else:
                red_url = '%s%s?path=%s' % (self.HOST, reverse('wx:get_user_info'), path)
                redirect_url = self.wechat_api.auth_url(red_url)
                # print("-----------------------------------------------------------------------------------------------------------")
                # print(redirect_url)
                # print("-----------------------------------------------------------------------------------------------------------")
                return redirect(redirect_url)
        else:
            return Http404('parameter path not found!')

class GetUserInfoView(WechatApiView):
    def get(self, request):

        redir_url = request.GET.get('path')
        code = request.GET.get('code')

        # print('===========================================================================================================')
        # print(redir_url)
        # print(code)
        # print('===========================================================================================================')

        if redir_url and code:
            token_data, error = self.wechat_api.get_auth_access_token(code)
            if error:
                return HttpResponseServerError('get access_token error')
            user_info, error = self.wechat_api.get_user_info(token_data['access_token'], token_data['openid'])
            if error:
                return HttpResponseServerError('get userinfo error')
            user = self._save_user(user_info)
            if not user:
                return HttpResponseServerError('save userinfo error')
            request.session['user'] = user
            # 跳转回目标页面
            return redirect(redir_url)
        else:
            return Http404('parameter path or code not founded!!')

    def _save_user(self, data):
        user = User.objects.filter(openid=data['openid'])
        # 没有则存储用户数据，有返回用户数据的字典
        if 0 == user.count():
            user_data = {
                'nickname': data['nickname'].encode('iso8859-1').decode('utf-8'),
                'openid': data['openid'],
                'headimgurl': data['headimgurl'],
                'sex': data['sex'],
                'city': data['city'].encode('iso8859-1').decode('utf-8'),
                'country': data['country'].encode('iso8859-1').decode('utf-8')
            }

            if 'unionid' in data:
                user_data.update('unionid', data.unionid)

            try:
                new_user = User(**user_data)
                new_user.save()

                user_data.update({'id': new_user.id})
                return json.dumps(user_data)
                # return user_data
            except Exception as e:
                print(e)

            return None
        else:
            # print(len(user))
            return UserSerializer.toString(user[0])

def signature(request):
    echostr = request.GET['echostr']
    return HttpResponse(echostr)

class TestView(BaseView):
    def get(self, request):
        userStr = request.session['user']
        print('=============================================================================')
        print(userStr)
        print('=============================================================================')
        user = UserSerializer.parse(userStr)
        return render(request, 'polls/test.html', context={'user': user.country})

