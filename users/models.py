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


class User(AbstractBaseUser, PermissionsMixin):

    INTEREST_CHOICES = [
        ("PM", "프로젝트/제품 관리 (PM)"),
        ("DESIGN", "디자인"),
        ("FRONTEND", "프론트엔드"),
        ("BACKEND", "백엔드"),
    ]

    AFFILIATION_CHOICES = [
        ("STUDENT", "대학생"),
        ("GRADUATE", "졸업생"),
        ("WORKER", "직장인"),
    ]

    LEVEL_CHOICES = [
        ("NOVICE", "초심자"),
        ("INTERMEDIATE", "중급자"),
        ("ADVANCED", "고급자"),
    ]

    id = models.AutoField(primary_key=True)

    username = models.CharField(max_length=150, unique=True, verbose_name="아이디")

    nickname = models.CharField(max_length=50, unique=True, verbose_name="닉네임")

    email = models.EmailField(max_length=255, unique=True, verbose_name="이메일")

    # 관심분야
    interest_field = models.CharField(
        max_length=10,
        choices=INTEREST_CHOICES,
        default="FRONTEND",
        verbose_name="관심분야",
    )

    # 소속
    affiliation = models.CharField(
        max_length=10,
        choices=AFFILIATION_CHOICES,
        default="STUDENT",
        verbose_name="소속",
    )

    dev_level = models.CharField(
        max_length=15, choices=LEVEL_CHOICES, default="NOVICE", verbose_name="개발 레벨"
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now, verbose_name="가입일")

    objects = CustomUserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "nickname"]

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
