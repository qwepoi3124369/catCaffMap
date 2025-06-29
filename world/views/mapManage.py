
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseForbidden
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from world.models import catCoffee,kaohsiung
from world.form.CatcafeForm import CatcafeForm
from django.urls import reverse

from django.core.paginator import Paginator
from django.contrib.gis.geos import GEOSGeometry

def mapManage(request, template_name, id=None):
    if request.user.is_superuser:
        ##點
        if template_name == 'manage/mapManage/catcoffee.html':
            point_list = catCoffee.objects.all().order_by('-id')
            print(point_list)
            paginator = Paginator(point_list, 8)  # 每頁 10 筆公告

            page_number = request.GET.get('page') or 1  # 如果頁碼為空，設置為第 1 頁
            page_obj = paginator.get_page(page_number)

            return render(request, 'manage.html', {'template_name': template_name, 'points': page_obj})


            # announcements = Announcement.objects.all().order_by('-created_at')
            # return render(request, 'manage.html', {'template_name': template_name, 'announcements': announcements})
        elif template_name == 'manage/mapManage/addCatcoffee.html':
            if request.method == 'POST':
                form = CatcafeForm(request.POST)
                if form.is_valid():
                    house = form.save(commit=False)
                    location = request.POST.get('location')
                    if location:
                        house.location = GEOSGeometry(location)
                    house.save()
                    return redirect('catCoffee')
            else:
                form = CatcafeForm()
            return render(request, 'manage.html', {'template_name': template_name, 'form': HouseForm})
        elif template_name == 'manage/mapManage/catcoffeeModify.html' and id:
            # 根據 ID 查找公告，若不存在則返回 404
            getMapFeature = get_object_or_404(catCoffee, id=id)

            if request.method == 'POST':
                form = CatcafeForm(request.POST, instance=getMapFeature)
                if form.is_valid():
                    house = form.save(commit=False)
                    location = request.POST.get('location')
                    if location:
                        house.location = GEOSGeometry(location)
                    form.save()  # 保存修改
                    return redirect('testpoint')  # 重定向至公告列表頁面
            else:
                # 如果是 GET 請求，顯示已填充數據的表單
                form = CatcafeForm(instance=getMapFeature)

            return render(request, 'manage.html', {'template_name': template_name,'form': form,'point': getMapFeature })

        else:
            return render(request, 'manage.html', {'template_name': template_name})

    else:
        return HttpResponseRedirect('/login')

def Catcafe(request):
    if request.user.is_superuser:
        if request.method == "POST":
            name = request.POST.get("name", "").strip()
            typeValue = request.POST.get("type", "").strip()

            minRate = request.POST.get("minRate")
            maxRate = request.POST.get("maxRate")

            district= request.POST.get("district")
            print(district)
            print(maxRate)
            return redirect(
                f"{reverse('catCoffee')}?name={name}&type={typeValue}&minRate={minRate}&maRate={maxRate}&district={district}")
        else:
            name = request.GET.get("name", "").strip()
            typeValue = request.GET.get("type", "all").strip()
            minRate = request.GET.get("minRate", "").strip()
            maxRate = request.GET.get("maxRate", "").strip()
            district = request.GET.get("district", "all").strip()

            point_list = catCoffee.objects.all().order_by('-id')
            if name != "":
                point_list = point_list.filter(name__icontains=name).order_by('-id')
            if typeValue != "all":
                point_list = point_list.filter(type=typeValue).order_by('-id')
            if district != "all":
                poly = kaohsiung.objects.get(townname=district).geom
                point_list = point_list.filter(location__contained=poly)
            if minRate != "":
                point_list = point_list.filter(rate__gte=minRate).order_by('-id')
            if maxRate != "":
                point_list = point_list.filter(rate__lte=maxRate).order_by('-id')

            print(point_list)
            paginator = Paginator(point_list, 8)  # 每頁 10 筆公告
            page_number = request.GET.get('page') or 1  # 如果頁碼為空，設置為第 1 頁
            page_obj = paginator.get_page(page_number)
            return render(request, 'manage.html',
                          {'template_name': 'manage/mapManage/catcoffee.html', 'points': page_obj})
    else:
        return HttpResponseRedirect('/login')

def addCatCafe(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = CatcafeForm(request.POST)
            if form.is_valid():
                CatCafe = form.save(commit=False)
                location = request.POST.get('location')
                if location:
                    CatCafe.location = GEOSGeometry(location)
                CatCafe.save()
                return redirect('catCoffee')
        else:
            form = CatcafeForm()
        return render(request, 'manage.html',
                      {'template_name': 'manage/mapManage/addCatcoffee.html', 'form': CatcafeForm})
    else:
        return HttpResponseRedirect('/login')

def modifyCatCafe(request, id=None):
    if request.user.is_superuser:
        if id:
            # 根據 ID 查找公告，若不存在則返回 404
            getMapFeature = get_object_or_404(catCoffee, id=id)

            if request.method == 'POST':
                form = CatcafeForm(request.POST, instance=getMapFeature)
                if form.is_valid():
                    point = form.save(commit=False)
                    location = request.POST.get('location')
                    if location:
                        point.location = GEOSGeometry(location)
                    form.save()  # 保存修改
                    return redirect('catCoffee')  # 重定向至公告列表頁面
            else:
                # 如果是 GET 請求，顯示已填充數據的表單
                form = CatcafeForm(instance=getMapFeature)

            return render(request, 'manage.html', {'template_name': 'manage/mapManage/catcoffeeModify.html','form': form,'point': getMapFeature })

    else:
        return HttpResponseRedirect('/login')

def deleteCatCafe(request,id):
    # 確認使用者已登入並且是超級使用者
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseForbidden("此操作僅限超級使用者")
    # 獲取公告物件或返回 404 錯誤
    item = get_object_or_404(catCoffee,id=id)
    print(item)
    # 刪除公告
    item.delete()

    # 返回刪除成功訊息或重定向
    return HttpResponse("刪除成功")  # 或使用 `redirect('announcements')` 來重定向到公告列表

