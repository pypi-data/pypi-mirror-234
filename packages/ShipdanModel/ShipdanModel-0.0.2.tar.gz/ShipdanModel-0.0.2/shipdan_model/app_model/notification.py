from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.conf import settings


User = get_user_model()

class AligoKakaoToken(models.Model):
    SHIPDAN = 1
    CHANNEL = (
        (SHIPDAN, '쉽단'),
    )

    key = models.CharField(max_length=250, verbose_name='토큰')
    is_expired = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    expired_at = models.DateTimeField()

    class Meta:
        db_table = 'notification_aligokakaotoken'


class KakaoTemplate(models.Model):
    TEMPLEATE_STATUS = (
        ('S', '중단'),
        ('A', '정상'),
        ('R', '대기'),
    )

    templtName = models.CharField(max_length=100, verbose_name='템플릿이름')
    templtContent = models.TextField(verbose_name='템플릿콘텐츠')
    status = models.CharField(max_length=3, verbose_name='승인상태', choices=TEMPLEATE_STATUS)
    templtCode = models.TextField(verbose_name='템플릿코드')
    cdate = models.TextField(verbose_name='템플릿 생성일')
    senderKey = models.TextField(null=True, default='')

    def __str__(self):
        return self.templtCode + '_' + self.templtName

    class Meta:
        db_table = 'notification_kakaotemplate'


class SMSNotificationMessage(models.Model):
    title = models.CharField(verbose_name='제목', max_length=50)
    content = models.TextField(verbose_name='내용')
    kakao_templt = models.ForeignKey(KakaoTemplate, related_name='SMS', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.pk) + '.' + self.title

    class Meta:
        db_table = 'notification_smsnotificationmessage'


class SMSNotification(models.Model):
    SEND_STATUS = (
        (0, '발송대기'),
        (1, '발송완료'),
        (2, '예약발송'),
        (-1, '발송실패'),
        (-2, '발송실패확인'),
    )
    receiver = models.CharField(max_length=20, verbose_name="수신자")
    msg = models.ForeignKey(SMSNotificationMessage, null=True, related_name='notifications', on_delete=models.SET_NULL)
    id_aligo = models.IntegerField(null=True)
    content = models.TextField()
    destination = models.CharField(verbose_name='고객명', blank=True, max_length=20)
    reserved_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=SEND_STATUS, default=0)

    class Meta:
        db_table = 'notification_smsnotification'


class KakaoTemplateButton(models.Model):
    LINKTYPE = (
        ('DS', '배송조희'),
        ('WL', '웹링크'),
        ('AL', '앱링크'),
        ('BK', '봇키워드'),
        ('MD', '메세지전달')
    )

    kakao_templete = models.ForeignKey(KakaoTemplate, related_name='buttons', on_delete=models.CASCADE)
    ordering = models.CharField(max_length=100, verbose_name='순서')
    name = models.CharField(max_length=100, verbose_name='버튼명')
    linkTypeName = models.CharField(max_length=20, verbose_name='버튼타입명')
    linkType = models.CharField(max_length=5, verbose_name='버튼타입', choices=LINKTYPE)
    linkMo = models.TextField(verbose_name='모바일웹링크', blank=True)
    linkPc = models.TextField(verbose_name='PC웹링크', blank=True)
    linkIos = models.TextField(verbose_name='IOS앱링크', blank=True)
    linkAnd = models.TextField(verbose_name='안드로이드앱링크', blank=True)

    class Meta:
        db_table = 'notification_kakaotemplatebutton'


