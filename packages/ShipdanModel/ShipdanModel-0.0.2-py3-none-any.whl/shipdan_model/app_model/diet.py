import datetime

from django.contrib.auth import get_user_model
from django.db import models

from shipdan_model.utils.time import KST
from shipdan_model.app_model.food import Dish

User = get_user_model()


class DietBundle(models.Model):
    """
    target_started_at의 사용법
    - 정의 : 식단 서비스에서 시작 날짜와 끝날짜를 의미함.
    - 식단 서비스가 언제부터 언제까지의 식단을 목표로 하는지가 중요.
    - 만약 월요일부터 토요일까지의 식단을 위한 서비스라면, 유저가 화수의 식단만 샀어도 target_stareted_at은 월요일이고, target_ended_at 토요일임.
    - 출고일 추가를 통해 목금토의 식단만을 위한 서비스를 예시로하면, target_started_at은 목요일, target_ended_at은 토요일임.
    - 사용의 편의를 위해 DateField가 아닌 DateTimeField를 사용하였으며, ended_at은 23시 59분 59초가 아닌, 0시 0분 0초로 처리!
    - 23년 8월 6일 현 정책은 target_started_at이 월요일인데, 유저가 화요일 식단부터 샀어도, 월요일에 배송이 됨.

    - operation
        - target_started_at을 배송이 되는 날짜로 생각하여, 출고일과 배송일을 계산 가능
        - 만약 정책이 바뀌어 한 주문에 2번이상 배송을 하는 경우도 로직적으로 처리
    - data
        - 코호트 계산을 target_started_at을 기준으로 처리하면 됨.
        만약 target_started_at이 23년 8월 15일 월요일로 되어있다면, 이 유저의 주문은 8월 7일 월요일 0시 ~ 8월 11일 금요일 12시임을 알 수 있고,
        8월 17일 목요일로 되어있다면, 이 유저의 주문이 8월 11일 금요일 12시 ~ 13일 일요일 23시 59분 59초임을 알 수 있음.
    """
    user = models.ForeignKey(User, related_name='diet_bundles', on_delete=models.CASCADE)
    target_started_at = models.DateTimeField(null=True, default=None)
    target_ended_at = models.DateTimeField(null=True, default=None)
    day_diets = models.ManyToManyField('app_model.DayDiet', related_name='diet_bundles')
    # TODO:food_order의 on_delete null  옵션 확인 받기
    food_order = models.OneToOneField('app_model.FoodOrder', on_delete=models.SET_NULL, null=True, related_name='diet_bundle', )
    day_diet_records = models.ManyToManyField('app_model.DayDietRecord', related_name='diet_bundles')
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = 'diet_dietbundle'


class DayDiet(models.Model):
    user = models.ForeignKey(User, related_name='day_diets', on_delete=models.CASCADE)
    day = models.DateField()
    calorie = models.FloatField(default=0)
    carbohydrate = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    order_deadline = models.DateTimeField(default=datetime.datetime(2099, 12, 31, tzinfo=KST), help_text='주문마감시간')
    order = models.ForeignKey('app_model.FoodOrder', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='day_diets')
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'day'], name='unique user and day')
        ]
        db_table = 'diet_daydiet'


class DayDietFood(models.Model):
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

    day_diet = models.ForeignKey(DayDiet, related_name='foods', on_delete=models.CASCADE, null=True)
    food_product = models.ForeignKey('app_model.FoodProduct', related_name='day_diet_food_products',
                                     on_delete=models.SET_NULL, null=True, blank=True)
    count = models.IntegerField(default=1)
    meal = models.IntegerField(choices=MEAL_TYPE, default=UNDEFINED)
    dish = models.ForeignKey('app_model.Dish', related_name='day_diet_foods', to_field='code', default=Dish.UNDEFINED,
                             on_delete=models.CASCADE)
    prev_replacement = models.ForeignKey('self', on_delete=models.CASCADE, related_name='next_replacements', null=True)
    in_cart = models.BooleanField(default=True)
    is_recommended = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    in_diet = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['day_diet', 'food_product', 'meal', 'dish'],
                                    name='unique day_diet, food, meal and dish')
        ]
        db_table = 'diet_daydietfood'


class MealTag(models.Model):
    name = models.CharField(unique=True, max_length=20, null=True)
    code = models.IntegerField(unique=True, null=True, default=None)

    class Meta:
        db_table = 'diet_mealtag'


class DayDietMealTag(models.Model):
    # tag manytomany 말고 foreignkey로 처리하는게 더 편리함. -> 바꾸지 마시오
    tag = models.ForeignKey(MealTag, related_name='meals', on_delete=models.CASCADE)
    day_diet = models.ForeignKey(DayDiet, related_name='tags', on_delete=models.CASCADE)
    meal = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tag', 'day_diet', 'meal'], name='unique tag, day_diet and meal')
        ]
        db_table = 'diet_daydietmealtag'


