from rest_framework.views import APIView
import json
from django.http import HttpResponse
import os
import datetime
import random
import zipfile
import shutil
import _thread
import logging
from .db_tool import *
from .globalobjs import *

logger = logging.getLogger(__name__)

class FileUpload(APIView):

    def __init__(self):
        pass

    def post(self, request, *args, **kwargs):
        try:
            file_path = save_file(request)
            logging.info("file_path:%s" % file_path)
            #_thread.start_new_thread(self.work, (file_path,))
            ret = {'status':'success'}
            return HttpResponse(json.dumps(ret))
        except BaseException as e:
            logging.error(str(e))
            logging.error('任务执行错误', exc_info=True)

    def work(self, file_path):
        try:
            logging.info("file_path:%s" % file_path)
        except BaseException as e:
            logging.error(str(e))
            logging.error('任务执行错误', exc_info=True)

def save_db(userId, title, moduleTag, moduleDesp, moduleCode):
    try:
        imageFile = "image.jpg";
        moduleFile = "module.glb"
        now = datetime.datetime.now();
        upload_date = now.strftime("%Y-%m-%d %H:%M:%S");
        status = 1;
        sql = "insert into module_info(author, title, image, module, desp, upload_date, status, module_code, tag) " \
              "values('{}','{}','{}','{}', '{}', '{}', {}, '{}', '{}')".format(
                userId, title, imageFile, moduleFile, moduleDesp, upload_date, status, moduleCode, moduleTag);
        logging.info(sql);
        db = DbTool(host=host, root=root, pwd=pwd, db_name=db_name);
        num = db.update(sql);
        if num > 0:
            return "success"
        else:
            return "error"

    except BaseException as e:
        logging.error(str(e))
        logging.error('任务执行错误', exc_info=True)

# 创建随机字符串
def createRandomStr(randomlength):
    digits = '0123456789';
    ascii_letters = 'abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    str_list = [random.choice(digits + ascii_letters) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str

# 创建文件夹
def createDir(dirPath):

    if os.path.exists(dirPath):
        return
    else:
        os.mkdir(dirPath);

# 解压zip文件
def unzip_file(zip_src, dst_dir):
    ret = zipfile.is_zipfile(zip_src)
    if ret:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
        return True;
    else:
        return  False;

# 解析文件
def save_file(request):
    try:
        if request.method == 'POST':
            file_obj = request.FILES.get('file');
            fileName = file_obj.name;
            if fileName == "":
                return "file not included";
            else:
                author = request.session.get("userId", -1);
                moduleName = request.POST.get("moduleName");
                moduleTag = request.POST.get("moduleTag");
                moduleDesp = request.POST.get("moduleDesp");
                if author == -1 or moduleName.strip() == "" or moduleTag.strip() == "" or moduleDesp.strip() == "":
                    return "invalid parameters";
                module_code = createRandomStr(32);
                zipFile = './temp/' + module_code+ "_" +file_obj.name;
                unzipDir = './temp/' + module_code+ "_" +file_obj.name.split('.')[0];
                file_path = os.path.join(zipFile);
                logging.info("file_path:%s" % file_path)
                f = open(file_path, 'wb')
                print(file_obj, type(file_obj))
                for chunk in file_obj.chunks():
                    f.write(chunk)
                f.close();
                targetDir = './static/upload/' + module_code;
                createDir('./static/upload/' + module_code);
                unzip_file(zipFile, unzipDir);
                shutil.copyfile(unzipDir+'/module.glb',targetDir+'/module.glb');
                shutil.copyfile(unzipDir+'/image.jpg',targetDir+'/image.jpg');
                shutil.rmtree(unzipDir);
                os.remove(zipFile);
                save_db(author, moduleName, moduleTag, moduleDesp, module_code);
                return "success";
    except BaseException as e:
        logging.error(str(e))
        logging.error('任务执行错误', exc_info=True)
        return "exception";