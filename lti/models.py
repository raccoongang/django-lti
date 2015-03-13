from django.db import models

class LTIUser(models.Model):
    user_id = models.CharField(max_length=255, blank=False)
    all_data = models.CharField(max_length=1024, blank=False)
    user_fk = models.PositiveIntegerField(null=True)
