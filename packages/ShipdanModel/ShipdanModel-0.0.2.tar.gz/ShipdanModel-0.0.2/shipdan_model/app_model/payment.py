import datetime

from django.contrib.auth import get_user_model
from django.db import models

from shipdan_model.app_model.constant import DIET_PAYMENT_SCHEDULE_STATUS, DietPaymentScheduleStatus
from shipdan_model.utils.time import KST

User = get_user_model()


class Order(models.Model):
    PG = 1

    ORDER_TYPES = {
        (PG, 'PG')
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_type = models.IntegerField(choices=ORDER_TYPES, default=1, help_text="결제 방법")
    merchant_uid = models.CharField(max_length=30, null=True, default=None, blank=True, unique=True)
    imp_uid = models.CharField(max_length=100, default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(null=True)
    deadline = models.DateTimeField(default=datetime.datetime(2099, 12, 31, tzinfo=KST), help_text='주문마감시간')

    class Meta:
        db_table = 'payment_order'


class OrderPaymentNoti(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='noti', null=True)
    is_noti = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payment_orderpaymentnoti'


class IamportCustomerUid(models.Model):
    """
    .. Note::
        -

    """
    UNDEFINED = 0
    REGISTERED = 1
    DELETED = -1

    STATES = (
        (UNDEFINED, '미정'),
        (REGISTERED, '등록완료'),
        (DELETED, '삭제')
    )
    user = models.ForeignKey(User, related_name='customer_uids', on_delete=models.CASCADE)
    card_name = models.CharField(max_length=20, null=True, blank=True, default=None)
    customer_uid = models.CharField(max_length=50)
    status = models.IntegerField(choices=STATES, default=UNDEFINED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'iamport_customeruid'

    def __str__(self):
        return self.customer_uid


class IamportOrder(models.Model):
    """
    .. Note::
        - Iamport 주문기록을 저장합니다.
        - imp_uid: 주문이 정상적으로 완료된 경우 Iamport 에서 넘겨주는 imp_uid 를 저장합니다.
        - is_canceled: 주문이 취소된 경우 True 아닌 경우 False 입니다.

    """
    UNPAID = 0
    PAID = 1
    CANCELED = -1
    FAILURE = -20

    PAY_STATUS = (
        (UNPAID, '미결제'),
        (PAID, '결제완료'),
        (CANCELED, '결제취소'),
        (FAILURE, '결제실패')
    )

    user = models.ForeignKey(User, related_name='iamport_orders', on_delete=models.CASCADE)
    customer_uid = models.ForeignKey(IamportCustomerUid, null=True, related_name='orders',
                                     on_delete=models.CASCADE)

    price = models.IntegerField()
    imp_uid = models.CharField(max_length=100, default=None, null=True, unique=True, )
    merchant_uid = models.CharField(max_length=100)

    status = models.IntegerField(choices=PAY_STATUS, default=0)
    status_description = models.TextField(default='', blank=True)
    name = models.TextField(verbose_name='주문명')

    is_canceled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payment_iamportorder'


class IamportWebhookLog(models.Model):
    STATUS_READY = 1
    STATUS_PAID = 2
    STATUS_CANCELLED = 3
    STATUS_FAILURE = 4

    STATUS_CHOICES = (
        (STATUS_READY, '가상계좌발급완료'),
        (STATUS_PAID, '결제완료'),
        (STATUS_CANCELLED, '결제취소'),
        (STATUS_FAILURE, '결제실패')
    )

    STATUS_MAP = {
        STATUS_READY: '가상계좌발급완료',
        STATUS_PAID: '결제완료',
        STATUS_CANCELLED: '결제취소',
        STATUS_FAILURE: '결제실패'
    }

    STATUS_TEXT_MAP = {
        'ready': STATUS_READY,
        'paid': STATUS_PAID,
        'cancelled': STATUS_CANCELLED,
        'failed': STATUS_FAILURE,
    }

    iamport_order = models.ForeignKey(IamportOrder, related_name='logs', on_delete=models.CASCADE)
    receipt = models.JSONField(default=dict)
    status = models.IntegerField(choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payment_iamportwebhooklog'


class IamportCancelLog(models.Model):
    iamport_order = models.ForeignKey(IamportOrder, related_name='cancel_log', on_delete=models.CASCADE)
    response = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payment_iamportcancellog'


class IamportScheduleLog(models.Model):
    """
    .. Note::
        - Iamport 스케쥴 예약시 남는 로그입니다.
    """
    order = models.OneToOneField(IamportOrder, related_name='schedule', on_delete=models.CASCADE)
    schedule_at = models.FloatField(max_length=60)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payment_iamportschedulelog'


class DietPaymentScheduleAddress(models.Model):
    """ 자동 결제 배송지 FoodOrderRemark, FoodOrderAddress 필드 값 """
    user = models.ForeignKey(User, related_name='diet_payment_schedule_addresses', null=True,
                             on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, default='')
    orderer = models.CharField(max_length=20, blank=True, default='', help_text='주문자 이름')
    content = models.TextField(blank=True)
    zonecode = models.CharField(max_length=10, verbose_name='우편번호')
    sido = models.CharField(max_length=10, verbose_name='도/시 이름')
    sigungu = models.CharField(max_length=10, verbose_name='시/군/구 이름')
    bname = models.CharField(max_length=20, verbose_name='법정동/법정리 이름', blank=True, null=True)
    bcode = models.PositiveBigIntegerField(verbose_name='법정동코드')
    roadAddress = models.CharField(max_length=50, verbose_name='도로명', blank=True, null=True)
    buildingName = models.CharField(max_length=50, verbose_name='건물명', blank=True, null=True)
    jibunAddress = models.CharField(max_length=50, verbose_name='지번', blank=True, null=True)
    autoRoadAddress = models.CharField(max_length=50, verbose_name='대체 도로명주소', blank=True, null=True)
    extra = models.CharField(max_length=100, verbose_name='상세주소', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payment_dietpaymentscheduleaddress'


class DietPaymentSchedule(models.Model):
    """ 자동 결제 스케줄, 자동 결제를 이용하는 유저에 한해 매주 생성"""

    user = models.ForeignKey(User, related_name='diet_payment_schedules', on_delete=models.CASCADE)
    status = models.IntegerField(choices=DIET_PAYMENT_SCHEDULE_STATUS, default=DietPaymentScheduleStatus.UNDEFINED,
                                 help_text='현재 상태, Log의 비정규화 필드')
    payment_at = models.DateTimeField()
    customer_uid = models.ForeignKey(IamportCustomerUid, related_name='diet_payment_schedules',
                                     on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(DietPaymentScheduleAddress, related_name='diet_payment_schedules',
                                on_delete=models.SET_NULL, null=True)
    coupon_use = models.BooleanField(default=True, help_text='쿠폰 자동 적용 여부')
    diet_bundle = models.OneToOneField('app_model.DietBundle', related_name='diet_payment_schedule', null=True,
                                       on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'payment_at'], name='DietPaymentSchedule user payment_at unique')
        ]
        db_table = 'payment_dietpaymentschedule'


class DietPaymentScheduleLog(models.Model):
    """ 자동 결제 로깅 """
    schedule = models.ForeignKey(DietPaymentSchedule, related_name='logs', on_delete=models.CASCADE)
    status = models.IntegerField(choices=DIET_PAYMENT_SCHEDULE_STATUS, default=DietPaymentScheduleStatus.UNDEFINED)
    content = models.TextField(max_length=255, default='', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payment_dietpaymentschedulelog'


class DietPaymentScheduleProfile(models.Model):
    """ 자동결제 현재 상태값. Template 역할 """

    EXPECTED = 0
    REGISTERED = 1
    SKIP = 2
    CANCEL = -1

    SCHEDULE_STATUS = (
        (EXPECTED, '등록예정'),
        (REGISTERED, '사용'),
        (SKIP, '건너뜀'),
        (CANCEL, '해지'),
    )

    user = models.OneToOneField(User, related_name='diet_payment_schedule_profile', on_delete=models.CASCADE)
    status = models.IntegerField(choices=SCHEDULE_STATUS, default=EXPECTED, help_text='현재 상태')
    coupon_use = models.BooleanField(default=True, help_text='쿠폰 자동 적용 현재 상태')
    consecutive_week = models.IntegerField(default=0, help_text='현재 연속 결제 주수')
    customer_uid = models.OneToOneField(IamportCustomerUid, related_name='diet_payment_schedule_profile',
                                        on_delete=models.SET_NULL, null=True)
    address = models.OneToOneField(DietPaymentScheduleAddress, related_name='diet_payment_schedule_profile',
                                   on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payment_dietpaymentscheduleprofile'


class OrderDeadlineModification(models.Model):
    """
    [3.9.2] 배송 불가능한 상황 대응
    - Order의 deadline이 앞당겨지는 경우 발생 ex) 기존 금요일 12시 마감 -> 목요일 12시 마감
    - 하나의 주간에 마감일이 2개 존재함 - 금 12시 일 24시(=차주 월 0시)
    - 이 중 하나의 마감일이 변경되더라도 로직적으로 두 마김일을 모두 입력 받음
    - 이때, 하나의 주간은 order_started_at으로 결정. 이는 항상 월요일에 해당해야 함 (order_dended_at은 자동으로 해당 주의 일요일로 계산함)
    """
    UNDEFINED = 0
    DELIVERY = 1
    STORE = 2
    ETC = 3

    CHANGE_CATEGORY = (
        (UNDEFINED, '미정'),
        (DELIVERY, '물류 대행사의 배송불가'),
        (STORE, '입점사의 식품 조달 불가'),
        (ETC, '기타')
    )
    order_started_at = models.DateField(help_text='order 기간의 시작일(월요일로 설정)')
    order_ended_at = models.DateField(null=True, help_text='order기간의 종료일(자동으로 일요일로 계산함)')
    first_deadline = models.DateTimeField(help_text='기존 금 12시 주문 마감일 -> 변경할 datetime')
    second_deadline = models.DateTimeField(help_text='기존 차주 월 0시 주문 마감일 -> 변경할 datetime')
    change_category = models.IntegerField(choices=CHANGE_CATEGORY, default=UNDEFINED)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = 'payment_orderdeadlinemodification'
