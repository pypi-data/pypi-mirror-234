import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from shipdan_model.utils.time import KST

User = get_user_model()

class FoodOrder(models.Model):
    UNDEFINED = 0
    ORDER_COMPLETE = 1
    PAYMENT_COMPLETE = 2
    DELIVERY_COMPLETE = 3
    CANCEL_ORDER = -10

    FAIL = -20

    ORDER_STATUS = (
        (UNDEFINED, '미정'),
        (ORDER_COMPLETE, '주문완료'),
        (PAYMENT_COMPLETE, '결제완료'),
        (DELIVERY_COMPLETE, '배달완료'),
        (CANCEL_ORDER, '주문취소'),
        (FAIL, '문제상황'),
    )
    order = models.OneToOneField('app_model.Order', related_name='food_order', on_delete=models.CASCADE)
    status = models.IntegerField(
        choices=ORDER_STATUS, default=UNDEFINED,
        help_text='주문에 대한 현재 상태를 의미함. FoodOrderState로 처리하는 것이 join비용이 많이 발생하여, 비정규화함.'
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'food_payment_foodorder'


class FoodOrderState(models.Model):

    # todo: to constant
    UNDEFINED = 0
    ORDER_COMPLETE = 1
    PAYMENT_COMPLETE = 2
    DELIVERY_COMPLETE = 3
    CANCEL_ORDER = -10

    FAIL = -20

    ORDER_STATUS = (
        (UNDEFINED, '미정'),
        (ORDER_COMPLETE, '주문완료'),
        (PAYMENT_COMPLETE, '결제완료'),
        (DELIVERY_COMPLETE, '배달완료'),
        (CANCEL_ORDER, '주문취소'),
        (FAIL, '문제상황'),
    )

    order = models.ForeignKey(FoodOrder, on_delete=models.CASCADE, related_name='states')
    status = models.IntegerField(choices=ORDER_STATUS, default=UNDEFINED)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order', 'status'], name='food order state unique')
        ]
        db_table = 'food_payment_foodorderstate'


class FoodOrderPolicy(models.Model):
    data = models.JSONField(default=dict)  # 추후 기획 변동 가능성 고려 > 유동적 설계
    target = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = 'food_payment_foodorderpolicy'


