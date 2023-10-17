import numpy as np
from food.models import FoodProduct
from diet.models import SampleMeal, SampleMealFood, MealTag
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import F, Value as V, OuterRef, Exists, Q
from health.models import Allergy

ALLERGY_COUNT = len(Allergy.ALLERGY_CODE) + 1
FOOD_COUNT_IN_ONE_MEAL = 3
WEEK_DAYS_COUNT = 7
try:
    MEAL_TAGS_COUNT = MealTag.objects.all().count()
except:
    MEAL_TAGS_COUNT = 3

food_product_numpy_dtype = [
        ('id', 'u4'), ('calorie', 'u2'), ('carbohydrate', 'f2'), ('protein', 'f2'), ('fat', 'f2'),
        ('sugar', 'f2'), ('sodium', 'f2'), ('price', 'u2'), ('food__group__code', 'u2'),
        ('food__categories__code', 'u2'),
        ('is_available', '?'), ('is_shown', '?'), ('allergies', '?', ALLERGY_COUNT),
        ('food_except_days', '?', WEEK_DAYS_COUNT)
]

week_diet_service_np_food_product_dtype = [
    ('id', 'u4'), ('name', 'U50'), ('sub_classification', 'u2'), ('calorie', 'u2'),
    ('carbohydrate', 'f2'), ('protein', 'f2'), ('fat', 'f2'),
    ('sugar', 'f2'), ('sodium', 'f2'), ('price', 'u2'), ('food__group__code', 'u2'),
    ('food__categories__code', 'u2'),
    ('is_available', '?'), ('is_shown', '?'), ('allergies', '?', ALLERGY_COUNT),
    ('food_except_days', '?', WEEK_DAYS_COUNT)
]

sample_meal_numpy_dtype = [
        ('id', 'u4'), ('calorie', 'f2'), ('carbohydrate', 'f2'), ('protein', 'f2'), ('fat', 'f2'),
        ('sugar', 'f2'), ('sodium', 'f2'), ('combination_code', 'u1'), ('total_price', 'u2'),
        ('allergies', '?', ALLERGY_COUNT + 1), ('food_products', 'u4', FOOD_COUNT_IN_ONE_MEAL),
        ('food_categories_code', 'u2', FOOD_COUNT_IN_ONE_MEAL),
        ('meal_except_days', '?', WEEK_DAYS_COUNT), ('meal_tags_code', '?', MEAL_TAGS_COUNT + 1)
]


def make_food_products_numpy(except_products_id=None):
    food_products = list(FoodProduct.objects.exclude(
        id=except_products_id
    ).filter(
        is_available=True, is_shown=True, is_approved=True
    ).annotate(
        allergies=ArrayAgg(F('food__allergies__code'), default=V([])),
        calorie=F('food__nutrient__calorie') * F('food__nutrient__proper_gram') / V(100),
        carbohydrate=F('food__nutrient__carbohydrate') * F('food__nutrient__proper_gram') / V(100),
        protein=F('food__nutrient__protein') * F('food__nutrient__proper_gram') / V(100),
        fat=F('food__nutrient__fat') * F('food__nutrient__proper_gram') / V(100),
        sugar=F('food__nutrient__sugar') * F('food__nutrient__proper_gram') / V(100),
        sodium=F('food__nutrient__sodium') * F('food__nutrient__proper_gram') / V(100),
        food_except_days=ArrayAgg(F('except_days__day'), default=V([])),
    ).values_list(
        'id', 'calorie', 'carbohydrate', 'protein', 'fat', 'sugar', 'sodium', 'price',
        'food__group__code', 'food__categories__code', 'is_available', 'is_shown', 'allergies', 'food_except_days'
    ))

    food_product_single_data_len = len(food_products[0])

    food_products = [
        (
            *food_product[:food_product_single_data_len - 2],
            *[[allergy in food_product[food_product_single_data_len - 2] for allergy in range(ALLERGY_COUNT)]],
            *[[except_day in food_product[food_product_single_data_len - 1] for except_day in range(WEEK_DAYS_COUNT)]],
        ) for food_product in food_products
    ]

    np_food_products = np.array(food_products, dtype=food_product_numpy_dtype)

    return np_food_products
