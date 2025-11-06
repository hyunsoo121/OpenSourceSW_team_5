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
