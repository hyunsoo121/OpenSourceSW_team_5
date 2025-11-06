from django.shortcuts import render

# Create your views here.


# 게시판 목록 페이지 렌더링
def posts_list(request):
    return render(request, "posts/posts_list.html")


# 게시판 상세 페이지 렌더링
def posts_detail(request, post_id):
    return render(request, "posts/posts_detail.html", {"post_id": post_id})
