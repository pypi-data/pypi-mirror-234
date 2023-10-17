from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from shipdan_model.utils.string import generate_number_key


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        User = get_user_model()
        now = timezone.now()
        email = self.normalize_email(email)
        try:
            user = User.objects.get(email=email)
            if user:
                return None
        except User.DoesNotExist:
            pass
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    is_ghost = models.BooleanField(default=False)  # True인 경우 다시 authenticate 불가능 + 회원가입 시 해당 인스턴스 삭제
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'accounts_user'


class UserResign(models.Model):
    user = models.ForeignKey(
        'app_model.User', on_delete=models.SET_NULL, null=True, related_name='resign_logs'
    )
    email = models.EmailField(
        max_length=254, null=True, blank=True, help_text='유저에겐 보여주지 마세요!'
    )

    resigned_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'accounts_userresign'


def profile_avatar_path(instance, filename):
    return 'accounts/avatar/{}/{}'.format(instance.user.email, filename)


class CommonProfile(models.Model):
    """
    .. Note::
        - 모든 유저가 갖는 공통 Profile
        - 주로 nickname 사용, 일부 locale에서 name 사용
    """
    MALE = 1
    FEMALE = 2
    GENDER = (
        (MALE, 'male'),
        (FEMALE, 'female'),
    )
    AGE_RANGE = (
        (1, '10대'),
        (2, '20대'),
        (3, '30대'),
        (4, '40대'),
        (5, '50대'),
        (6, '60대'),
        (7, '70대')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='common_profile')
    name = models.CharField(max_length=10, null=True)
    gender = models.IntegerField(choices=GENDER, help_text="1=남자, 2=여자", blank=True, null=True)
    age_range = models.IntegerField(choices=AGE_RANGE, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, null=True)

    nickname = models.CharField(max_length=8, blank=True, default='')
    avatar = models.ImageField(upload_to=profile_avatar_path, null=True, blank=True)
    use_common_avatar = models.BooleanField(default=False)
    one_line_intro = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        db_table = 'accounts_commonprofile'


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')

    zonecode = models.CharField(max_length=10, verbose_name='우편번호')
    sido = models.CharField(max_length=10, verbose_name='도/시 이름')
    sigungu = models.CharField(max_length=10, verbose_name='시/군/구 이름')
    bname = models.CharField(max_length=20, default='', verbose_name='법정동/법정리 이름', blank=True)
    bcode = models.CharField(max_length=20, default='', verbose_name='법정동 코드', blank=True)
    roadAddress = models.CharField(max_length=50, default='', verbose_name='도로명', blank=True)
    buildingName = models.CharField(max_length=50, default='', verbose_name='건물명', blank=True)
    jibunAddress = models.CharField(max_length=50, default='', verbose_name='지번 주소', blank=True)
    autoRoadAddress = models.CharField(max_length=50, default='', verbose_name='대체 도로명주소', blank=True)
    content = models.CharField(max_length=100, default='', verbose_name='장소 및 출입방법', blank=True)

    extra = models.CharField(max_length=100, default='', verbose_name='상세주소', blank=True)

    class Meta:
        db_table = 'accounts_address'


class KeyForResetPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='key_for_password')
    key = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = generate_number_key()
        return super().save(*args, **kwargs)

    def generate_new_key(self):
        self.key = generate_number_key(length=6)
        self.save()
        return self.key

    class Meta:
        db_table = 'accounts_keyforresetpassword'


class Tos(models.Model):
    PRIVACY = 1
    MARKETING_MESSAGE = 2  # 사용하지 않음.
    SERVICE = 3
    ABOVE_AGE_14 = 4
    EVENT_MESSAGE = 5  # 해당 값을 홍보성 메시지 수신동의도 함께 처리함.
    TERMS = (
        (PRIVACY, '개인정보처리방침'),
        (MARKETING_MESSAGE, '홍보성 메세지 수신 동의'),
        (SERVICE, '서비스 이용약관 동의'),
        (ABOVE_AGE_14, '만 14세 이상'),
        (EVENT_MESSAGE, '이벤트 정보 알림 수신 동의'),
    )
    TERMS_DICT = {
        'PRIVACY': PRIVACY,
        'MARKETING_MESSAGE': MARKETING_MESSAGE,
        'SERVICE': SERVICE,
        'ABOVE_AGE_14': ABOVE_AGE_14,
        'EVENT_MESSAGE': EVENT_MESSAGE,
    }

    # 이용약관
    term = models.IntegerField(choices=TERMS)
    version = models.IntegerField(default=1)
    publication_date = models.DateField(null=True, )
    is_required = models.BooleanField(default=False)
    is_used = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['term', 'version'], name='unique term and version for tos')
        ]
        db_table = 'accounts_tos'


