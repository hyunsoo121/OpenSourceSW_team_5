# API 명세서 (프로젝트 기준)

## 개요

이 문서는 현재 레포지토리의 엔드포인트(주로 서버 렌더링 뷰)를 정리한 API 명세서입니다. 또한, Django 템플릿에서 값을 어떻게 읽어와 렌더링하는지 예제(템플릿 스니펫)도 포함합니다.

> 주의: 이 프로젝트는 대부분 서버 사이드 렌더링을 사용합니다. 많은 뷰가 HTML 템플릿을 반환하므로 응답은 HTML이며, 템플릿에서 전달된 컨텍스트 변수를 사용해 값을 표시합니다.

---

## 엔드포인트 요약

| API 이름         |                        URL |  Method  | 설명                               | 요청 예시        | 응답(템플릿) 컨텍스트                  |
| ---------------- | -------------------------: | :------: | ---------------------------------- | ---------------- | -------------------------------------- |
| 게시판 목록      |                  `/posts/` |   GET    | 공개된 게시글 목록 페이지          | -                | `{'posts': QuerySet[Post]}`            |
| 게시글 상세      |    `/posts/<int:post_id>/` |   GET    | 단일 게시글 상세 페이지            | -                | `{'post': Post}`                       |
| 회원가입 페이지  |            `/user/signup/` |   GET    | 회원가입 폼 렌더링                 | -                | `{'form': SignupForm}`                 |
| 로그인 페이지    |             `/user/login/` |   GET    | 로그인 폼 렌더링                   | -                | `{'form': LoginForm}`                  |
| 회원정보 수정    |      `/user/edit-profile/` | GET/POST | 프로필 수정 폼 렌더링 및 제출 처리 | form-data (POST) | `{'form': EditProfileForm}`            |
| 관리자 요청 목록 |          `/admin-request/` |   GET    | 관리자 요청 리스트(로그인 필요)    | -                | `{'requests': QuerySet[AdminRequest]}` |
| 관리자 요청 상세 | `/admin-request/<int:pk>/` |   GET    | 특정 관리자 요청 상세(로그인 필요) | -                | `{'admin_request': AdminRequest}`      |
| 관리자 요청 작성 |   `/admin-request/create/` | GET/POST | 요청 작성 폼 렌더링/제출           | form-data (POST) | `{'form': AdminRequestForm}`           |

---

## 데이터 모델 요약 (주요 필드)

- Post

  - id: Integer
  - author: User (FK)
  - type: Char (choices: CLUB, EXTERNAL, BOOTCAMP)
  - name: Char
  - homepage_link: URL
  - application_months: Char (콤마로 구분된 문자열, ex: "1월,2월")
  - activity_months: Char (콤마로 구분)
  - description: Text
  - eligibility: Char (콤마로 구분된 코드, ex: "STUDENT,GRADUATE")
  - recruitment_fields: Char (콤마로 구분된 코드)
  - required_dev_levels: Char (콤마로 구분)

- PostReviewLink

  - post: FK -> Post
  - review_title: Char
  - review_url: URL

- AdminRequest
  - requester, target_post (FK -> posts.Post), request_type, title, content, status, reviewer, review_comment

---

## 응답/템플릿 사용 예제

아래는 뷰가 템플릿으로 전달하는 컨텍스트(예: `posts` 또는 `post`)를 템플릿에서 어떻게 렌더링하는지 보여줍니다.

### 게시판 목록 템플릿 (`templates/posts/posts_list.html`)

목록에서 게시글 이름, 활동 타입을 출력하고 상세페이지 링크를 걸 때:

```django
{% extends 'base.html' %}
{% block content %}
	<ul>
	{% for post in posts %}
		<li>
			<a href="{% url 'posts:posts_detail' post.id %}">
				{{ post.name }} — {{ post.get_type_display }}
			</a>
		</li>
	{% empty %}
		<li>등록된 게시글이 없습니다.</li>
	{% endfor %}
	</ul>
{% endblock %}
```

### 게시글 상세 템플릿 (`templates/posts/posts_detail.html`)

상세 템플릿에서 모집 분야, 지원 기간 등 콤마로 저장된 다중 선택 필드들은 모델에 구현된 헬퍼 메서드(`get_*_display`)를 호출하면 사람이 읽기 좋은 문자열을 얻을 수 있습니다.