class KakaoTemplateVariable(models.Model):
    kakao_template = models.ForeignKey(KakaoTemplate, related_name='variables', on_delete=models.CASCADE,
                                       verbose_name='연결된 템플릿')
    name = models.CharField(verbose_name='변수명', max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'notification_kakaotemplatevariable'


class KakaoAlimTalk(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='kakao_alimtalks', on_delete=models.CASCADE)
    kakao_template = models.ForeignKey(KakaoTemplate, related_name='kakao_alimtalks', on_delete=models.SET_NULL,
                                       null=True)
    tpl_code = models.TextField(verbose_name='템플릿코드')
    senddate = models.DateTimeField(null=True, blank=True, default=None)
    subject = models.CharField(verbose_name='알림톡제목', max_length=50)
    message = models.TextField(verbose_name='알림톡내용')
    created_at = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    mid = models.IntegerField(help_text='알림톡 전송 시 response 중 message id', null=True)

    class Meta:
        db_table = 'notification_kakaoalimtalk'


class MainNotice(models.Model):
    FOREVER = 0
    DAY = 1
    WEEK = 2
    MONTH = 3
    UNTIL_CODE = (
        (FOREVER, '영원히'),
        (DAY, '일'),
        (WEEK, '주'),
        (MONTH, '월'),
    )

    title = models.CharField(max_length=20, help_text='공지 제목')
    sub_title = models.CharField(max_length=20, help_text='서브 타이틀', blank=True)
    analytics_property = models.CharField(
        max_length=30, help_text='엠플리튜드 등 분석툴에서 사용할 user property나 event property에 들어갈 내용. 30자 이내로 영어로 작석바람')
    content = models.TextField(blank=True, default='')
    background_img = models.ImageField(blank=True, null=True, default=None, upload_to='mainnotice/background_img',
                                       help_text='이미지, 현재는 사용계획 없음')
    is_seen = models.BooleanField(default=False, help_text='started_at, ended_at과 더불어 is_seen도 체크 되어야 유저가 봄')
    web_seen = models.BooleanField(default=True, help_text='web에서 볼지 안볼지')
    ios_seen = models.BooleanField(default=True, help_text='ios에서 볼지 안볼지')
    android_seen = models.BooleanField(default=True, help_text='android에서 볼지 안볼지')
    started_at = models.DateTimeField(help_text='시작시간')
    ended_at = models.DateTimeField(help_text='끝시간')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    until_code = models.IntegerField(choices=UNTIL_CODE)
    until_amount = models.PositiveSmallIntegerField(default=1)
    style = models.JSONField(default=dict)
    link_to = models.TextField(null=True, blank=True, default=None, help_text="자세히 보기 주소")

    def __str__(self):
        return f'{self.title}_{self.sub_title}'

    class Meta:
        db_table = 'notification_mainnotice'


class MainNoticeButton(models.Model):
    CLOSE_BUTTON = 1
    UNTIL_BUTTON = 2
    LINK_BUTTON = 3

    BUTTON_CODES = (
        (CLOSE_BUTTON, '닫기'),
        (UNTIL_BUTTON, '그만보기'),
        (LINK_BUTTON, '자세히 보기 등'),
    )

    main_notice = models.ForeignKey(MainNotice, related_name='buttons', on_delete=models.CASCADE)
    code = models.IntegerField(choices=BUTTON_CODES)

    content = models.CharField(
        max_length=30, blank=True, default='', help_text='버튼안에 들어갈 글입니다. theme 상황에 따라 안적으셔도 됩니다.')
    theme = models.PositiveSmallIntegerField(default=1)
    style = models.JSONField(default=dict)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['main_notice', 'code'], name='unique main notice and button code')
        ]
        db_table = 'notification_mainnoticebutton'


class MainNoticeUserLog(models.Model):
    user = models.ForeignKey(User, related_name='main_notice_logs', on_delete=models.CASCADE)
    main_notice = models.ForeignKey(MainNotice, related_name='user_logs', on_delete=models.CASCADE)
    first_viewed = models.DateTimeField(auto_now_add=True)
    never_shown_until = models.DateTimeField(null=True, blank=True, default=None, help_text='다시보지 않기를 눌렀을 경우 시간 기입')

    class Meta:
        db_table = 'notification_mainnoticeuserlog'


