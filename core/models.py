from django.db import models

from django.db import models

class AnalysisResult(models.Model):
    id = models.AutoField(primary_key=True)
    video_id = models.IntegerField()
    status = models.CharField(max_length=50)
    incidents_found = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
