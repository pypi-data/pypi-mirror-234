from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class HealthProfile(models.Model):
    user = models.OneToOneField(User, related_name='health_profile', on_delete=models.CASCADE)
    height = models.FloatField(help_text='현재 신장', null=True)
    goal_weight = models.FloatField(null=True)
    exercise_time = models.FloatField(default=0, help_text='하루 평균 운동 시간')
    exercise_intensity = models.FloatField(default=0, null=True, help_text='운동 강도')
    job_activity = models.FloatField(null=True)
    sleep_time = models.FloatField(null=True, help_text='단위는 시간')

    class Meta:
        db_table = 'health_healthprofile'


class HealthGoal(models.Model):
    UNDEFINED = 0
    GOAL_T1 = 1
    GOAL_T2 = 2
    GOAL_T3 = 3

    DISTINCT_LOSS = 1
    DISTINCT_GAIN = 2
    MODERATE_LOSS = 3
    MODERATE_GAIN = 4
    HEAlTHY_GOAL = 5

    profile = models.OneToOneField(HealthProfile, related_name='goal', on_delete=models.CASCADE)
    goal_code = models.IntegerField(default=UNDEFINED)
    weight_goal = models.IntegerField(default=UNDEFINED)

    class Meta:
        db_table = 'health_healthgoal'


class Weight(models.Model):
    profile = models.ForeignKey(HealthProfile, related_name='weights', on_delete=models.CASCADE)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'health_weight'


class BodyFat(models.Model):
    # 체지방량입니다. 체지방률 아님!
    profile = models.ForeignKey(HealthProfile, related_name='body_fats', on_delete=models.CASCADE)
    amount = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'health_bodyfat'


class Muscle(models.Model):
    profile = models.ForeignKey(HealthProfile, related_name='muscles', on_delete=models.CASCADE)
    amount = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'health_muscle'


class Allergy(models.Model):
    EGGS = 1
    MILK = 2
    WHEAT = 3
    SHRIMP = 4
    CRAB = 5
    MACKEREL = 6
    WALNUTS = 7
    PORK = 8
    PEANUTS = 9
    SHELLFISH = 10
    PEACH = 11
    BUCKWHEAT = 12
    SOYBEANS = 13
    PINE_NUTS = 14
    TOMATO = 15
    BEEF = 16
    CHICKEN = 17
    MUSSEL = 18
    ABALONE = 19
    OYSTER = 20
    SQUID = 21
    SULFITES = 22

    ALLERGY_CODE = (
        (EGGS, '알류'),
        (MILK, '우유'),
        (WHEAT, '밀'),
        (SHRIMP, '새우'),
        (CRAB, '게'),
        (MACKEREL, '고등어'),
        (WALNUTS, '호두'),
        (PORK, '돼지고기'),
        (PEANUTS, '땅콩'),
        (SHELLFISH, '조개류'),
        (PEACH, '복숭아'),
        (BUCKWHEAT, '메밀'),
        (SOYBEANS, '대두'),
        (PINE_NUTS, '잣'),
        (TOMATO, '토마토'),
        (BEEF, '쇠고기'),
        (CHICKEN, '닭고기'),
        (MUSSEL, '홍합'),
        (ABALONE, '전복'),
        (OYSTER, '굴'),
        (SQUID, '오징어'),
        (SULFITES, '아황산류')
    )

    code = models.IntegerField(choices=ALLERGY_CODE, unique=True)
    name = models.CharField(max_length=20, unique=True)
    text = models.CharField(max_length=50, blank=True, null=True, help_text='사용자에게 보여질 텍스트')
    profiles = models.ManyToManyField(HealthProfile, related_name='allergies')
    foods = models.ManyToManyField('app_model.Food', related_name='allergies')

    class Meta:
        db_table = 'health_allergy'


