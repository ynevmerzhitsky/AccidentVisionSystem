from celery import shared_task, current_app
import json

@shared_task
def process_video_task(video_id):
    # Simulate processing
    result = {
        'video_id': video_id,
        'status': 'processed',
        'incidents_found': 3
    }
    # Publish to a dedicated “task_result” exchange/queue
    with current_app.producer_or_acquire() as producer:
        producer.publish(
            json.dumps(result),
            exchange='',
            routing_key='task_result',
            serializer='json'
        )

    return result