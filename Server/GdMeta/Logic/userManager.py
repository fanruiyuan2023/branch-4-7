from django.contrib import auth
import json
from django.http import HttpResponse
from rest_framework.views import APIView
import logging
from .globalobjs import *
from .db_tool import *



class UserManager(APIView):


    def post(self, request):
        ret = {}
        try:
            userName = request.POST.get("userName");
            status = request.POST.get("status");

            sql = "select id,username,telephonenum,status from user_info where 1=1";
            if userName.strip() != "":
                sql = sql + " and username like '%{}%'".format(userName);
            if status.strip() != "":
                sql = sql + " and status={}".format(status);

            logging.info(sql);
            result = [];
            db = DbTool(host=host, root=root, pwd=pwd, db_name=db_name);
            db.select(sql, result);
            print(result)
            db.close()
            ret["status"] = "success";
            ret['data'] = result;
        except BaseException as e:
            ret["status"] = "error"
            logging.error(str(e))
            logging.error('任务执行错误', exc_info=True)
        return HttpResponse(json.dumps(ret))
        pass


class UserStatus(APIView):

    def post(self, request):
        ret = {}
        try:
            userId = request.POST.get("userId");
            status = request.POST.get("status");
            sql = "update user_info set status={} where id={}".format(status, userId);
            logging.info(sql);
            db = DbTool(host=host, root=root, pwd=pwd, db_name=db_name);
            num = db.update(sql);
            db.close()
            if num > 0:
                ret["status"] = "success";
            else:
                ret["status"] = "failed";
        except BaseException as e:
            ret["status"] = "error"
            logging.error(str(e))
            logging.error('任务执行错误', exc_info=True)
        return HttpResponse(json.dumps(ret))
