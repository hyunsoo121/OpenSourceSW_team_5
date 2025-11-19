from django.shortcuts import get_object_or_404, render

from .models import Post


# 게시판 목록 페이지 렌더링
def posts_list(request):
    """게시글 목록을 가져와 posts_list.html에 전달합니다.

    기본적으로 공개된 게시글(is_published=True)만 보여줍니다.
    """
    posts = Post.objects.filter(is_published=True).order_by("-created_at")
    # 활동 타입 필터링 추가
    activity_type = request.GET.get("activity_type")
    if activity_type:
        posts = posts.filter(activity_type=activity_type)
    return render(request, "posts/posts_list.html", {"posts": posts})


# 게시판 상세 페이지 렌더링
def posts_detail(request, post_id):
    """단일 게시글을 조회하여 posts_detail.html에 전달합니다."""
    post = get_object_or_404(Post, pk=post_id)
    return render(
        request,
        "posts/posts_detail.html",
        {"post": post, "type_display": post.get_type_display},
    )
