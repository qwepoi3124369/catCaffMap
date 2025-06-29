from django.contrib import admin
from django.contrib.gis.db import models as gis_models
from leaflet.admin import LeafletGeoAdmin
from world.models import catCoffee

@admin.register(catCoffee)
class catCoffeeAdmin(LeafletGeoAdmin):
    pass

from .models import Announcement  # 導入 Announcement 模型
# 註冊 Announcement 模型到 Django 管理後台
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'created_at', 'owner')  # 顯示的字段
    search_fields = ('name', 'owner')  # 可搜尋的字段
    list_filter = ('created_at', 'owner')  # 篩選器