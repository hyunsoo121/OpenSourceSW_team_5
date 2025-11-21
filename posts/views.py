from django.db import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string

from .models import Post


# Ajax: 필터링된 게시글 목록(부분 HTML)을 반환
def posts_ajax_list(request):
    posts = Post.objects.filter(is_published=True).order_by("-created_at")
    # 페이지 타입 필터 (예: club, external, bootcamp) — AJAX에서 전달될 수 있음
    type_param = request.GET.get("type")
    if type_param and type_param != "ALL":
        posts = posts.filter(type=type_param.lower())
    # 다중 선택(콤마로 구분된 값)이 전달될 수 있음. 기본값은 ALL.
    field = request.GET.get("field")  # e.g. 'BACKEND,FRONTEND' or 'ALL'
    quarter = request.GET.get("quarter")
    eligibility = request.GET.get("eligibility")
    level = request.GET.get("level")

    # 모집 분야 (다중 선택 -> OR)
    if field and field not in ["ALL", ""]:
        values = [v for v in field.split(",") if v]
        if values:
            qf = models.Q()
            for v in values:
                qf |= models.Q(recruitment_fields__regex=rf"(^|,){v}(,|$)")
            posts = posts.filter(qf)

    # 분기 -> 월 매핑 (다중 분기 지원)
    if quarter and quarter not in ["ALL", ""]:
        quarter_values = [qv for qv in quarter.split(",") if qv]
        quarter_map = {
            "1분기": ["1월", "2월", "3월"],
            "2분기": ["4월", "5월", "6월"],
            "3분기": ["7월", "8월", "9월"],
            "4분기": ["10월", "11월", "12월"],
        }
        months = []
        for qv in quarter_values:
            months.extend(quarter_map.get(qv, []))
        months = list(dict.fromkeys(months))  # 중복 제거, 순서 보존
        if months:
            qm = models.Q()
            for m in months:
                qm |= models.Q(application_months__regex=rf"(^|,){m}(,|$)")
            posts = posts.filter(qm)

    # 신청 자격 (다중 선택 -> OR)
    if eligibility and eligibility not in ["ALL", ""]:
        values = [v for v in eligibility.split(",") if v]
        if values:
            qe = models.Q()
            for v in values:
                qe |= models.Q(eligibility__regex=rf"(^|,){v}(,|$)")
            posts = posts.filter(qe)

    # 개발 레벨 (다중 선택 -> OR)
    if level and level not in ["ALL", ""]:
        values = [v for v in level.split(",") if v]
        if values:
            ql = models.Q()
            for v in values:
                ql |= models.Q(required_dev_levels__regex=rf"(^|,){v}(,|$)")
            posts = posts.filter(ql)

    context = {"posts": posts}
    html = render_to_string(
        "posts/_posts_list_container.html", context, request=request
    )
    return HttpResponse(html)


# 게시판 목록 페이지 렌더링 (기본)
def posts_list(request):
    posts = Post.objects.filter(is_published=True).order_by("-created_at")
    return render(request, "posts/posts_list.html", {"posts": posts})


def posts_type_list(request, type_code):
    """타입별(동아리/대외활동/부트캠프) 게시글 목록 페이지

    type_code는 템플릿의 JS가 AJAX 요청에 포함시키기 위해 전달됩니다.
    """
    posts = Post.objects.filter(is_published=True, type=type_code.lower()).order_by(
        "-created_at"
    )
    return render(
        request, "posts/posts_list.html", {"posts": posts, "type_code": type_code}
    )


# 게시판 상세 페이지 렌더링
def posts_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(
        request,
        "posts/posts_detail.html",
        {"post": post, "type_display": post.get_type_display},
    )
