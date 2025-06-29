
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect

from world.views.manageIndex import manageIndexManage
from world.views.map import map,map2,getfeature,getfeature2,getfeature3,buffer,attributeSearch,kaohsiungLayer,catCafeDetail
from world.views.mapManage import mapManage,Catcafe,addCatCafe,modifyCatCafe,deleteCatCafe
from world.views.login import SignUpView,login,main_page,log_out,change_password
from world.views.announcement import delete_announcement,add_announcement,announcementManage
urlpatterns = [
path('', lambda request: HttpResponseRedirect('/map/')),  # 根路径重定向到 /map/
# 原本的後台
    path("admin/", admin.site.urls),
# 登入註冊
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('login/', login, name='login'),
    path('log_out/', log_out, name='log_out'),
    path('main_page/', main_page, name='main_page'),
    # path('change-password/', change_password, name='change_password'),
# 地圖
    path('map/', map, name='map'),
    path('map2/', map2, name='map2'),
    path('kaohsiungLayer/', kaohsiungLayer, name='kaohsiungLayer'),
    path('getfeature1/', getfeature, name='getfeature'),
    path('getfeature2/', getfeature2, name='getfeature2'),
    path('getfeature3/', getfeature3, name='getfeature3'),
    path('buffer/', buffer, name='buffer'),
    path('attributeSearch/', attributeSearch, name='attributeSearch'),
    path('map/catCafeDetail/<int:id>', catCafeDetail, name='catCafeDetail'),

# 地圖管理
#     path('manage/catcoffee', mapManage, {'template_name': 'manage/mapManage/catcoffee.html'},name='catCoffee'),
    path('manage/addCatcoffee', addCatCafe, name='addcatCoffee'),

path('manage/catcoffee', Catcafe,name='catCoffee'),
path('deleteCatcoffee/<int:id>/', deleteCatCafe, name='deleteCatcoffee'),
    path('manage/modifyCatcoffee/<int:id>', modifyCatCafe,   name='modifyCatcoffee'),

    # 首頁
    path('manage/', manageIndexManage, {'template_name': 'manage/manageIndex.html'}, name='manage'),

# 公告
    path('manage/announcementsAdd', announcementManage, {'template_name': 'manage/system/announcement/announcementsAdd.html'}, name='announcementsAdd'),
    path('manage/announcement', announcementManage, {'template_name': 'manage/system/announcement/announcement.html'}, name='announcement'),
    path('delete_announcement/<int:announcement_id>/', delete_announcement, name='delete_announcement'),
    path('add_announcement/', add_announcement, name='add_announcement'),
    # path('manage/announcementModify/<int:announcement_id>/', announcementManage,{'template_name': 'manage/system/announcement/announcementModify.html'}, name='announcement_modify'),
   ##切兩半
   path('manage/announcementsModify/<int:announcement_id>', announcementManage,
         {'template_name': 'manage/system/announcement/announcementModify.html'}, name='announcement_modify'),




    path('profile/', manageIndexManage, {'template_name': 'profile.html'}, name='profile'),
    path('settings/', manageIndexManage, {'template_name': 'settings.html'}, name='settings'),


# path('accounts/',include('registration.backends.default.urls'))

]
