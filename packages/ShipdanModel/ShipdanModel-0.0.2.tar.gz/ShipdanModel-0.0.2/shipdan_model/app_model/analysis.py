from django.db import models


class TotalAmplitudeBatchEventResult(models.Model):
    total_event = models.IntegerField()
    content = models.CharField(max_length=100, help_text='어떤 내용인지 설명', default='')
    event_type = models.CharField(max_length=100, default='')
    event_property = models.JSONField(default=dict, help_text='기본 이벤트 프로퍼티')
    has_error = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'analysis_totalamplitudebatcheventresult'


class AmplitudeBatchEventResult(models.Model):
    upper = models.ForeignKey(TotalAmplitudeBatchEventResult, on_delete=models.CASCADE, related_name='lowers')

    start_batch = models.IntegerField()
    end_batch = models.IntegerField()
    code = models.IntegerField()
    events_ingested = models.IntegerField(null=True)
    payload_size_bytes = models.BigIntegerField(null=True)
    server_upload_time = models.BigIntegerField(null=True, help_text='시간 ms입니다.')
    error = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'analysis_amplitudebatcheventresult'
