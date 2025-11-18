from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm


# 회원가입 페이지 렌더링 및 로직 처리
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            auth_login(request, user)

            return redirect("home")

    else:
        form = CustomUserCreationForm()

    return render(request, "user/signup.html", {"form": form})


# 로그인 페이지 렌더링
def login(request):
    # 로그인 로직은 Django의 built-in LoginView를 사용하는 것이 더 일반적입니다.
    return render(request, "user/login.html")


# 회원정보 수정 페이지 렌더링
def edit_profile(request):
    return render(request, "user/edit_profile.html")