class FCMDevice(models.Model):
    UNDEFINED = 0
    ANDROID = 1
    IOS = 2
    CHROME = 3

    DEVICES = [
        (UNDEFINED, 'UNDEFINED'),
        (ANDROID, 'ANDROID'),
        (IOS, 'IOS'),
        (CHROME, 'CHROME'),
    ]

    device_type = models.IntegerField(choices=DEVICES, default=UNDEFINED)
    user = models.ForeignKey(User, related_name='fcm_devices', blank=True, null=True,
                             on_delete=models.CASCADE)
    dev_id = models.CharField(verbose_name=("Device ID"), max_length=50, blank=True, null=True, default=None)
    reg_id = models.CharField(verbose_name=("Registration ID"), max_length=255, blank=True, null=True, default=None)
    name = models.CharField(verbose_name=("Name"), max_length=255, blank=True, null=True)
    is_active = models.BooleanField(verbose_name=("Is active?"), default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notification_fcmdevice'


class FCMNotificationCategory(models.Model):
    UNDEFINED = 0
    ALL_STACK = 1
    LAST_STACK = 2
    NO_STACK = 3
    STACK_LIST = (
        (UNDEFINED, 'UNDEFINED'),
        (ALL_STACK, 'ALL_STACK'),
        (LAST_STACK, 'LAST_STACK'),
        (NO_STACK, 'NO_STACK')
    )

    code = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=30, help_text='유저에게는 보이지 않는 해당 카테고리의 이름이니다')
    content = models.TextField(blank=True, help_text='유저에게는 보이지 않는 해당 카테고리의 설명입니다')
    topic = models.CharField(max_length=50, blank=True, default='', help_text='topic입니다')
    collapse_key = models.CharField(blank=True, default='', max_length=50)
    stack = models.IntegerField(choices=STACK_LIST, default=UNDEFINED)

    class Meta:
        db_table = 'notification_fcmnotificationcategory'


def fcm_notification_image_path(instance, filename):
    return 'spark/fcm_image/{}/{}'.format(instance.name, filename)


class FCMNotificationTarget(models.Model):
    name = models.CharField(max_length=20, help_text='amplitude 이벤트 프로퍼티 및 유저 프로퍼티로 들어갈 값입니다.')
    content = models.CharField(max_length=100, blank=True, help_text='해당 타겟 이벤트의 설명입니다. 안적으셔 괜찮습니다.')
    title = models.CharField(max_length=100, null=True, blank=True, help_text="제목입니다.")
    body = models.CharField(max_length=255, null=True, blank=True, help_text="내용입니다.")
    image = models.ImageField(upload_to=fcm_notification_image_path,
                              null=True, blank=True, help_text='앱푸시에 보이는 이미지입니다.')
    data = models.JSONField(
        default=dict, help_text='데이터 메세지 payload입니다. 필요시 개발자를 불러주세요!', null=True, blank=True
    )

    filter_event_tos = models.BooleanField(default=False, help_text='체크 시, 이벤트 수신 미동의 유저는 필터링됩니다.')

    reserved_at = models.DateTimeField()
    is_sent = models.BooleanField(default=False, help_text='실제로 보내지면 True로 바뀌며, 추후 업데이트는 불가능합니다.')
    emails = models.TextField(default='', help_text='쉼표 없이 한줄씩 적어주세요!')
    invalid_emails = models.TextField(
        default='',
        help_text='유저가 없거나(이메일 잘못기입 혹은 회원탈퇴), fcm 디바이스 등록이 되지 않거나, is active가 False인 유저입니다. 저장 시, '
                  '자동으로 기입됩니다. 필터는 적용된 값입니다.'
    )

    total_target = models.IntegerField(default=0, help_text='invalid_email 중 필터 빼고 적용한 유저수입니다.')
    valid_target = models.IntegerField(default=0, help_text='total_target에서 필터를 거치고 남은 유저입니다.')
    total_sent = models.IntegerField(
        default=0,
        help_text='fcm 발송 요청완료 수입니다. 단, 이는 실제로 받은 값은 아닙니다. 실제 유저가 받았는지 안받았는지는 알 수 있는 방법은 없습니다.'
    )
    total_viewed = models.IntegerField(default=0, help_text='유저가 해당 fcm을 본 경우입니다.')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'notification_fcmnotificationtarget'


