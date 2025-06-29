
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





def manageIndexManage(request, template_name):
    if request.user.is_superuser:
        return render(request, 'manage.html', {'template_name': template_name})
    else:
        return HttpResponseRedirect('/login')






