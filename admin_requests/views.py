from django.shortcuts import render

# Create your views here.


# 요청 목록 페이지 렌더링
def request_list(request):
    return render(request, "admin_request/request_list.html")


# 요청 상세 페이지 렌더링
def request_detail(request, request_id):
    return render(
        request, "admin_request/request_detail.html", {"request_id": request_id}
    )


# 요청 작성 페이지 렌더링
def request_create(request):
    return render(request, "admin_request/request_create.html")


# 요청 수정 페이지 렌더링
def request_edit(request, request_id):
    return render(
        request,
        "admin_request/request_edit.html",
        {"request_id": request_id, "title": "기존 제목", "content": "기존 내용"},
    )