class FCMNotification(models.Model):
    """
    .. Note::
        - notification 모델

    """

    identification_for_check = models.CharField(
        null=True, blank=True, default=None, max_length=100,
        help_text='app 패키지 쪽 문제로 {timestamp}_{random range timestamp}로 unique 처리'
    )

    target = models.ForeignKey(FCMNotificationTarget, related_name='notifications', null=True, default=None, blank=True,
                               on_delete=models.SET_NULL)
    name = models.CharField(max_length=100, blank=True, default='', help_text='amplitude에 사용될 수 있습니다.')
    title = models.CharField(max_length=100, null=True, blank=True, help_text="제목입니다.")
    body = models.CharField(max_length=255, null=True, blank=True, help_text="내용입니다.")
    message_id = models.CharField(max_length=100, blank=True)
    image = models.TextField(blank=True, null=True, help_text="프로필 이미지 등 push msg에 사용되는 큰 아이콘")
    icon = models.TextField(blank=True, null=True, help_text="작은 아이콘 이미지")
    link = models.TextField(blank=True, null=True, help_text="딥링크 주소")
    big_image = models.TextField(blank=True, null=True, help_text="큰 이미지 notification에 사용합니다.")

    data = models.TextField(blank=True, help_text='데이터 메세지 payload입니다')
    category = models.ForeignKey(FCMNotificationCategory, related_name='fcm_notifications', on_delete=models.SET_NULL,
                                 null=True, blank=True)

    to = models.ForeignKey(FCMDevice, related_name='fcm_notifications', null=True, blank=True,
                           help_text='단일로 보내는 대상입니다.', on_delete=models.SET_NULL)
    topic = models.CharField(max_length=50, blank=True, default='', help_text='topic입니다')

    is_checked = models.BooleanField(default=False)
    checked_at = models.DateTimeField(blank=True, null=True, default=None)
    reserved_at = models.DateTimeField(blank=True, null=True)
    is_sent = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'notification_fcmnotification'


class SendAllFCMLog(models.Model):
    total_message_count = models.IntegerField()
    success_message_count = models.IntegerField()
    fail_message_count = models.IntegerField()
    time_to_send_all = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'notification_sendallfcmlog'