class UserMealTag(models.Model):
    meal_tag = models.ForeignKey(MealTag, on_delete=models.CASCADE, related_name='user_meal_tags')
    meal = models.IntegerField(choices=DayDietFood.MEAL_TYPE)
    is_shown = models.BooleanField(default=True)

    users = models.ManyToManyField(User, related_name='meal_tags')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['meal_tag', 'meal'], name='unique tag and meal')
        ]
        db_table = 'diet_usermealtag'


class DayDietMealExclusion(models.Model):
    UNDEFINED = 0
    BREAKFAST = 1
    LUNCH = 2
    DINNER = 3
    SNACK = 4
    MEAL_CODES = (
        (UNDEFINED, '미정'),
        (BREAKFAST, '아침'),
        (LUNCH, '점심'),
        (DINNER, '저녁'),
        (SNACK, '간식'),
    )

    code = models.IntegerField(choices=MEAL_CODES, unique=True)
    day_diets = models.ManyToManyField(DayDiet, related_name='meal_exclusions')

    class Meta:
        db_table = 'diet_daydietmealexclusion'


class DayDietFoodChangeEvent(models.Model):
    CREATE_WEEK_DIET = 100
    REPLACE_WEEK_DIET = 101

    CREATE_DAY_DIET = 200
    REPLACE_DAY_DIET = 201
    DELETE_DAY_DIET = 202

    CREATE_MEAL = 300
    REPLACE_MEAL = 301
    DELETE_MEAL = 302

    CREATE_FOOD = 400
    REPLACE_FOOD = 401
    DELETE_FOOD = 402
    REPLACE_FOOD_BY_BOOKMARKED = 403
    REPLACE_FOOD_BY_BEFORE_DAY_DIET_FOOD = 404

    user = models.ForeignKey(User, related_name='day_diet_change_events', on_delete=models.CASCADE)
    code = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'diet_daydietfoodchangeevent'


class DayDietFoodChangeLog(models.Model):
    change_event = models.ForeignKey(DayDietFoodChangeEvent, related_name='change_logs', on_delete=models.CASCADE)
    day_diet_food = models.ForeignKey(DayDietFood, related_name='change_logs', on_delete=models.CASCADE)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'diet_daydietfoodchangelog'


class SampleMeal(models.Model):
    UNDEFINED = 0
    GOOD = 1
    PROBLEM_SITUATION = 2
    INVISIBLE = 3

    STATE_CODES = (
        (UNDEFINED, '미정'),
        (GOOD, '좋음'),
        (PROBLEM_SITUATION, '문제 상황'),
        (INVISIBLE, '임의로 가림')
    )

    instance_id = models.IntegerField(null=True)
    combination_code = models.IntegerField(default=0)
    sampling_id = models.IntegerField(null=True, unique=True)
    calorie = models.FloatField(default=0)
    carbohydrate = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    sodium = models.FloatField(default=0)
    sugar = models.FloatField(default=0)
    total_price = models.IntegerField(null=True, default=None, blank=True)
    state = models.IntegerField(choices=STATE_CODES, default=GOOD)
    tags = models.ManyToManyField(MealTag, related_name='sample_meal_tags')

    class Meta:
        db_table = 'diet_samplemeal'


class SampleMealFood(models.Model):
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

    sample_meal_instance_id = models.IntegerField(null=True)
    sample_meal = models.ForeignKey(SampleMeal, related_name='foods', on_delete=models.CASCADE)
    food = models.ForeignKey('app_model.Food', related_name='sample_meal_foods', on_delete=models.CASCADE)
    food_product = models.ForeignKey('app_model.FoodProduct', related_name='sample_meal_food_products',
                                     on_delete=models.CASCADE, null=True)
    count = models.IntegerField(default=1)
    dish = models.ForeignKey('app_model.Dish', related_name='sample_meal_foods', to_field='code',
                             default=Dish.UNDEFINED, on_delete=models.CASCADE)

    class Meta:
        db_table = 'diet_samplemealfood'


class SampleMealExceptDay(models.Model):
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

    day = models.IntegerField(choices=DAYS, unique=True)
    sample_meals = models.ManyToManyField(SampleMeal, related_name='except_days')

    class Meta:
        db_table = 'diet_samplemealexceptday'


class DayDietDeadlineModification(models.Model):
    """
    [3.9.2] 배송 불가능한 상황 대응
    - DayDiet의 order_deadline이 앞당겨지는 경우 발생
        ex) 월요일 DayDiet에 대해서 기존에는 금요일 12시 마감 -> 목요일 12시 마감 (Order의 deadline이 목요일 12시로 변경됨에 따라)
    - diet_started_at ~ diet_ended_at애 포함되는 DayDiet에 대해서, order_deadline을 입력받은 deadline으로 지정함
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
    diet_started_at = models.DateField(help_text='order_deadline을 수정할 DayDiet 기간의 시작일')
    diet_ended_at = models.DateField(help_text='order_deadline을 수정할 DayDiet 기간의 종료일')
    deadline = models.DateTimeField(help_text='시작일~종료일에 해당하는 DayDiet들에 대해 지정해주려는 order_deadline')
    change_category = models.IntegerField(choices=CHANGE_CATEGORY, default=UNDEFINED)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = 'diet_daydietdeadlinemodification'


