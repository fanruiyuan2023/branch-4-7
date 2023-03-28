from django.urls import path, re_path
from django.urls import re_path as url
# 从自己的 app 目录引入 views
from .views import *
from .auth import *
from .fileupload import *
from .register import *


urlpatterns = [

    url(r'^login/$', Login.as_view(), name='gdmeta'),
    url(r'^logout/$', Logout.as_view(), name='gdmeta'),
    url(r'^main/$', MainPage.as_view(), name='gdmeta'),
    url(r'^upload/$', Upload.as_view(), name='gdmeta'),
    url(r'^userauth/$', UserAuth.as_view(), name='gdmeta'),
    url(r'^filesubmit/$', FileUpload.as_view(), name='gdmeta'),
    url(r'^loadModule/$', ModulePage.as_view(), name='gdmeta'),
    url(r'^userRegister/$', Register.as_view(), name='gdmeta'),


]