class Diagnosis(models.Model):
    # 복수형 diagnoses
    profile = models.ForeignKey(HealthProfile, related_name='diagnoses', on_delete=models.CASCADE)
    start_weight = models.FloatField()
    start_body_fat = models.FloatField(null=True)
    start_muscle = models.FloatField(null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    goal_weight = models.FloatField(help_text='목표 체중')
    goal_body_fat = models.FloatField(help_text='목표 체지방량', null=True)
    goal_muscle = models.FloatField(help_text='목표 근육량', null=True)
    goal_at = models.DateTimeField()
    recommend_calorie = models.FloatField(help_text='권장 하루 섭취 에너지(kcal)')
    recommend_protein = models.FloatField(help_text='권장 단백질 섭취량(g)')
    recommend_carbohydrate = models.FloatField(help_text='권장 탄수화물 섭취량(g)')
    recommend_fat = models.FloatField(help_text='권장 지방 섭취량(g)')
    is_checked = models.BooleanField(default=False)

    class Meta:
        db_table = 'health_diagnosis'


class PreferenceFoodCategory(models.Model):
    CHICKEN = 1
    PORK = 2
    BEEF = 3
    SEAFOOD = 4
    BREAD = 5
    SANDWICH = 6
    DESSERT = 7
    BUNSIK = 8
    SALAD = 9
    DOSILAK = 10
    FRIED_RICE = 11
    NOODLES = 12
    DAIRY_PRODUCT = 13
    SNACK = 14
    BREAKFAST_CEREAL = 15
    NUTS = 16
    BEVERAGE = 17
    CARBONATED_DRINK = 18
    JUICE = 19
    SUPPLEMENT_DRINK = 20

    FOOD_PREFERENCE_CODE = (
        (CHICKEN, '닭고기'),
        (PORK, '돼지고기'),
        (BEEF, '소고기'),
        (SEAFOOD, '수산식품'),
        (BREAD, '빵'),
        (SANDWICH, '샌드위치'),
        (DESSERT, '디저트'),
        (BUNSIK, '분식'),
        (SALAD, '샐러드'),
        (DOSILAK, '도시락'),
        (FRIED_RICE, '볶음밥'),
        (NOODLES, '면류'),
        (DAIRY_PRODUCT, '유제품'),
        (SNACK, '과자'),
        (BREAKFAST_CEREAL, '시리얼'),
        (NUTS, '견과류'),
        (BEVERAGE, '음료'),
        (CARBONATED_DRINK, '탄산음료'),
        (JUICE, '과채주스'),
        (SUPPLEMENT_DRINK, '보충제 음료')
    )
    code = models.IntegerField(choices=FOOD_PREFERENCE_CODE, unique=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    text = models.CharField(max_length=50, null=True, blank=True, help_text='사용자에게 보여질 텍스트')
    profiles = models.ManyToManyField(HealthProfile, related_name='preference_food_categories')
    third_categories = models.ManyToManyField('app_model.ThirdCategory', related_name='preference_food_categories')

    class Meta:
        db_table = 'health_preferencefoodcategory'


class MealExclusion(models.Model):
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
    profiles = models.ManyToManyField(HealthProfile, related_name='meal_exclusions')

    class Meta:
        db_table = 'health_mealexclusion'


class DislikeCategoryLayerParameter(models.Model):
    UNDEFINED = 0
    MAIN = 1
    PROTEIN = 2
    SNACK = 3
    DRINK = 4
    GROUP = (
        (UNDEFINED, '미정'),
        (MAIN, '메인'),
        (PROTEIN, '단백질'),
        (SNACK, '간식'),
        (DRINK, '음료')
    )
    group = models.IntegerField(choices=GROUP, default=MAIN)
    code = models.IntegerField(unique=True)
    display = models.CharField(max_length=20)
    is_shown = models.BooleanField(default=True)
    category_codes = models.ManyToManyField('app_model.ThirdCategory', related_name='dislike_layer_parameters')
    profiles = models.ManyToManyField(HealthProfile, related_name='dislike_layer_parameters')

    class Meta:
        db_table = 'health_dislikecategorylayerparameter'


class CustomCalorie(models.Model):
    profile = models.OneToOneField(HealthProfile, on_delete=models.CASCADE, related_name='custom_calorie')
    amount = models.FloatField(default=2000, help_text='유저가 커스텀한 칼로리')
    is_instead = models.BooleanField(default=True, help_text='진단 칼로리 대신에 식단 생성에 사용할지에 대한 값')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'health_customcalorie'


class FoodProductTaste(models.Model):
    UNDEFINED = 0
    GOOD = 1
    BAD = 2
    NEUTRAL = 3

    profile = models.ForeignKey(HealthProfile, related_name='food_product_tastes', on_delete=models.CASCADE)
    food_product = models.ForeignKey('app_model.FoodProduct', related_name='taste_users', on_delete=models.CASCADE)
    taste = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'health_foodproducttaste'


class FoodProductBlock(models.Model):
    """ (23.09.04) deprecated """
    profile = models.ForeignKey(HealthProfile, related_name='food_product_blocks', on_delete=models.CASCADE)
    food_product = models.ForeignKey('app_model.FoodProduct', related_name='food_product_blocks',
                                     on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_blocked = models.BooleanField(default=True)

    class Meta:
        db_table = 'health_foodproductblock'


class FoodProductBlockLog(models.Model):
    """ (23.09.04) deprecated """
    UNDEFINED = 0
    SPICY = 1
    UNLIKE_INGREDIENTS = 2
    NOT_DELICIOUS = 3
    SMALL_PORTIONS = 4

    REASON_CODES = (
        (UNDEFINED, '미정'),
        (SPICY, '너무 매웠어요'),
        (UNLIKE_INGREDIENTS, '싫어하는 식재료가 포함돼 있어요'),
        (NOT_DELICIOUS, '맛 없어요'),
        (SMALL_PORTIONS, '양이 적어요')
    )

    block = models.ForeignKey(FoodProductBlock, related_name='logs', on_delete=models.CASCADE)
    is_blocked = models.BooleanField(default=True)
    reason = models.IntegerField(choices=REASON_CODES, default=UNDEFINED)
    created_at = models.DateTimeField(auto_now_add=True)
    extra = models.CharField(max_length=255, default='', null=True, blank=True)

    class Meta:
        db_table = 'health_foodproductblocklog'
