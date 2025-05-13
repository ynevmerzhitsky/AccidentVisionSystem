from django.contrib import admin

from django.contrib import admin
from .models import AnalysisResult

@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'video_id', 'status', 'incidents_found', 'created_at')
    list_filter = ('status',)
    search_fields = ('video_id',)
    ordering = ('-created_at',)
