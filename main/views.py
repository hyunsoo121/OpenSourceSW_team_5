from django.http import HttpRequest
from django.shortcuts import render


def main(request: HttpRequest):
    # 1. 로그인된 유저 객체 또는 AnonymousUser 객체를 가져옵니다.
    user = request.user

    # 2. 닉네임 변수를 초기화합니다.
    user_nickname = None

    # 3. 유저가 인증되었는지 (로그인되었는지) 확인합니다.
    # request.user.is_authenticated는 로그인 상태일 때만 True입니다.
    if user.is_authenticated:
        # User 모델에 정의된 'nickname' 필드 값을 가져옵니다.
        user_nickname = user.nickname

    # 템플릿에 닉네임 값을 딕셔너리 형태로 전달합니다.
    return render(request, "main/main.html", {"nickname": user_nickname})
