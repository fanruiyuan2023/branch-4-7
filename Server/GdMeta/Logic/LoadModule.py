from rest_framework.views import APIView
import json
from django.http import HttpResponse
import os
import _thread
import logging
logger = logging.getLogger(__name__)

class LoadModule(APIView):

    def __init__(self):
        pass

    def post(self, request, *args, **kwargs):
        # 获取模型ID号
        moduleId = request.POST.get("moduleId")

        pass