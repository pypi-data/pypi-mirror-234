from django.db import models


class DeployRestTime(models.Model):
    finished_at = models.DateTimeField()
    code = models.IntegerField(default=-3000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'core_deployresttime'


class AppVersion(models.Model):
    ANDROID = 1
    IOS = 2
    APP_OS = (
        (ANDROID, 'android'),
        (IOS, 'ios')
    )

    app_os = models.IntegerField(choices=APP_OS)
    latest_version = models.CharField(max_length=10)
    required_version = models.CharField(max_length=10)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'core_appversion'


class AppTutorialSwitch(models.Model):  # todo 이거 필요함?
    # 잠시 있을 칭구...
    on = models.BooleanField(default=True)

    class Meta:
        db_table = 'core_apptutorialswitch'
