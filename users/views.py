from django.shortcuts import render


# 회원가입 페이지 렌더링
def signup(request):
    return render(request, "user/signup.html")


# 로그인 페이지 렌더링
def login(request):
    return render(request, "user/login.html")


# 회원정보 수정 페이지 렌더링
def edit_profile(request):
    return render(request, "user/edit_profile.html")