class TosUserRelation(models.Model):
    user = models.ForeignKey('app_model.User', on_delete=models.CASCADE, related_name='tos_rels')
    tos = models.ForeignKey(Tos, on_delete=models.CASCADE, related_name='user_rels')
    approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'accounts_tosuserrelation'


class OnboardingProcessCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=50)
    ordering = models.IntegerField(help_text='카테고리의 순서', unique=True, null=True, default=None)
    is_shown_step = models.BooleanField(default=False)

    class Meta:
        db_table = 'accounts_onboardingprocesscategory'


class OnboardingProcess(models.Model):
    name = models.CharField(max_length=50, unique=True)
    prev_swiper = models.CharField(max_length=50, null=True, default=None, blank=True)
    next_swiper = models.CharField(max_length=50, null=True, default=None, blank=True)
    prev_page = models.CharField(max_length=50, null=True, default=None, blank=True)
    next_page = models.CharField(max_length=50, null=True, default=None, blank=True)
    is_used = models.BooleanField(default=True)
    is_question = models.BooleanField(default=True)
    category = models.ForeignKey(OnboardingProcessCategory, on_delete=models.CASCADE, null=True, blank=True,
                                 default=None)
    ordering = models.IntegerField(help_text='카테고리 내 순서', null=True, default=None)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['category', 'ordering'],
                                    name='unique category and ordering for onboarding process')
        ]
        db_table = 'accounts_onboardingprocess'


class OnboardingProcessUserRelation(models.Model):
    user = models.ForeignKey(User, related_name='onboarding_process_rels', on_delete=models.CASCADE)
    process = models.ForeignKey(OnboardingProcess, related_name='user_rels', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    answer = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'accounts_onboardingprocessuserrelation'


class OnboardingFinish(models.Model):
    user = models.ForeignKey(User, related_name='onboarding_finished', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'accounts_onboardingfinish'


class TemporaryUserLog(models.Model):
    changed_from = models.ForeignKey(User, related_name='from_user', null=True, on_delete=models.SET_NULL)
    changed_to = models.ForeignKey(User, related_name='temporary_logs', on_delete=models.CASCADE)

    class Meta:
        db_table = 'accounts_temporaryuserlog'


class OnboardingAB(models.Model):
    ONBOARDING_A = 1
    ONBOARDING_B = 2
    ONBOARDING_C = 3
    ONBOARDING_D = 4

    user = models.OneToOneField(User, related_name='onboarding_ab', on_delete=models.CASCADE)
    version = models.CharField(max_length=20)
    code = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'accounts_onboardingab'


class DailyActiveUserLog(models.Model):
    user = models.ForeignKey(User, related_name='dau_logs', on_delete=models.CASCADE)

    method = models.CharField(max_length=10, default='GET')
    path = models.CharField(max_length=255)
    param = models.JSONField(default=dict)
    body = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'accounts_dailyactiveuserlog'


class ABTest(models.Model):
    version = models.CharField(max_length=30, unique=True)
    seed = models.CharField(max_length=20)
    total_group = models.IntegerField(default=2)
    started_at = models.DateTimeField(null=True, default=None)
    ended_at = models.DateTimeField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'accounts_abtest'


class UserABProperty(models.Model):
    user = models.ForeignKey(User, related_name='ab_properties', on_delete=models.CASCADE)
    ab_test = models.ForeignKey(ABTest, related_name='ab_properties', on_delete=models.CASCADE)
    value = models.IntegerField()
    extra = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'ab_test'], name='unique user and ab_test for UserABProperty')
        ]
        db_table = 'accounts_userabproperty'
