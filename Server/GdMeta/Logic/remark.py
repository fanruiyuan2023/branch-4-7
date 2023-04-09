
import json
from django.http import HttpResponse
from rest_framework.views import APIView
import hashlib
import logging
from .db_tool import *
from .globalobjs import *

class SubmitRemark(APIView):

    def post(self, request):
        ret = {}
        try:
            userId = request.session.get("userId", None);
            if userId == None:
                ret["status"] = "noLogin";
            else:
                module_code = request.POST.get("module_code");
                author_id = request.POST.get("author_id");
                remark = request.POST.get("remark");
                guest_id = request.session.get("userId");
                status = 1;
                sql = "insert into remark_info(guest_id,author_id,module_code,remark,status)" \
                      " values({},{},'{}','{}',{})"\
                    .format(guest_id,author_id,module_code,remark,status);
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

class GetRemarkInfo(APIView):

    def post(self, request):
        ret = {"remarks":[]};
        try:
            module_code = request.POST.get("module_code");
            db = DbTool(host=host, root=root, pwd=pwd, db_name=db_name);
            sql = "SELECT t1.remark, t2.username FROM remark_info t1 LEFT JOIN user_info t2 on t1.guest_id = t2.id " \
                  "where t1.status = 1 and t1.module_code='{}'".format(module_code);
            logging.info(sql);
            result = []
            db.select(sql, result);
            print(result)
            db.close()
            if len(result) == 0:
                ret["status"] = "failed";
            else:
                for item in result:
                    temp = {"guest":item[1],"remark":item[0]}
                    ret["remarks"].append(temp);
            ret["status"] = "success";
            db.close()
        except BaseException as e:
            ret["status"] = "error"
            logging.error(str(e))
            logging.error('任务执行错误', exc_info=True)
        return HttpResponse(json.dumps(ret))

def getRemarkNum(module_code):
    remarkNum = 0;
    try:
        db = DbTool(host=host, root=root, pwd=pwd, db_name=db_name);
        sql = "select count(*) from remark_info where status=1 and module_code='{}'".format(module_code);
        logging.info(sql);
        result = []
        db.select(sql, result);
        print(result)
        db.close()
        if len(result) == 0:
            remarkNum = 0;
        elif result[0][0] >= 0:
            remarkNum = result[0][0];
        db.close()
    except BaseException as e:
        remarkNum = 0;
        logging.error(str(e))
        logging.error('任务执行错误', exc_info=True)
    return remarkNum;