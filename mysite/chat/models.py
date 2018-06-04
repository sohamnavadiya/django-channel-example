from django.db import models

# Create your models here.

class Record(models.Model):
    event = models.TextField(blank=True, null=True)
    sid = models.TextField(blank=True, null=True)
    cid = models.TextField(blank=True, null=True)
    circle = models.TextField(blank=True, null=True)
    call_member = models.TextField(blank=True, null=True)
    operator = models.TextField(blank=True, null=True)
    cid_type = models.TextField(blank=True, null=True)
    cid_e164 = models.TextField(blank=True, null=True)
    request_time = models.TextField(blank=True, null=True)
    cid_country = models.TextField(blank=True, null=True)
    total_call_duration = models.TextField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    rec_md5_checksum = models.TextField(blank=True, null=True)
    record_duration = models.TextField(blank=True, null=True)
    called_number = models.TextField(blank=True, null=True)


