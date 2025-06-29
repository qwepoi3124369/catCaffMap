
from world.models import catCoffee, kaohsiung, Announcement
from django.contrib.gis.db.models.functions import AsGeoJSON
from django.http import JsonResponse,HttpResponseRedirect
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance, Transform
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from world.form.CatcafeForm import CatcafeForm

def map(request):

    AnnouncementData = Announcement.objects.all().order_by('-id')[:10]



    # 取得所有貓咖啡店的資料
    catCoffeeData = catCoffee.objects.annotate(json_location=AsGeoJSON("location"))

    # 轉換為 GeoJSON 格式，包含所有屬性
    catCoffeeGeojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": cafe.json_location,  # 這裡已經是 GeoJSON 格式
                "properties": {
                    "id":cafe.id,
                    "name": cafe.name,  # 假設有 name 欄位
                    "address":  cafe.address,  # 加入額外屬性
                    "type": cafe.type,
                "rate":cafe.rate
                }
            }
            for cafe in catCoffeeData
        ]
    }

    # kaohsiungData= kaohsiung.objects.annotate(geom_3826 = Transform('geom', 3826)).annotate(json_location=AsGeoJSON("geom_3826"))
    kaohsiungData = kaohsiung.objects.annotate(json_location=AsGeoJSON("geom"))

    kaohsiungGeojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": feature.json_location,  # 這裡已經是 GeoJSON 格式
                "properties": {
                    "id": feature.gid,
                    "name": feature.townname,  # 假設有 name 欄位
                }
            }
            for feature in kaohsiungData
        ]
    }

    return render(request, 'map/map.html', {'catCafe': catCoffeeGeojson,"kaohsiung":kaohsiungGeojson,"Announcements":AnnouncementData})

##MultiPolygon arcgisjs不支援geojson
def kaohsiungLayer(request):
    kaohsiungData= kaohsiung.objects.all()
    serializer =serialize("geojson", kaohsiungData, geometry_field="geom", fields=["gid", "townname"],srid=3826)
    return JsonResponse(serializer, safe=False)


def my_view(request):
    show_map_dialog = request.GET.get('show_map', 'false').lower() == 'true'
    context = {
        'show_map_dialog': show_map_dialog,  # 傳遞布林值到模板
        'dialog_title': '地圖對話框',
        'dialog_content': '這裡是地圖的內容'
    }
    return render(request, 'map/mapDialogTemplate/Announcement.html', context)



def catCafeDetail(request, id=None):
    # if request.user.is_superuser:
    if 1==1:
        if id:
            # 根據 ID 查找公告，若不存在則返回 404
            getMapFeature = get_object_or_404(catCoffee, id=id)


            return render(request, 'map/catcafe.html', {'point': getMapFeature })

    else:
        return HttpResponseRedirect('/login')


def map2(request):
    # 从数据库中获取所有的 House 对象
    houses = House.objects.all()
    location_json = houses.annotate(json=AsGeoJSON("location"))
    # location_json = houses.annotate(json=AsGeoJSON("location")).get(name="location").json
    test=[]
    for house in location_json:
        test.append(house.json)
        print(house.json)  # 每个 house 对象的 GeoJSON 数据


    # 将 houses 传递到模板
    return JsonResponse({"houses": test}, safe=False)

from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
# @login_required  # 使用 Django 自帶的登錄檢查裝飾器
def getfeature(request):
    # 此視圖僅允許已登錄用戶訪問
    if request.method == 'POST':
        try:
            x = float(request.POST.get('x'))
            y = float(request.POST.get('y'))
            tolerance = float(request.POST.get('torelance'))
            point = Point(x, y, srid=3826)

            # 查詢距離 point 在容差範圍內的最近的 WorldHouse
            houses = House.objects.filter(location__distance_lte=(point, tolerance)) \
                .annotate(distance=Distance('location', point)) \
                .order_by('distance')[:1]

            # 構建響應數據
            data = []
            for house in houses:
                data.append({
                    'location_geojson': house.location.geojson,
                    'properties': {
                        'name': house.name,
                    }
                })
            return JsonResponse({'status': '1ok', 'data': data})

        except (TypeError, ValueError) as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'})


# @login_required
def getfeature2(request):
    if request.method == 'POST':
        try:
            x = float(request.POST.get('x'))
            y = float(request.POST.get('y'))
            tolerance = float(request.POST.get('torelance'))
            point = Point(x, y, srid=3826)

            # 查詢在容差範圍內最接近的 WorldLine
            lines = world_line.objects.annotate(
                geom_4326=Transform('geom', 4326)  # 將 geom 轉換為 SRID 4326
            ).filter(
                geom_4326__distance_lte=(Transform(point, 4326), tolerance)
            ).annotate(
                distance=Distance('geom_4326', Transform(point, 4326))
            ).order_by('distance')[:1]

            print(lines)
            # 構建響應數據
            data = []

            for line in lines:

                data.append({
                    'location_geojson': line.geom.geojson,
                    'properties': {
                        'name': line.name,
                    }
                })
            return JsonResponse({'status': '2ok', 'data': data})

        except (TypeError, ValueError) as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'})


