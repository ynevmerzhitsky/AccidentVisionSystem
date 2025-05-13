from django.shortcuts import render

from django.http import JsonResponse
from .tasks import process_video_task

def launch_process(request, video_id):
    # Enqueue the task
    async_result = process_video_task.apply_async(args=[video_id], queue='task')
    return JsonResponse({'task_id': async_result.id}, status=202)
