from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import CustomUserCreationForm


# 회원가입 페이지 렌더링 및 로직 처리
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            auth_login(request, user)

            return redirect("/")

    else:
        form = CustomUserCreationForm()

    return render(request, "user/signup.html", {"form": form})


# 로그인 페이지 렌더링 및 처리
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "로그인 성공했습니다.")
            next_url = request.GET.get("next") or request.POST.get("next") or "/"
            return redirect(next_url)
        else:
            messages.error(request, "아이디 또는 비밀번호가 올바르지 않습니다.")

    return render(request, "user/login.html")


# 회원정보 수정 페이지 렌더링
def edit_profile(request):
    return render(request, "user/edit_profile.html")


def logout_view(request):
    auth_logout(request)
    messages.info(request, "로그아웃되었습니다.")
    return redirect("/")
