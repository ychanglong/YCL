# 引入常见的基础模块
from django.shortcuts import render, HttpResponse, redirect, reverse
# 插入Django.http中的模块
from django.http import JsonResponse, FileResponse
# 插入时间日期
import time, datetime
# 插入Q,Sum
from django.db.models import Q, Sum
# 插入随机函数
import random
# 插入setting
from django.conf import settings
# 引入os模块
import os