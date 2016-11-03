from django.conf.urls import include, url

from .views import *

urlpatterns = [
    # 授权
    url(r'^auth/$', AuthView.as_view(), name='wx_auth'),

    # 获取用户信息
    url(r'^code/$', GetUserInfoView.as_view(), name='get_user_info'),

    # 测试
    url(r'^test/$', TestView.as_view(), name='test_view'),

    url(r'^signature/$', signature, name='test_view'),

]