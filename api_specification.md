# API 명세서

## 개요

이 문서는 프로젝트의 API 명세를 정의합니다.

---

## 엔드포인트

### 1. 게시판 API

- **URL**: `/posts`
- **Method**: GET
- **설명**: 게시판 목록을 가져옵니다.
- **Response**:

  ```json
  [
    {
      "id": 1,
      "title": "게시글 제목",
      "content": "게시글 내용"
    }
  ]
  ```

- **URL**: `/posts/detail/<id>`
- **Method**: GET
- **설명**: 특정 게시글의 상세 정보를 가져옵니다.
- **Response**:
  ```json
  {
    "id": 1,
    "title": "게시글 제목",
    "content": "게시글 내용"
  }
  ```

---

### 2. 사용자 API

- **URL**: `/user/signup`
- **Method**: GET
- **설명**: 회원가입 페이지를 렌더링합니다.

- **URL**: `/user/login`
- **Method**: GET
- **설명**: 로그인 페이지를 렌더링합니다.

- **URL**: `/user/edit-profile`
- **Method**: GET
- **설명**: 회원정보 수정 페이지를 렌더링합니다.

---

### 3. 관리자 요청 API

- **URL**: `/admin-request`
- **Method**: GET
- **설명**: 관리자 요청 목록을 가져옵니다.

- **URL**: `/admin-request/detail/<id>`
- **Method**: GET
- **설명**: 특정 관리자 요청의 상세 정보를 가져옵니다.

---

## 기타

- 추가적인 설명이나 주석을 여기에 작성하세요.