class CouponAutomaticPage(models.Model):
    title = models.CharField(help_text='구분 용입니다.', max_length=100)
    button_text = models.CharField(default='쿠폰 다운로드', max_length=50)
    code = models.CharField(unique=True, help_text='쿠폰 코드입니다. 쿠폰 템플릿의 코드값과 똑같이 적어주셔야합니다.', max_length=20)
    content = models.TextField(blank=True, default='')

    is_seen = models.BooleanField(default=False, help_text='started_at, ended_at과 더불어 is_seen도 체크 되어야 유저가 봄')
    started_at = models.DateTimeField(help_text='이벤트 시작시간입니다. 쿠폰의 유효기간과는 다른 값입니다.')
    ended_at = models.DateTimeField(help_text='이벤트 끝시간입니다. 쿠폰의 유효기간과는 다른 값입니다.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notification_couponautomaticpage'


class AirbridgeDevice(models.Model):
    UNDEFINED = 'undefined'
    ANDROID = 'Android'
    IOS = 'iOS'

    DEVICES = [
        (UNDEFINED, 'UNDEFINED'),
        (ANDROID, 'ANDROID'),
        (IOS, 'IOS'),
    ]
    user = models.ForeignKey(User, related_name='airbridge_devices', blank=True, null=True,
                             on_delete=models.CASCADE)

    device_uuid = models.CharField(max_length=100)
    os_name = models.CharField(choices=DEVICES, max_length=10)
    os_version = models.CharField(max_length=20)
    device_model = models.CharField(max_length=50)
    gaid = models.CharField(null=True, default=None, max_length=100)
    ifa = models.CharField(null=True, default=None, max_length=100)
    ifv = models.CharField(null=True, default=None, max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notification_airbridgedevice'


""" 아래로 다 deprecated (23.09.04 기준 코드 작업 중)"""


class AmazonSNSPlatformApplication(models.Model):
    name = models.CharField(max_length=50)
    arn = models.CharField(max_length=200, null=True, default=None)

    class Meta:
        db_table = 'airbridge_amazonsnsplatformapplication'


class AmazonSNSPlatformEndpoint(models.Model):
    fcm_device = models.OneToOneField(FCMDevice, related_name='amazon_endpoint', on_delete=models.CASCADE)
    platform_application = models.ForeignKey(AmazonSNSPlatformApplication, related_name='endpoints',
                                             on_delete=models.SET_NULL, null=True)

    arn = models.CharField(max_length=200, null=True, default=None, unique=True)
    token = models.CharField(default='', max_length=200, help_text='fcm device reg_id')
    enabled = models.BooleanField(default=True)
    attributes = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notification_amazonsnsplatformendpoint'


class AmazonSNSTopic(models.Model):
    name = models.CharField(max_length=50, unique=True)
    arn = models.CharField(max_length=200, null=True, default=None, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = 'notification_amazonsnstopic'


class AmazonSNSSubscriptionCategory(models.Model):
    code = models.IntegerField()
    name = models.CharField(default=None, null=True, max_length=50, unique=True)
    title = models.CharField(max_length=300)
    body = models.CharField(max_length=300)
    description = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notification_amazonsnssubscriptioncategory'


class AmazonSNSSubscription(models.Model):
    topic = models.ForeignKey(
        AmazonSNSTopic, related_name='subscriptions', on_delete=models.SET_NULL, null=True
    )
    endpoint = models.ForeignKey(
        AmazonSNSPlatformEndpoint, related_name='subscriptions', on_delete=models.SET_NULL, null=True
    )
    user = models.ForeignKey(
        User, related_name='amazon_sns_subscriptions', on_delete=models.CASCADE, null=True, default=None
    )
    arn = models.CharField(max_length=200, null=True, default=None, unique=True)
    attributes = models.JSONField(default=dict)
    category = models.ForeignKey(
        AmazonSNSSubscriptionCategory, related_name='subscriptions', on_delete=models.SET_NULL, null=True, default=None
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = 'notification_amazonsnssubscription'


class PushRoutineCategory(models.Model):
    code = models.IntegerField(unique=True)
    name = models.CharField(default=None, null=True, max_length=50, unique=True)
    title = models.CharField(max_length=300)
    body = models.CharField(max_length=300)
    description = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notification_pushroutinecategory'


class PushRoutine(models.Model):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6
    DAYS = (
        (MONDAY, '월'),
        (TUESDAY, '화'),
        (WEDNESDAY, '수'),
        (THURSDAY, '목'),
        (FRIDAY, '금'),
        (SATURDAY, '토'),
        (SUNDAY, '일'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='push_routines')
    is_active = models.BooleanField(default=True)
    days = ArrayField(models.IntegerField(choices=DAYS))
    sent_at = ArrayField(models.TimeField())
    category = models.ForeignKey(
        PushRoutineCategory, related_name='push_routines', on_delete=models.SET_NULL, null=True, default=None
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notification_pushroutine'


class PushRoutineCronLog(models.Model):
    code = models.IntegerField()
    name = models.CharField(default=None, null=True, max_length=50)
    sent_at = models.DateTimeField()
    res = models.JSONField(help_text='일단 어떻게 사용할지 모르겠어서, 저장. 이것 보단 publish에 대해 저장을 해야할 것 같음.', default=dict())

    class Meta:
        db_table = 'notification_pushroutinecronlog'