class FoodDiscount(models.Model):
    food_product = models.ForeignKey('app_model.FoodProduct', related_name='food_discounts', on_delete=models.CASCADE)
    amount = models.IntegerField()
    code = models.IntegerField(null=True, blank=True)
    code_for_devel = models.CharField(max_length=10, blank=True, help_text='개발용 코드입니다. 해당 코드에 따라 이벤트 등의 일을 개발합니다.')
    content = models.CharField(max_length=100, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'food_payment_fooddiscount'


class CouponDiscount(models.Model):
    INFINITY_VALUE = 100000000  # 임의의 큰 값

    UNDEFINED = 0
    EVENT = 1
    INVITATION = 2
    CS = 3
    HOST = 4

    COUPON_CATEGORY = (
        (UNDEFINED, '미정'),
        (INVITATION, '초대코드'),
        (CS, 'cs'),
        (HOST, '초대호스트'),
    )

    user = models.ForeignKey(User, related_name='coupon_discounts', on_delete=models.CASCADE)
    amount = models.IntegerField(null=True, blank=True)
    rate = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], null=True, blank=True)
    code = models.CharField(max_length=20, null=True, default=None)
    code_for_devel = models.CharField(max_length=50, blank=True, help_text='개발용 코드입니다. 해당 코드에 따라 이벤트 등의 일을 개발합니다.')
    coupon_category = models.IntegerField(choices=COUPON_CATEGORY, default=UNDEFINED)
    content = models.CharField(max_length=100, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    used_at = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    min_order_amount = models.IntegerField(null=True, blank=True, default=0, help_text='쿠폰을 적용할 수 있는 최소 주문 금액 입니다.')
    max_amount = models.IntegerField(
        default=INFINITY_VALUE, help_text='쿠폰이 최대로 적용될 수 있는 할인 금액 입니다. 입력 하지 않으면 임의의 큰 값으로 자동 설정 됩니다.'
    )
    actual_discount_amount = models.IntegerField(null=True, blank=True, help_text='결제 시 실제로 할인된 금액 입니다.')

    class Meta:
        db_table = 'food_payment_coupondiscount'


class CouponDiscountTemplate(models.Model):
    amount = models.IntegerField(null=True, blank=True)
    rate = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], null=True, blank=True)
    code = models.CharField(max_length=20, null=True, default=None)
    code_for_devel = models.CharField(max_length=50, null=True, default='', blank=True,
                                      help_text='개발용 코드입니다. 해당 코드에 따라 이벤트 등의 일을 개발합니다.')
    coupon_category = models.IntegerField(choices=CouponDiscount.COUPON_CATEGORY, default=CouponDiscount.UNDEFINED)
    content = models.CharField(max_length=100, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    duration = models.DurationField(null=True, blank=True, default=None)

    used = models.BooleanField(default=True, help_text='사용하지 않을 경우 False처리 해주세요. 편합니다.')

    min_order_amount = models.IntegerField(null=True, blank=True, default=0, help_text='쿠폰을 적용할 수 있는 최소 주문 금액 입니다.')
    max_amount = models.IntegerField(
        default=CouponDiscount.INFINITY_VALUE,
        help_text='쿠폰이 최대로 적용될 수 있는 할인 금액 입니다. 입력 하지 않으면 임의의 큰 값으로 자동 설정 됩니다.'
    )

    def __str__(self):
        return f'{self.id} {self.code} {self.content}'

    class Meta:
        db_table = 'food_payment_coupondiscounttemplate'
        ordering = ['-id']


class CouponDiscountTarget(models.Model):
    coupon_discount_template = models.ForeignKey(
        CouponDiscountTemplate, on_delete=models.CASCADE, related_name='coupon_discount_target'
    )
    reserved_at = models.DateTimeField()
    started_at = models.DateTimeField(
        null=True, blank=True, help_text='비워 있으면 template의 duration과 reserved_at을 기준으로 쿠폰 유효기간을 설정합니다.')
    ended_at = models.DateTimeField(null=True, blank=True)

    emails = models.TextField(default='', help_text='쉼표 없이 한줄씩 적어주세요!')
    invalid_emails = models.TextField(
        default='',
        help_text='유저가 없거나(이메일 잘못기입 혹은 회원탈퇴),is active가 False인 유저입니다. 저장 시, '
                  '자동으로 기입됩니다.'
    )
    is_created = models.BooleanField(default=False, help_text='실제로 생성되면 True로 바뀌며, 추후 업데이트는 불가능합니다.')
    total_target = models.IntegerField(default=0, help_text='전체 유저수입니다.')
    valid_target = models.IntegerField(default=0, help_text='쿠폰이 생성 예상되는 유저수입니다.')
    total_created = models.IntegerField(default=0, help_text='쿠폰이 최종적으로 생성된 유저수입니다.')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'food_payment_coupondiscounttarget'


class EventCouponCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    coupon_discount_template = models.ForeignKey(CouponDiscountTemplate, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'food_payment_eventcouponcode'


class InvitationCouponCode(models.Model):
    user = models.OneToOneField(User, default=None, null=True, related_name='invitation_code',
                                on_delete=models.SET_NULL)
    code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'food_payment_invitationcouponcode'


class CouponCodeMapper(models.Model):
    UNDEFIEND = 0
    EVENT = 1
    INVITATION = 2

    COUPON_CATEGORY = (
        (UNDEFIEND, '미정'),
        (EVENT, '이벤트'),
        (INVITATION, '초대코드')
    )

    code = models.CharField(unique=True, max_length=20)
    coupon_category = models.IntegerField(choices=COUPON_CATEGORY)

    class Meta:
        db_table = 'food_payment_couponcodemapper'


class OrderCouponRelation(models.Model):
    order = models.ForeignKey(FoodOrder, on_delete=models.CASCADE, related_name='coupon_rels')
    coupon = models.ForeignKey(CouponDiscount, on_delete=models.CASCADE, related_name='order_rels')

    class Meta:
        db_table = 'food_payment_ordercouponrelation'


class FoodOrderCouponTemporaryRelation(models.Model):
    order = models.OneToOneField(FoodOrder, on_delete=models.CASCADE, related_name='coupons_temp_rel')
    coupons = models.ManyToManyField(CouponDiscount, related_name='food_order_temp_rel')
    created_at = models.DateTimeField(null=True, auto_now_add=True)

    class Meta:
        db_table = 'food_payment_foodordercoupontemporaryrelation'


class FoodOrderRemark(models.Model):
    order = models.OneToOneField(FoodOrder, on_delete=models.CASCADE, related_name='remark')
    phone = models.CharField(max_length=20, blank=True, default='')
    orderer = models.CharField(max_length=20, blank=True, default='', help_text='주문자 이름')
    content = models.TextField(blank=True)

    class Meta:
        db_table = 'food_payment_foodorderremark'


class FoodOrderAddress(models.Model):
    order_remark = models.OneToOneField(FoodOrderRemark, on_delete=models.CASCADE, related_name='address')
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

    class Meta:
        db_table = 'food_payment_foodorderaddress'


class OrderFoodProductRelation(models.Model):
    order = models.ForeignKey(FoodOrder, on_delete=models.CASCADE, related_name='food_product_rels')
    price = models.IntegerField(default=0, null=True)
    food_product = models.ForeignKey('app_model.FoodProduct', related_name='order_rels', on_delete=models.SET_NULL,
                                     null=True)
    quantity = models.IntegerField()
    delivery = models.ForeignKey('app_model.Delivery', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='order_food_product_rels')
    coupons = models.ManyToManyField(CouponDiscount, related_name='food_product_rels')

    class Meta:
        db_table = 'food_payment_orderfoodproductrelation'


class OrderDeliveryRelation(models.Model):
    order = models.ForeignKey(FoodOrder, on_delete=models.CASCADE, related_name='delivery_rels')
    delivery = models.OneToOneField('app_model.Delivery', on_delete=models.SET_NULL, related_name='order_rel', null=True)
    coupons = models.ManyToManyField(CouponDiscount, related_name='delivery_rels')

    class Meta:
        db_table = 'food_payment_orderdeliveryrelation'


class OrderDayDietLog(models.Model):
    user = models.ForeignKey(User, related_name='order_day_diet_logs', on_delete=models.CASCADE)
    day = models.DateField()

    food_order = models.ForeignKey(
        FoodOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name='day_diet_logs'
    )
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    order_deadline = models.DateTimeField(default=datetime.datetime(2099, 12, 31, tzinfo=KST), help_text='주문마감시간')

    class Meta:
        db_table = 'food_payment_orderdaydietlog'


class OrderDayDietFoodLog(models.Model):
    UNDEFINED = 0
    BREAKFAST = 1
    LUNCH = 2
    DINNER = 3
    SNACK = 4

    MEAL_TYPE = (
        (UNDEFINED, '미정'),
        (BREAKFAST, '아침'),
        (LUNCH, '점심'),
        (DINNER, '저녁'),
        (SNACK, '간식')
    )

    day_diet = models.ForeignKey(OrderDayDietLog, related_name='foods', on_delete=models.CASCADE, null=True)
    food_product = models.ForeignKey(
        'app_model.FoodProduct', related_name='order_day_diet_logs', on_delete=models.SET_NULL, null=True, blank=True
    )
    count = models.IntegerField(default=1)
    price = models.IntegerField()
    unit_cost = models.IntegerField(default=0)
    meal = models.IntegerField(choices=MEAL_TYPE, default=UNDEFINED)
    is_purchased = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = 'food_payment_orderdaydietfoodlog'


class Point(models.Model):
    UNDEFINED = 0
    EVENT = 1
    ORDER = 2

    POINT_CATEGORY = (
        (UNDEFINED, '미정'),
        (ORDER, '구매'),
        (EVENT, '이벤트'),
    )
    user = models.ForeignKey(User, related_name='points', on_delete=models.CASCADE)
    category = models.IntegerField(choices=POINT_CATEGORY, default=UNDEFINED)
    total_amount = models.IntegerField(null=True)
    remain_amount = models.IntegerField(null=True)

    is_usable = models.BooleanField(help_text='사용 가능 여부입니다. 적립 예정과 적립 완료의 상태를 분리하기 위한 필드입니다.')
    available_at = models.DateTimeField(help_text='이용 가능한 날짜입니다.')

    expired_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'food_payment_point'


class PointLog(models.Model):
    UNDEFINED = 0
    EXPECTED = 1
    ACCUMULATED = 2
    CANCELLED = 3
    USED = 4
    USED_CANCEL = 5
    EXPIRED = 6

    POINT_STATUS = (
        (UNDEFINED, '미정'),
        (EXPECTED, '적립 예정'),
        (ACCUMULATED, '적립 완료'),
        (CANCELLED, '적립 취소'),
        (USED, '사용'),
        (USED_CANCEL, '사용 취소'),
        (EXPIRED, '기한 만료')
    )

    point = models.ForeignKey(Point, related_name='logs', on_delete=models.CASCADE)
    amount = models.IntegerField(null=True)
    status = models.IntegerField(choices=POINT_STATUS, default=UNDEFINED)
    content = models.CharField(null=True, blank=True, max_length=100, help_text='적립금 목록에 보여지는 내용입니다.')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'food_payment_pointlog'


class PointPolicy(models.Model):
    data = models.JSONField(default=dict)
    target = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = 'food_payment_pointpolicy'


class OrderPointRelation(models.Model):
    # todo: related_name points_rel로 변경해야함.
    order = models.OneToOneField(FoodOrder, on_delete=models.CASCADE, related_name='points_rels')
    amount = models.IntegerField(null=True)
    points = models.ManyToManyField(Point, related_name='order_rels', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'food_payment_orderpointrelation'


class FoodOrderPointTemporaryRelation(models.Model):
    order = models.OneToOneField(FoodOrder, on_delete=models.CASCADE, related_name='points_temp_rel')
    amount = models.IntegerField(null=True)
    points = models.ManyToManyField(Point, related_name='food_order_temp_rel')
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'food_payment_foodorderpointtemporaryrelation'
