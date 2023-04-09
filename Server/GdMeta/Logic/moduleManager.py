from django.contrib import auth
import json
from django.http import HttpResponse
from rest_framework.views import APIView
import logging
from .globalobjs import *
from .db_tool import *



class ModuleManager(APIView):

    def post(self, request):
        ret = {}
        try:
            moduleName = request.POST.get("moduleName");
            status = request.POST.get("status");

            sql = "SELECT t1.id,t1.module,t2.username,t1.module_code,t1.tag,t1.status " \
                  "FROM module_info t1 LEFT JOIN user_info t2 ON t1.author = t2.id " \
                  "WHERE 1=1";

            if moduleName.strip() != "":
                sql = sql + " and t1.module like '%{}%'".format(moduleName);
            if status.strip() != "":
                sql = sql + " and t1.status={}".format(status);

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



class ModuleStatus(APIView):

    def post(self, request):
        ret = {}
        try:
            moduleId = request.POST.get("moduleId");
            status = request.POST.get("status");
            sql = "update module_info set status={} where id={}".format(status, moduleId);
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
