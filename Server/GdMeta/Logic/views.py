from django.contrib.auth.models import User
from django.contrib import auth
from django.template import RequestContext
import json
from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse
from rest_framework.views import APIView
import logging
from .db_tool import *
from .globalobjs import *
from .dianzan import *
from .remark import *
from django.views.decorators.clickjacking import xframe_options_exempt



class Login(APIView):
    #@xframe_options_exempt
    def get(self, request, *args, **kwargs):
        try:
            logging.info('Login is called...');
            #return HttpResponse(content=open(base_dir + "/templates/login.html", encoding='utf-8').read())
            return HttpResponse(content=open(base_dir + "/templates/login_jupiter.html", encoding='utf-8').read())
        except BaseException as e:
            logging.error(str(e))
            logging.error('任务执行错误', exc_info=True)

class Logout(APIView):
    def get(self, requset, *args, **kwargs):
        try:
            logging.info("Logout is called...");
            requset.session.clear();
            #return HttpResponse(content=open(base_dir + "/templates/login.html", encoding='utf-8').read())
            return HttpResponse(content=open(base_dir + "/templates/login_jupiter.html", encoding='utf-8').read())
        except BaseException as e:
            logging.error((str(e)))
            logging.error('任务执行错误', exc_info=True)


class MainPage(APIView):
    def get(self, request, *args, **kwargs):
        try:
            self.getModuleInfo();
            ret_list = self.getModuleInfo();
            userName = request.session.get("userName", "guest");
            return render(request, "main.html", {"ret_list": ret_list, "userName":userName});
        except BaseException as e:
            logging.error(str(e))
            logging.error('任务执行错误', exc_info=True)

    # 获取所有模型信息
    def getModuleInfo(self):
        sql = "select t1.username, t2.title, t2.module_code, t2.desp, t2.tag, t2.upload_date " \
              "from user_info t1 INNER JOIN module_info t2 on t1.id = t2.author WHERE t2.status = 1";
        logging.info(sql);
        db = DbTool(host=host, root=root, pwd=pwd, db_name=db_name);
        results = []
        db.select(sql, results);
        ret_list = [];
        for item in results:
            print(item);
            author = item[0];
            title = item[1];
            moduleCode = item[2];
            moduleName = 'module.glb';
            image = moduleCode + '/image.jpg';
            desp = item[3];
            tag = item[4];
            datetime = item[5];
            zanNum = getZanNum(moduleCode);
            remarkNum = getRemarkNum(moduleCode);
            moduleInfo = {"moduleName": moduleName, 'image':image,
                          'title':title,'author':author,
                          'desp':desp, 'tag':tag,
                          'datetime':'{}-{}-{}'.format(datetime.year, datetime.month, datetime.day) ,
                          'moduleCode':moduleCode,
                          'zanNum':zanNum,
                          'remarkNum':remarkNum
                          };
            ret_list.append(moduleInfo);
        return ret_list;


class Upload(APIView):
    def get(self, request, *args, **kwargs):
        try:
            return  HttpResponse(content=open(base_dir + "/templates/upload.html", encoding='utf-8').read());
        except BaseException as e:
            logging.error(str(e))
            logging.error('任务执行错误', exc_info=True)

class ModulePage(APIView):

    def get(self, request, *args, **kwargs):
        try:
            moduleCode = request.GET.get("moduleCode");
            authorId = self.getAuthorId(moduleCode);
            info_dict = {'moduleCode':moduleCode, 'authorId': authorId};
            response = render(request, "loadModule.html", {'data': info_dict});
            return response;
        except BaseException as e:
            logging.error(str(e))
            logging.error('任务执行错误', exc_info=True)

    def getAuthorId(self, module_code):
        authorId = -1;
        try:
            sql = "select author from module_info where module_code = '{}'".format(module_code);
            logging.info(sql);
            db = DbTool(host=host, root=root, pwd=pwd, db_name=db_name);
            results = []
            db.select(sql, results);
            if len(results) > 0:
                authorId = results[0][0];
        except BaseException as e:
            logging.error(str(e))
            logging.error('任务执行错误', exc_info=True)
        return authorId;

class AdminPage(APIView):

    def get(self, request, *args, **kwargs):
        try:
            response = render(request, "admin.html");
            return response;
        except BaseException as e:
            logging.error(str(e))
            logging.error('任务执行错误', exc_info=True)