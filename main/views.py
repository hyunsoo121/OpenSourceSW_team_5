from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render
from django.utils import timezone

from posts.models import Post


def main(request: HttpRequest):
    user = request.user
    user_nickname = None
    recommended_posts = Post.objects.none()

    print("\n\n--- main 뷰 함수 실행 시작 ---")

    if user.is_authenticated:
        user_nickname = user.nickname
        print(f"사용자 인증됨. 닉네임: {user_nickname}")

        try:
            interest_code = user.interest_field
            affiliation_code = user.affiliation
            dev_level_code = user.dev_level
        except AttributeError as e:
            print(f"User 모델 필드 접근 오류: {e}")
            interest_code = None
            affiliation_code = None
            dev_level_code = None

        print(
            f"[유저 필터링 기준] 관심사: '{interest_code}', 소속: '{affiliation_code}', 레벨: '{dev_level_code}'"
        )

        current_month = f"{timezone.now().month}월"
        print(f"현재 검색 월: {current_month}")

        q_published = Q(is_published=True)
        q_month = Q(application_months__icontains=current_month)

        q_interest = Q()
        if interest_code:
            q_interest |= Q(recruitment_fields__icontains=interest_code)

        q_eligibility = Q()
        if affiliation_code:
            q_eligibility |= Q(eligibility__icontains=affiliation_code)
        if dev_level_code:
            q_eligibility |= Q(eligibility__icontains=dev_level_code)

        q_activity_type = Q()
        activity_type = request.GET.get("activity_type")
        if activity_type:
            q_activity_type = Q(activity_type=activity_type)

        final_query = (
            q_published & q_month & (q_interest | q_eligibility) & q_activity_type
        )
        print(f"[최종 쿼리]: {final_query}")

        recommended_posts = Post.objects.filter(final_query).distinct()
        print(f"총 추천 게시글 수: {recommended_posts.count()}")

    else:
        print("사용자 인증되지 않음.")

    print("--- main 뷰 함수 실행 종료 ---")
    return render(
        request,
        "main/main.html",
        {
            "nickname": user_nickname,
            "recommended_posts": recommended_posts,
        },
    )


def recommend_page(request):
    """
    사용자 추천 페이지
    - 관심 분야만 일치하면 추천
    - 동아리, 대외활동, 부트캠프 모두 포함
    """
    user = request.user
    recommended_posts = Post.objects.none()

    print("\n\n========== recommend_page 시작 ==========")

    if user.is_authenticated:
        print(f"✅ 로그인한 사용자: {user.nickname}")

        # 사용자 관심 분야 가져오기
        try:
            interest_code = user.interest_field
            print(f"📌 사용자 관심 분야: {interest_code}")
        except AttributeError as e:
            print(f"❌ 관심 분야 가져오기 실패: {e}")
            interest_code = None

        if interest_code:
            # 관심 분야만으로 필터링 (활동 타입 무관)
            recommended_posts = Post.objects.filter(
                is_published=True,  # 공개된 게시글만
                recruitment_fields__icontains=interest_code,  # 관심 분야 일치
            ).order_by(
                "-created_at"
            )  # 최신순 정렬

            print(f"🔍 필터링 조건: 공개 + 관심분야({interest_code})")
            print(f"📊 총 추천 게시글: {recommended_posts.count()}개")

            # 활동 타입별 개수 확인 (디버깅)
            for post in recommended_posts[:5]:  # 처음 5개만 출력
                print(f"  - [{post.get_type_display()}] {post.name}")

        else:
            print("⚠️ 관심 분야가 설정되지 않음")
    else:
        print("❌ 로그인하지 않은 사용자")

    print("========== recommend_page 종료 ==========\n")

    return render(
        request,
        "recommend/recommend_page.html",
        {
            "recommended_posts": recommended_posts,
            "user_interests": interest_code if user.is_authenticated else None,
        },
    )
