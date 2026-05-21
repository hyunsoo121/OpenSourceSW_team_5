# 🖥️ ITformation

> IT 직무/활동 정보를 체계적으로 제공하는 플랫폼
> 기존 서비스들의 광범위한 카테고리 문제를 해소하고, IT에 특화된 맞춤형 정보를 제공합니다.

<br>

## 📌 목차

- [프로젝트 소개](#-프로젝트-소개)
- [주요 기능](#-주요-기능)
- [기술 스택](#-기술-스택)
- [시스템 아키텍처](#-시스템-아키텍처)
- [CI/CD 파이프라인](#-cicd-파이프라인)
- [Kubernetes 구성](#-kubernetes-구성)
- [코드 품질 관리](#-코드-품질-관리)
- [트러블슈팅](#-트러블슈팅)
- [팀원 및 역할](#-팀원-및-역할)

<br>

## 🧩 프로젝트 소개

기존 IT 정보 서비스(링커리어, 에브리타임, 슥삭)는 **사용자 의존적**이거나 **카테고리가 너무 광범위**하다는 문제가 있었습니다.

**ITformation**은 이러한 문제를 해소하기 위해 IT 직무에 특화된 체계적인 정보 제공과 개인 맞춤형 추천 기능을 제공합니다.

<br>

## ✨ 주요 기능

| 기능 | 설명 |
|------|------|
| **IT 정보 제공** | 모집분야, 요구레벨 등 체계적인 필드로 구성된 IT 활동 정보 제공 |
| **관리자 요청** | 이메일 전송을 통한 새로운 정보 등록 요청 기능 |
| **개인 맞춤 추천** | 사용자 프로필 기반의 맞춤형 IT 활동 추천 |

<br>

## 🛠️ 기술 스택

### Backend
![Python](https://img.shields.io/badge/Python-3.9-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=flat&logo=postgresql&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=flat&logo=gunicorn&logoColor=white)

### Infrastructure
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat&logo=kubernetes&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=flat&logo=nginx&logoColor=white)
![GCP](https://img.shields.io/badge/GCP-4285F4?style=flat&logo=googlecloud&logoColor=white)

### CI/CD & 코드 품질
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat&logo=githubactions&logoColor=white)
![Docker Hub](https://img.shields.io/badge/Docker_Hub-2496ED?style=flat&logo=docker&logoColor=white)
![pre-commit](https://img.shields.io/badge/pre--commit-FAB040?style=flat&logo=precommit&logoColor=black)

<br>

## 🏗️ 시스템 아키텍처

```
                        [인터넷]
                           │
                    HTTPS (443)
                           │
              ┌────────────▼────────────┐
              │   cert-manager (SSL)    │
              │  Let's Encrypt 자동 발급 │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │   Traefik Ingress       │
              │  itformation.p-e.kr     │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │   Nginx (리버스 프록시)  │
              │   정적 파일 서빙         │
              │   replica: 1            │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │   Django (Gunicorn)     │
              │   비즈니스 로직 처리     │
              │   replica: 2            │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │   PostgreSQL 15         │
              │   PVC 1Gi               │
              └─────────────────────────┘

         [GCP VM - K3s Kubernetes Cluster]
```

### 주요 설계 포인트

- **Django 2 Replicas**: 고가용성을 위한 파드 이중화
- **Nginx 리버스 프록시**: Django 앞단에서 정적 파일 서빙 및 요청 분산
- **PVC (Persistent Volume Claim)**: 정적 파일을 Nginx와 Django가 공유
- **Kubernetes Secret**: DB 비밀번호, Django SECRET_KEY, 이메일 비밀번호 등 민감 정보 분리 관리
- **ConfigMap**: 공개 설정값 별도 관리 (DB 이름, 허용 호스트 등)
- **HTTPS 강제 적용**: `SECURE_SSL_REDIRECT=True` + cert-manager Let's Encrypt 자동 인증

<br>

## 🔄 CI/CD 파이프라인

`main` 브랜치에 Push/PR 시 GitHub Actions가 자동 실행됩니다.

```
[Push to main]
      │
      ▼
┌─────────────────────────────────────────┐
│              1단계: CI                   │
│  ┌──────────┐  ┌──────────┐            │
│  │ Flake8   │  │  Black   │            │
│  │ (린팅)   │  │ (포매팅) │            │
│  └──────────┘  └──────────┘            │
│  ┌──────────┐  ┌──────────┐            │
│  │  isort   │  │ Safety   │            │
│  │(임포트)  │  │(보안검사)│            │
│  └──────────┘  └──────────┘            │
│  ┌──────────────────────────┐          │
│  │  Docker Compose 빌드 테스트│         │
│  └──────────────────────────┘          │
└──────────────┬──────────────────────────┘
               │ CI 통과 시
               ▼
┌─────────────────────────────────────────┐
│          2단계: CD 준비                  │
│  Docker 이미지 빌드 (linux/amd64)        │
│  Docker Hub Push                        │
│  heksis/oss-django:latest               │
└──────────────┬──────────────────────────┘
               │ 이미지 Push 완료 시
               ▼
┌─────────────────────────────────────────┐
│          3단계: CD 실행                  │
│  SSH → GCP VM 접속                      │
│  git reset --hard origin/main           │
│  kubectl delete/create secret           │
│  kubectl apply -f k8s/                  │
│  kubectl rollout restart django         │
│  kubectl get pods (상태 확인)           │
└─────────────────────────────────────────┘
```

<br>

## ☸️ Kubernetes 구성

```
k8s/
├── config.yaml        # ConfigMap (공개 설정, Nginx 설정)
├── django.yaml        # Django Deployment (replica: 2) + Service + PVC
├── nginx.yaml         # Nginx Deployment (replica: 1) + Service (NodePort: 30000)
├── postgres.yaml      # PostgreSQL Deployment + Service + PVC
├── ingress.yaml       # Traefik Ingress (HTTPS → nginx-service)
└── cert-issuer.yaml   # cert-manager ClusterIssuer (Let's Encrypt)
```

### 리소스 제한 설정

| 파드 | Memory Request | Memory Limit | CPU Request | CPU Limit |
|------|---------------|--------------|-------------|-----------|
| Django | 256Mi | 512Mi | 100m | 500m |
| Nginx | 64Mi | 128Mi | 50m | 250m |
| PostgreSQL | 128Mi | 512Mi | 100m | 500m |

<br>

## 🔍 코드 품질 관리

### pre-commit hooks

커밋 시 자동으로 아래 검사가 실행됩니다.

| 훅 | 역할 |
|----|------|
| **trailing-whitespace** | 불필요한 공백 제거 |
| **end-of-file-fixer** | 파일 끝 빈 줄 강제 |
| **check-large-files** | 대용량 파일 커밋 방지 |
| **check-yaml** | Kubernetes YAML 문법 오류 사전 검출 |
| **Black** | 코드 포매팅 자동화 |
| **isort** | 임포트 정렬 강제 적용 |
| **Conventional Commits** | 가독성 높은 커밋 메시지 규칙 적용 |

### Conventional Commits 규칙

```
feat:     새로운 기능 추가
fix:      버그 수정
docs:     문서 수정
style:    코드 포매팅
refactor: 리팩토링
test:     테스트 코드 추가
chore:    기타 변경사항
```

<br>

## 🔥 트러블슈팅

### 1. 배포 후 변경된 코드가 서버에 반영되지 않는 현상 (이미지 갱신 실패)

**증상**
GitHub Actions CI/CD 파이프라인이 성공(✅)으로 완료되고, K3s에서 파드를 강제 재시작(`rollout restart`)했음에도 브라우저에서 변경된 코드가 반영되지 않고 이전 화면이 지속적으로 출력됨.

**원인**
파이프라인 워크플로우(`django_ci.yml`)에 코드를 빌드하여 Docker Hub에 푸시하는 `Build & Push` 단계가 누락되어 있었음. 파이프라인은 테스트용 컨테이너만 실행 후 종료되었고, 서버는 Docker Hub에 있는 과거 이미지를 계속 Pull하여 배포하고 있었음.

**해결**
1. 워크플로우에 `build-and-push-action` 단계를 추가하여 테스트 통과 시 새 이미지를 빌드하고 Docker Hub에 Push하도록 수정
2. `k8s/django.yaml`에 `imagePullPolicy: Always` 속성을 추가하여 K8s가 배포 시 항상 최신 이미지를 강제로 Pull하도록 보완

```yaml
# k8s/django.yaml
containers:
- name: django
  image: heksis/oss-django:latest
  imagePullPolicy: Always  # ← 추가
```

---

### 2. Django 컨테이너 실행 직후 CrashLoopBackOff 현상 (설정 매핑 오류)

**증상**
CD 파이프라인 실행 후 Django 파드가 `ContainerCreating` → `Error` / `CrashLoopBackOff` 상태로 전환되며 정상 구동되지 않음.

**원인**
`settings.py`에서 환경 변수를 매핑하는 코드에 오류가 있었음. `DEFAULT_FROM_EMAIL` 설정 시 실제 발신자 이메일(`EMAIL_HOST_USER`)이 아닌 SMTP 서버 주소(`EMAIL_HOST`)를 잘못 참조하여 애플리케이션 초기화 시 오류 발생.

```python
# 잘못된 코드
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", EMAIL_HOST)  # ❌ SMTP 서버 주소

# 수정된 코드
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)  # ✅ 이메일 주소
```

**해결**
1. `kubectl logs` 명령어로 Crash된 파드의 로그를 확인하여 에러 발생 지점 추적
2. `settings.py` 내 변수 매핑 코드를 올바르게 수정
3. Kubernetes ConfigMap과 애플리케이션 설정값 일치 여부를 검증한 뒤 재배포하여 정상 구동 확인

```bash
# 파드 로그 확인 명령어
kubectl logs <pod-name>
kubectl describe pod <pod-name>
```

---

### 3. K8s 파드들이 무더기로 Evicted 되는 현상 (Disk Pressure)

**증상**
배포 중 갑자기 기존 파드들이 작동을 멈추고, `kubectl get pods` 확인 시 수십 개의 파드가 `Evicted` 상태로 남아있으며 새로운 파드도 생성되지 않음.

**원인**
CI/CD 파이프라인 구축 과정에서 잦은 빌드/배포 테스트를 반복한 결과, GCP VM 내부에 사용하지 않는 이전 버전의 Docker 이미지, 중지된 컨테이너, 빌드 캐시가 대량으로 쌓임. VM 디스크 사용량이 **92%** 를 초과(Disk Pressure)하여 K8s 스케줄러가 시스템 보호를 위해 파드를 강제 종료.

**해결**

```bash
# 1. 디스크 사용량 확인
df -h
# → /dev/sda1: 92% 사용 확인

# 2. 사용하지 않는 Docker 리소스 전체 삭제 (약 4~5GB 확보)
docker system prune -a --volumes -f

# 3. Evicted 상태 파드 일괄 정리
kubectl delete pod --field-selector=status.phase=Failed

# 4. K3s 서비스 재시작으로 클러스터 안정화
sudo systemctl restart k3s
```

**재발 방지**
K8s 리소스 제한(`resources.limits`) 설정으로 파드별 메모리/CPU 사용량을 제한하고, 정기적인 `docker system prune` 실행을 고려.

---

## 👥 팀원 및 역할

| 이름 | 역할 |
|------|------|
| **김현수** (팀장) | 백엔드 개발, CI/CD 파이프라인 구축, Kubernetes 인프라 구성 |
| 윤태옥 | 프론트엔드 개발, UI/UX 디자인 (Figma) |
| 이예건 | 프론트엔드 개발, UI/UX 디자인 (Figma) |
| 최우진 | 프론트엔드 개발 |

<br>

## 📂 프로젝트 구조

```
OpenSourceSW_team_5/
├── .github/
│   └── workflows/
│       └── django.yml       # GitHub Actions CI/CD
├── k8s/                     # Kubernetes 설정 파일
├── nginx/                   # Nginx 설정
├── admin_requests/          # 관리자 요청 앱
├── main/                    # 메인 앱
├── posts/                   # 게시물 앱
├── users/                   # 유저 앱
├── config/                  # Django 프로젝트 설정
├── templates/               # HTML 템플릿
├── static/                  # 정적 파일
├── Dockerfile
├── docker-compose.yml
├── .pre-commit-config.yaml
├── api_specification.md     # API 명세서
└── requirements.txt
```
