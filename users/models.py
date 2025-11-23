from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


# 1. 사용자 관리자 (Manager) 정의
class CustomUserManager(BaseUserManager):
    """
    AbstractBaseUser를 위한 사용자 생성 관리자입니다.
    """

    def create_user(self, username, email, nickname, password=None, **extra_fields):
        if not username:
            raise ValueError("사용자명 (ID)은 필수입니다.")
        if not email:
            raise ValueError("이메일은 필수입니다.")
        if not nickname:
            raise ValueError("닉네임은 필수입니다.")

        email = self.normalize_email(email)
        user = self.model(
            username=username, email=email, nickname=nickname, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username, email, nickname, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, nickname, password, **extra_fields)


# 2. 커스텀 사용자 모델 정의
class User(AbstractBaseUser, PermissionsMixin):

    # 선택 필드 Choices 정의
    INTEREST_CHOICES = [
        ("PM", "기획"),
        ("DESIGN", "디자인"),
        ("FRONTEND", "프론트엔드"),
        ("BACKEND", "백엔드"),
        ("AI_ML", "AI/머신러닝"),
        ("EMBEDDED", "임베디드 SW"),
        ("QA", "QA/테스팅"),
        ("NETWORK", "네트워크/보안"),
        ("ETC", "기타"),
    ]
    AFFILIATION_CHOICES = [
        ("STUDENT_CS", "대학생(전공)"),
        ("STUDENT_NON_CS", "대학생(비전공)"),
        ("GRADUATE", "졸업생"),
        ("WORKER", "직장인"),
        ("NON_MAJOR", "비전공자"),
    ]
    LEVEL_CHOICES = [
        ("NOVICE", "초심자"),
        ("INTERMEDIATE", "중급자"),
        ("ADVANCED", "고급자"),
    ]

    # 모델 필드 정의
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True, verbose_name="아이디")
    nickname = models.CharField(max_length=50, unique=True, verbose_name="닉네임")
    email = models.EmailField(max_length=255, unique=True, verbose_name="이메일")
    phone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="전화번호"
    )
    address = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="주소"
    )

    interest_field = models.CharField(
        max_length=15,
        choices=INTEREST_CHOICES,
        default="FRONTEND",
        verbose_name="관심분야",
    )
    affiliation = models.CharField(
        max_length=20,
        choices=AFFILIATION_CHOICES,
        default="STUDENT_CS",
        verbose_name="소속",
    )
    dev_level = models.CharField(
        max_length=15, choices=LEVEL_CHOICES, default="NOVICE", verbose_name="개발 레벨"
    )

    # Django 인증 시스템 필수 필드
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="가입일")

    objects = CustomUserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "nickname"]

    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to.",
        related_name="custom_user_set",  # 고유한 related_name 지정
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="custom_user_permissions_set",  # 고유한 related_name 지정
        related_query_name="user",
    )

    class Meta:
        db_table = "users"
        verbose_name = "사용자"
        verbose_name_plural = "사용자 목록"

    def __str__(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
