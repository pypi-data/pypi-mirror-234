from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# todo 솔직히 아는 것 없어서 다 가져옴 - 검수 요망
class DietOrderSurvey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diet_order_surveys')
    question_category = models.IntegerField()
    answer = models.JSONField(default=dict)
    extra = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'diet_survey_dietordersurvey'


class DietOrderSurveyComplete(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diet_order_surveys_completed')
    diet_order = models.OneToOneField(
        'app_model.FoodOrder', related_name='surveys_completed', on_delete=models.CASCADE
    )
    answer = models.IntegerField(help_text='complete 상태')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'diet_survey_dietordersurveycomplete'


class DayDietSurveyComplete(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='day_diet_surveys_completed')
    day_diet = models.OneToOneField('app_model.OrderDayDietLog', related_name='survey_completed',
                                    on_delete=models.CASCADE)
    answer = models.IntegerField(help_text='complete 상태')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'diet_survey_daydietsurveycomplete'


class DietOrderSurveyRelation(models.Model):
    survey = models.OneToOneField(DietOrderSurvey, related_name='diet_order_relation', on_delete=models.CASCADE)
    diet_order = models.ForeignKey('app_model.FoodOrder', related_name='survey_relations', on_delete=models.CASCADE)

    class Meta:
        db_table = 'diet_survey_dietordersurveyrelation'


class DietMealSurveyRelation(models.Model):
    survey = models.OneToOneField(DietOrderSurvey, related_name='diet_meal_relation', on_delete=models.CASCADE)
    day_diet = models.ForeignKey('app_model.OrderDayDietLog', related_name='meal_survey_relations',
                                 on_delete=models.CASCADE)
    meal = models.IntegerField()

    class Meta:
        db_table = 'diet_survey_dietmealsurveyrelation'


class DietFoodSurveyRelation(models.Model):
    survey = models.OneToOneField(DietOrderSurvey, related_name='diet_food_relation', on_delete=models.CASCADE)
    day_diet_food = models.ForeignKey('app_model.OrderDayDietFoodLog', related_name='survey_relations',
                                      on_delete=models.CASCADE)

    class Meta:
        db_table = 'diet_survey_dietfoodsurveyrelation'


class FoodProductSurveyRelation(models.Model):
    survey = models.OneToOneField(DietOrderSurvey, related_name='food_product_relation', on_delete=models.CASCADE)
    food_product = models.ForeignKey('app_model.FoodProduct', related_name='survey_relations', on_delete=models.CASCADE)

    class Meta:
        db_table = 'diet_survey_foodproductsurveyrelation'
