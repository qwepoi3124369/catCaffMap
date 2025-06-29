
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseForbidden
from django.views.generic import TemplateView, CreateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User


def change_password(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/manage')
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # 預設情況下，改完密碼後，session 可能會失效，需要手動更新 session
            update_session_auth_hash(request, user)
            messages.success(request, '密碼已成功變更！')
            return redirect('map')
        else:
            messages.error(request, '請修正以下錯誤。')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})



# 创建一个新的表单类
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='使用者名稱',
        max_length=25,
        help_text='必要的。25 個字或更少，只包含字母、數字和 @/./+/-/_。'
    )
    email = forms.EmailField(required=True, help_text='必填。請輸入一個有效的電子郵件地址。')
    first_name = forms.CharField(required=False, help_text='選填。請輸入您的名字。', label='名字')
    last_name = forms.CharField(required=False, help_text='選填。請輸入您的姓氏。', label='姓氏')


    password1 = forms.CharField(
        required=True,
        label="密碼",
        strip=False,
        widget=forms.PasswordInput(attrs={
            # 'class': 'form-control',
            'placeholder': '輸入密碼',
            # 'autocomplete': 'new-password',
        }),
        help_text="<p>@你的密碼不能與其他個人資訊太相近。</p>\n<p>@你的密碼必須包含至少 8 個字元。</p>\n<p>@你不能使用常見的密碼。</p>\n@你的密碼不能全都是數字。"
    )




    password2 = forms.CharField(
        required=True,
        label="確認密碼",
        strip=False,
        widget=forms.PasswordInput(attrs={
            # 'class': 'form-control',
            'placeholder': '再次輸入密碼',
            # 'autocomplete': 'new-password',
        }),
        help_text="請再輸入一次密碼以確認。"
    )


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        # 保存提供的密碼為哈希密碼
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        else:
            print("error")
        return user
class SignUpView(CreateView):
    # form_class = UserCreationForm
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')  # 成功注册后重定向到登录页面
    template_name = 'sign_up.html'


def login(request):
    login_failed = None  # 初始化變量，默認為 None

    if request.user.is_authenticated:
        if request.user.has_perm('app_name.special_permission'):
            return HttpResponseRedirect('/manage')
        else:
            return HttpResponseRedirect('/houses')  # 默認重定向

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)
            if user.has_perm('app_name.special_permission'):
                return HttpResponseRedirect('/manage')
            else:
                return HttpResponseRedirect('/houses')  # 默認重定向
        else:
            login_failed = 'error'  # 僅在表單提交且失敗時設置此變量

    return render(request, 'login.html', {'login_failed': login_failed})

def main_page(request):
    return render(request, 'main_page.html')

def log_out(request):
    auth.logout(request)
    return HttpResponseRedirect('/login')