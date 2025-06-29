
from world.models import House
from django.contrib.gis.db.models.functions import AsGeoJSON
from django.http import JsonResponse
import json
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseForbidden
from django.views.generic import TemplateView, CreateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.contrib import auth
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from world.models import Announcement
from django.core.paginator import Paginator





def manage(request, template_name):
    if request.user.is_superuser:
        if template_name == 'manage/system/announcement/announcement.html':
            announcement_list = Announcement.objects.all().order_by('-created_at')
            paginator = Paginator(announcement_list, 8)  # 每頁 10 筆公告

            page_number = request.GET.get('page') or 1  # 如果頁碼為空，設置為第 1 頁
            page_obj = paginator.get_page(page_number)
            return render(request, 'manage.html', {'template_name': template_name, 'announcements': page_obj})

            # announcements = Announcement.objects.all().order_by('-created_at')
            # return render(request, 'manage.html', {'template_name': template_name, 'announcements': announcements})
        else:
            return render(request, 'manage.html', {'template_name': template_name})
    else:
        return HttpResponseRedirect('/login')