```django
<h2>{{ post.name }} ({{ post.get_type_display }})</h2>

<h3>모집 분야</h3>
<p>{{ post.get_recruitment_fields_display }}</p>

<h3>지원 기간</h3>
<p>{{ post.get_application_months_display }}</p>

<h3>신청 자격</h3>
<p>{{ post.get_eligibility_display }}</p>

<h3>요구 개발 레벨</h3>
<p>{{ post.get_required_dev_levels_display }}</p>

<h3>활동 후기</h3>
{% for r in post.reviews.all %}
	<p><a href="{{ r.review_url }}" target="_blank">{{ r.review_title }}</a></p>
{% empty %}
	<p>후기 없음</p>
{% endfor %}
```

### 폼에 체크박스(다중 선택) 필드 렌더링

`PostAdminForm`에서 `MultipleChoiceField` + `CheckboxSelectMultiple` 위젯을 사용합니다. 일반 템플릿에서 폼을 렌더링할 때는 아래처럼 사용합니다.

```django
<form method="post">{% csrf_token %}
	{{ form.non_field_errors }}
	<div>
		<label>지원 기간</label>
		{{ form.application_months }}  {# 이 필드는 Checkbox widgets를 렌더링 #}
	</div>
	<div>
		<label>모집 분야</label>
		{{ form.recruitment_fields }}
	</div>
	<button type="submit">저장</button>
</form>
```

- 관리자(Admin)에서는 `ModelAdmin.form = PostAdminForm` 설정으로 자동으로 위젯과 초기값이 반영됩니다.

### 템플릿에서 콤마 구분 값(리스트)로 다루기

모델에 `get_*_display()`가 이미 있으면 그걸 사용하세요. 만약 템플릿 레벨에서 리스트로 순회하고 싶다면 커스텀 템플릿 필터를 만들 수 있습니다.

예: `templatetags/split_filters.py` 생성

```python
# posts/templatetags/split_filters.py
from django import template

register = template.Library()

@register.filter
def split(value, sep=','):
		if not value:
				return []
		return [v.strip() for v in value.split(sep) if v.strip()]
```

템플릿에서 사용:

```django
{% load split_filters %}
{% for code in post.recruitment_fields|split:',' %}
	<span>{{ code }}</span>
{% endfor %}
```

하지만 가능한 경우 모델 레벨에서 가공해 주는 것이 더 안전합니다(이미 구현된 `get_recruitment_fields_display()`처럼).

---

## API 응답 예시 (템플릿 대체 JSON 응답을 만든 경우 참고)

만약 뷰에서 JSON 응답(REST 스타일)을 제공한다면 응답 예시는 다음과 같습니다.

### GET /posts/ (JSON)

```json
[
  {
    "id": 1,
    "name": "Alpha Club",
    "type": "CLUB",
    "recruitment_fields": "BACKEND,FRONTEND",
    "application_months": "3월,4월",
    "eligibility": "STUDENT",
    "required_dev_levels": "NOVICE"
  }
]
```

### GET /posts/<id>/ (JSON)

```json
{
  "id": 1,
  "name": "Alpha Club",
  "type": "CLUB",
  "description": "동아리 소개...",
  "recruitment_fields": "BACKEND,FRONTEND",
  "reviews": [{ "title": "후기1", "url": "https://..." }]
}
```

---

## 보안 / 인증

- 관리자/요청 관련 엔드포인트는 로그인 및 권한 검사를 필요로 합니다(뷰에서 `request.user.is_authenticated` 또는 데코레이터로 처리).
- 폼 제출시 CSRF 토큰(`{% csrf_token %}`)을 반드시 포함하세요.

---

## 부록: 템플릿에서 자주 쓰이는 코드 패턴

- URL reverse (템플릿)
  ```django
  <a href="{% url 'posts:posts_detail' post.id %}">상세</a>
  ```
- 안전한 HTML 출력
  ```django
  {{ post.description|linebreaksbr }}
  ```
- 폼 전체 출력 (간단)
  ```django
  <form method="post">{% csrf_token %}{{ form.as_p }}<button>저장</button></form>
  ```

---

필요하시면 이 문서를 기반으로 OpenAPI/Swagger 형식(JSON/YAML)으로 변환해 드리거나, REST JSON 엔드포인트(뷰)를 추가하는 가이드와 코드를 제공해 드리겠습니다.
