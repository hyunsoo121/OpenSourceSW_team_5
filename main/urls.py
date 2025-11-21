from django.urls import path

from . import views

# 앱의 URL 패턴을 정의
urlpatterns = [
    # 루트 경로 ('/')에 접속하면 views.index 함수가 실행됩니다.
    path("", views.main, name="home"),
    path("detail/", views.detailPage, name="detail"),
]
