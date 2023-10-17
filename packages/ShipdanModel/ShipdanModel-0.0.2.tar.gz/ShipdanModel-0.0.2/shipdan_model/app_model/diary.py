import datetime

from django.contrib.auth import get_user_model
from django.db import models

from shipdan_model.app_model.food import NutrientMeta, UnitMeta, FoodGroup
from shipdan_model.app_model.food_payment import OrderDayDietFoodLog

User = get_user_model()

class FoodProductLog(models.Model):
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

    food_product = models.ForeignKey('app_model.FoodProduct', related_name='logs', on_delete=models.SET_NULL, null=True,
                                     blank=True)
    count = models.IntegerField(default=1)
    meal = models.IntegerField(choices=MEAL_TYPE, default=UNDEFINED)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = 'diary_foodproductlog'


class UserFoodProductLog(models.Model):
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

    USER = 1
    REFERENCE = 2

    USER_SOURCE = 1
    REFERENCE_SOURCE = 2

    DATA_SOURCE_TYPE = (
        (USER_SOURCE, '직접 등록'),
        (REFERENCE_SOURCE, '외부 등록'),
    )

    food_product = models.ForeignKey('app_model.UserFoodProduct', related_name='logs', on_delete=models.SET_NULL, null=True,
                                     blank=True)
    count = models.IntegerField(default=1)
    meal = models.IntegerField(choices=MEAL_TYPE, default=UNDEFINED)
    data_source_type = models.IntegerField(choices=DATA_SOURCE_TYPE, default=USER_SOURCE)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = 'diary_userfoodproductlog'


class DayDietFoodRecordFood(models.Model):
    sku = models.CharField(max_length=20, help_text='재고관리코드', null=True)
    name = models.CharField(max_length=255)
    dishes = models.ManyToManyField('app_model.Dish', related_name='record_foods')
    brand = models.ForeignKey('app_model.FoodBrand', null=True, blank=True, related_name='record_foods',
                              on_delete=models.SET_NULL)
    group = models.ForeignKey('app_model.FoodGroup', null=True, blank=True, to_field='code', default=FoodGroup.UNDEFINED,
                              related_name='record_foods',
                              on_delete=models.SET_DEFAULT)
    storage_method = models.ForeignKey('app_model.StorageMethod', on_delete=models.SET_NULL, null=True, default=None)

    class Meta:
        db_table = 'diary_daydietfoodrecordfood'


class DayDietFoodRecordFoodProduct(models.Model):
    sku = models.CharField(max_length=20, help_text='재고관리코드', null=True)
    food = models.ForeignKey(DayDietFoodRecordFood, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'diary_daydietfoodrecordfoodproduct'


def day_diet_food_product_image_path(instance, filename):
    now = datetime.datetime.now()
    filename = filename.split('/')[-1]
    return 'spark/day_diet_record/{}_{}'.format(now, filename)


class DayDietFoodRecordImage(models.Model):
    product = models.ForeignKey(DayDietFoodRecordFoodProduct, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=day_diet_food_product_image_path)
    code = models.IntegerField(default=100)
    code_index = models.IntegerField(default=0)

    class Meta:
        ordering = ['code', 'code_index']
        db_table = 'diary_daydietfoodrecordimage'

class DayDietFoodRecordUnit(UnitMeta, models.Model):
    food_product = models.ForeignKey(DayDietFoodRecordFoodProduct, related_name='units', on_delete=models.CASCADE)

    class Meta:
        db_table = 'diary_daydietfoodrecordunit'


class DayDietFoodRecordNutrient(NutrientMeta, models.Model):
    food = models.OneToOneField(DayDietFoodRecordFood, related_name='nutrient', on_delete=models.CASCADE)

    class Meta:
        db_table = 'diary_daydietfoodrecordnutrient'


class DayDietRecord(models.Model):
    user = models.ForeignKey(User, related_name='day_diet_records', on_delete=models.CASCADE)
    day = models.DateField()
    diagnosis = models.ForeignKey('app_model.Diagnosis', related_name='day_diet_records', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'day'], name='unique user and day for DayDietRecord')
        ]
        db_table = 'diary_daydietrecord'


class DayDietFoodRecord(models.Model):
    UNDEFINED = 0
    PURCHASED_FOOD = 1
    USER_FOOD = 2
    FOOD_PRODUCT = 3
    LOG_TYPE = (
        (UNDEFINED, '미정'),
        (PURCHASED_FOOD, '구매한 식품'),
        (USER_FOOD, '직접 추가한 식품'),
        (FOOD_PRODUCT, '기존 식품'),
    )

    DELETED = -1
    RECORDED = 1
    RECORD_STATUS = (
        (UNDEFINED, '미정'),
        (RECORDED, '기록 완료'),
        (DELETED, '기록 삭제'),
    )

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

    day_diet_record = models.ForeignKey(DayDietRecord, related_name='foods', on_delete=models.CASCADE, null=True)

    log_type = models.IntegerField(choices=LOG_TYPE, default=UNDEFINED)
    status = models.IntegerField(choices=RECORD_STATUS, default=UNDEFINED)
    meal = models.IntegerField(choices=MEAL_TYPE, default=UNDEFINED)
    food_product = models.ForeignKey(DayDietFoodRecordFoodProduct, related_name='day_diet_records',
                                     on_delete=models.SET_NULL, null=True)
    order_day_diet_food_log = models.ForeignKey(OrderDayDietFoodLog, related_name='day_diet_records',
                                                on_delete=models.SET_NULL, null=True)
    food_product_log = models.ForeignKey(FoodProductLog, related_name='day_diet_records', on_delete=models.SET_NULL,
                                         null=True)
    user_food_product_log = models.ForeignKey(UserFoodProductLog, related_name='day_diet_records',
                                              on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'diary_daydietfoodrecord'


class SearchFoodProductLog(models.Model):
    UNDEFINED = 0
    DELETED = 1
    SEARCHED = 2

    SEARCH_STATUS = (
        (UNDEFINED, '미정'),
        (SEARCHED, '검색 완료'),
        (DELETED, '검색 삭제'),
    )

    user = models.ForeignKey(User, related_name='user_search_food_products', on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    status = models.IntegerField(choices=SEARCH_STATUS, default=UNDEFINED)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = 'diary_searchfoodproductlog'