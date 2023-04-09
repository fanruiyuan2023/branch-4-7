
import json
from django.http import HttpResponse
from rest_framework.views import APIView
import hashlib
import logging
from .db_tool import *
from .globalobjs import *

class SubmitDianzan(APIView):

    def post(self, request):
        ret = {}
        try:
            userId = request.session.get("userId", None);
            if userId == None:
                ret["status"] = "noLogin";
            else:
                module_code = request.POST.get("module_code");
                guest_id = request.session.get("userId");
                status = 1;
                sql = "insert into dian_zan(module_code,user_id,status) values('{}',{},{})".format(module_code, guest_id, status);
                logging.info(sql);
                db = DbTool(host=host, root=root, pwd=pwd, db_name=db_name);
                num = db.update(sql);
                if num > 0:
                    ret["status"] = "success";
                else:
                    ret["status"] = "failed";
                db.close()
        except BaseException as e:
            ret["status"] = "error"
            logging.error(str(e))
            logging.error('任务执行错误', exc_info=True)
        return HttpResponse(json.dumps(ret))

class GetDianzanInfo(APIView):

    def post(self, request):
        ret = {};
        try:
            module_code = request.POST.get("module_code");
            db = DbTool(host=host, root=root, pwd=pwd, db_name=db_name);
            sql = "select count(*) from dian_zan where status=1 and module_code = '{}'".format(module_code);
            logging.info(sql);
            result = []
            db.select(sql, result);
            print(result)
            db.close()
            if len(result) == 0:
                ret["status"] = "failed";
            elif result[0][0] >= 0:
                ret["dianzan_num"] = result[0][0];
            db.close()
        except BaseException as e:
            ret["status"] = "error"
            logging.error(str(e))
            logging.error('任务执行错误', exc_info=True)
        return HttpResponse(json.dumps(ret))

def getZanNum(module_code):
    zanNum = 0;
    try:
        db = DbTool(host=host, root=root, pwd=pwd, db_name=db_name);
        sql = "select count(*) from dian_zan where status=1 and module_code='{}'".format(module_code);
        logging.info(sql);
        result = []
        db.select(sql, result);
        print(result)
        db.close()
        if len(result) == 0:
            zanNum = 0;
        elif result[0][0] >= 0:
            zanNum = result[0][0];
        db.close()
    except BaseException as e:
        zanNum = 0;
        logging.error(str(e))
        logging.error('任务执行错误', exc_info=True)
    return zanNum;