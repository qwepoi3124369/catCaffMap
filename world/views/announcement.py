
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseForbidden
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from world.models import Announcement
from django.core.paginator import Paginator
from world.form.AnnouncementForm import AnnouncementForm


from django.shortcuts import render
from django.http import JsonResponse

from django.views.decorators.http import require_http_methods






def announcementManage(request, template_name, announcement_id=None):
    if request.user.is_superuser:
        if template_name == 'manage/system/announcement/announcement.html':
            announcement_list = Announcement.objects.all().order_by('-created_at')
            paginator = Paginator(announcement_list, 8)  # 每頁 10 筆公告

            page_number = request.GET.get('page') or 1  # 如果頁碼為空，設置為第 1 頁
            page_obj = paginator.get_page(page_number)
            return render(request, 'manage.html', {'template_name': template_name, 'announcements': page_obj})
            # 公告修改頁面
        elif template_name == 'manage/system/announcement/announcementModify.html' and announcement_id:
            # 根據 ID 查找公告，若不存在則返回 404
            announcement = get_object_or_404(Announcement, id=announcement_id)

            if request.method == 'POST':
                form = AnnouncementForm(request.POST, instance=announcement)
                if form.is_valid():
                    form.save()  # 保存修改
                    return redirect('announcement')  # 重定向至公告列表頁面
            else:
                # 如果是 GET 請求，顯示已填充數據的表單
                form = AnnouncementForm(instance=announcement)
###announcement需要改
            return render(request, 'manage.html', {'template_name': template_name,'form': form,'announcement': announcement })



            # announcements = Announcement.objects.all().order_by('-created_at')
            # return render(request, 'manage.html', {'template_name': template_name, 'announcements': announcements})
        else:
            return render(request, 'manage.html', {'template_name': template_name})
    else:
        return HttpResponseRedirect('/login')



def delete_announcement(request, announcement_id):
    # 確認使用者已登入並且是超級使用者
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseForbidden("此操作僅限超級使用者")

    # 獲取公告物件或返回 404 錯誤
    announcement = get_object_or_404(Announcement, id=announcement_id)

    # 刪除公告
    announcement.delete()

    # 返回刪除成功訊息或重定向
    return HttpResponse("刪除成功")  # 或使用 `redirect('announcements')` 來重定向到公告列表




def add_announcement(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("此操作僅限超級使用者")

    if request.method == 'POST':
        name = request.POST.get('name')
        content = request.POST.get('content')
        owner = request.POST.get('owner')

        if name and content and owner:  # 確認所有字段都有填寫
            Announcement.objects.create(
                name=name,
                content=content,
                owner=owner
            )
            return redirect('/manage/announcement')  # 假設 'manage' 是返回的頁面名稱

    return render(request,  'add_announcement.html')





