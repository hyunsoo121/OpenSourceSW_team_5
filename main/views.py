from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render
from django.utils import timezone

from posts.models import Post

# models.py에서 User 모델을 직접 import하지 않고 request.user를 사용합니다.


def main(request: HttpRequest):
    user = request.user
    user_nickname = None
    recommended_posts = Post.objects.none()

    print("\n\n--- main 뷰 함수 실행 시작 ---")

    # 1. 유저 인증 확인
    if user.is_authenticated:
        user_nickname = user.nickname
        print(f"사용자 인증됨. 닉네임: {user_nickname}")

        # --- 2. 현재 사용자 데이터 가져오기 (필터링 기준) ---

        # 🔑 수정: display 값 대신 DB에 저장된 '코드 값'을 사용합니다.
        try:
            interest_code = user.interest_field
            affiliation_code = user.affiliation
            dev_level_code = user.dev_level
        except AttributeError as e:
            # User 모델에 필드가 없는 경우 오류 처리 (일반 User 모델 사용 시 발생 가능)
            print(
                f"User 모델 필드 접근 오류: {e}. 로그인된 사용자 필드를 확인할 수 없습니다."
            )
            interest_code = None
            affiliation_code = None
            dev_level_code = None

        print(
            f"[유저 필터링 기준 코드] 관심사: '{interest_code}', 소속: '{affiliation_code}', 레벨: '{dev_level_code}'"
        )

        # --- 3. 현재 월 계산 ---
        # 🔑 수정: __icontains 룩업을 위해 따옴표 없이 일반 문자열로 설정
        current_month = f"{timezone.now().month}월"
        print(f"현재 검색 월 (일반 문자열): {current_month}")

        # --- 4. Post 필터링 로직 구현 ---

        # A. 기본 필터: 공개된 게시글만 필터링
        q_published = Q(is_published=True)

        # B. 지원 기간 필터: 현재 월이 application_months에 포함되는 포스트
        # JSON 배열 텍스트에 '11월'과 같은 문자열이 포함되는지 검색
        q_month = Q(application_months__icontains=current_month)
        print(f"B. 지원 기간 쿼리 (q_month): {q_month}")

        # C. 모집 분야 필터: 유저의 관심 분야 코드(예: BACKEND)가 recruitment_fields에 포함되는 포스트
        q_interest = Q()
        if interest_code:
            q_interest |= Q(recruitment_fields__icontains=interest_code)
            print(f"C. 관심 분야 쿼리 (q_interest): {q_interest}")

        # D. 신청 자격 필터 (eligibility): 소속 및 레벨 코드가 eligibility에 포함되는 포스트
        q_eligibility = Q()

        # 소속 필터
        if affiliation_code:
            q_eligibility |= Q(eligibility__icontains=affiliation_code)

        # 개발 레벨 필터
        if dev_level_code:
            q_eligibility |= Q(eligibility__icontains=dev_level_code)

        print(f"D. 신청 자격 쿼리 (q_eligibility): {q_eligibility}")

        # F. 활동 타입 필터링 추가
        q_activity_type = Q()
        activity_type = request.GET.get("activity_type")
        if activity_type:
            q_activity_type = Q(activity_type=activity_type)
            print(f"F. 활동 타입 필터링 (q_activity_type): {q_activity_type}")

        # 최종 쿼리 조건에 활동 타입 추가
        final_query = (
            q_published & q_month & (q_interest | q_eligibility) & q_activity_type
        )
        print(f"\n[ORM 쿼리] 최종 쿼리 조건: {final_query}")

        # 쿼리 실행
        recommended_posts = Post.objects.filter(final_query).distinct()
        print(f"쿼리 실행 완료. 총 추천 게시글 수: {recommended_posts.count()}")
        print(f"추천 게시글 목록 (ID): {[post.pk for post in recommended_posts]}")

        all_posts = Post.objects.all()
        print(f"\n======== [DB 저장된 전체 Post 데이터 목록] ========")
        if not all_posts.exists():
            print("❌ 데이터베이스에 저장된 게시글이 없습니다.")

        for post in all_posts:
            print("-" * 50)
            print(f"ID: {post.pk}")
            print(f"동아리 이름: {post.name}")
            print(f"공개 여부 (is_published): {post.is_published}")
            print(f"모집 분야 (recruitment_fields): {post.recruitment_fields}")
            print(f"지원 기간 (application_months): {post.application_months}")
            print(f"신청 자격 (eligibility): {post.eligibility}")
        print("=" * 50)

    else:
        print("사용자 인증되지 않음. 추천 게시글 없음.")

    print("--- main 뷰 함수 실행 종료 ---")
    return render(
        request,
        "main/main.html",
        {
            "nickname": user_nickname,
            "recommended_posts": recommended_posts,
        },
    )
