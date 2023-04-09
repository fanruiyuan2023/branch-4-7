from django.contrib import auth
import json
from django.http import HttpResponse
from rest_framework.views import APIView
import hashlib
import logging
from .db_tool import *
from .globalobjs import *

class UserAuth(APIView):

    def post(self, request):
        ret = {}
        try:
            user = request.POST.get("user")
            password = request.POST.get("pwd")
            #password = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
            logging.info(user + ',' + pwd)
            sql = "select id from user_info where status=1 and " \
                  "username='{}' and password='{}' ".format(user, password);
            logging.info(sql);
            db = DbTool(host=host, root=root, pwd=pwd, db_name=db_name);
            result = []
            db.select(sql, result);
            print(result)
            db.close()
            if len(result) == 0:
                ret["status"] = "failed";
            elif result[0][0] > 0:
                ret["status"] = "success";
                request.session["userId"] = result[0][0];
                request.session['userName'] = user;
                request.session.set_expiry(3600);           # 一个小时后过期
                ret["userName"] = user;
        except BaseException as e:
            ret["status"] = "error"
            logging.error(str(e))
            logging.error('任务执行错误', exc_info=True)
        return HttpResponse(json.dumps(ret))

# 参考文件：https://blog.csdn.net/m0_58987515/article/details/124972835
# https://blog.csdn.net/adminwg/article/details/126210925