# @login_required
def getfeature3(request):
    if request.method == 'POST':
        try:
            x = float(request.POST.get('x'))
            y = float(request.POST.get('y'))
            tolerance = float(request.POST.get('torelance'))
            point = Point(x, y, srid=3826)

            # 查詢在容差範圍內最接近的 GeologMap
            polygons = world_polygon.objects.annotate(
                geom_4326=Transform('geom', 4326)  # 將 geom 轉換為 SRID 4326
            ).filter(
                geom_4326__distance_lte=(Transform(point, 4326), tolerance)
            ).annotate(
                distance=Distance('geom_4326', Transform(point, 4326))
            ).order_by('distance')[:1]
            data=[]
            # 構建響應數據
            for polygon in polygons:
                data.append({
                    'location_geojson': polygon.geom.geojson,
                    'properties': {
                        'name': polygon.name,
                    }
                })
            return JsonResponse({'status': 'ok', 'data': data})

        except (TypeError, ValueError) as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'})


def buffer(request):
    if request.method == 'POST':
        x = float(request.POST.get('x'))
        y = float(request.POST.get('y'))

        page = int(request.POST.get('page'))
        tolerance = float(request.POST.get('torelance'))
        point = Point(x, y, srid=3826)

        searchItems = catCoffee.objects.annotate(
            geom_4326=Transform('location', 4326)  # 將 geom 轉換為 SRID 4326
        ).filter(
            geom_4326__distance_lte=(Transform(point, 4326), tolerance)
        ).annotate(
            distance=Distance('geom_4326', Transform(point, 4326))
        ).order_by('distance')
        print(searchItems)
        paginator = Paginator(searchItems, 3)


        page_objs = paginator.get_page(page)
        pagesNum = paginator.num_pages  # 總頁數
        # return render(request, 'map.html', {
        #     'searchDatas': page_objs
        # })
        data = []
        allData=[]
        # 構建響應數據

        for searchItem in searchItems:
            allData.append({
                'location_geojson': searchItem.location.geojson,
                'properties': {
                    'id': searchItem.id,
                    'name': searchItem.name,
                    "address": searchItem.address,  # 加入額外屬性
                    "type": searchItem.type,
                    "rate": searchItem.rate
                }
            })

        for page_obj in page_objs:
            data.append({
                'location_geojson': page_obj.location.geojson,
                'properties': {
                    'id': page_obj.id,
                    'name': page_obj.name,
                    "address": page_obj.address,  # 加入額外屬性
                    "type": page_obj.type,
                    "rate": page_obj.rate
                }
            })
        return JsonResponse({'status': 'ok', 'data': data,'allData':allData,"pagesNum":pagesNum})

def attributeSearch(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        typeValue = request.POST.get("type", "").strip()
        page = int(request.POST.get('page'))
        minRate = request.POST.get("minRate")
        maxRate = request.POST.get("maxRate")

        district = request.POST.get("district")
        print(district)

        searchItems = catCoffee.objects.all().order_by('-id')
        if name != "":
            searchItems = searchItems.filter(name__icontains=name).order_by('-id')
        if typeValue != "all":
            searchItems = searchItems.filter(type=typeValue).order_by('-id')
        if district != "all":
            poly = kaohsiung.objects.get(townname=district).geom
            searchItems = searchItems.filter(location__contained=poly)
        if minRate != "":
            searchItems = searchItems.filter(rate__gte=minRate).order_by('-id')
        if maxRate != "":
            searchItems = searchItems.filter(rate__lte=maxRate).order_by('-id')

        print(searchItems)
        paginator = Paginator(searchItems, 3)
        page_objs = paginator.get_page(page)
        pagesNum = paginator.num_pages  # 總頁數
        data = []
        allData = []
        # 構建響應數據

        for searchItem in searchItems:
            allData.append({
                'location_geojson': searchItem.location.geojson,
                'properties': {
                    'id': searchItem.id,
                    'name': searchItem.name,
                    "address": searchItem.address,  # 加入額外屬性
                    "type": searchItem.type,
                    "rate": searchItem.rate
                }
            })

        for page_obj in page_objs:
            data.append({
                'location_geojson': page_obj.location.geojson,
                'properties': {
                    'id': page_obj.id,
                    'name': page_obj.name,
                    "address": page_obj.address,  # 加入額外屬性
                    "type": page_obj.type,
                    "rate": page_obj.rate
                }
            })
        return JsonResponse({'status': 'ok', 'data': data,'allData':allData,"pagesNum":pagesNum})

