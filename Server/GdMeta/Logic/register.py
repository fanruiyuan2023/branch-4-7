from django.contrib import auth
import json
from django.http import HttpResponse
from rest_framework.views import APIView
import logging
from .globalobjs import *
from .db_tool import *



class Register(APIView):

    def post(self, request):
        ret = {}
        try:
            userName = request.POST.get("userName");
            password = request.POST.get("password");
            telephoneNum = request.POST.get("telephoneNum");
            sex = 1;
            status = 1;
            sql = "insert into user_info(username, password, telephonenum, sex, status) " \
                  "values('{}','{}','{}',{},{}) ".format(userName, password, telephoneNum, sex, status);
            logging.info(sql);
            db = DbTool(host=host, root=root, pwd=pwd, db_name=db_name)
            num = db.update(sql);
            print(num)
            db.close()
            if num > 0:
                ret["status"] = "success";
            else:
                ret["status"] = "failed";
            ret["userName"] = userName;
        except BaseException as e:
            ret["status"] = "error"
            logging.error(str(e))
            logging.error('任务执行错误', exc_info=True)
        return HttpResponse(json.dumps(ret))