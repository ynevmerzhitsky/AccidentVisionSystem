import json
import socket
from django.core.management.base import BaseCommand
from kombu import Connection, Exchange, Queue
from core.models import AnalysisResult
from django.conf import settings

class Command(BaseCommand):
    help = "Consume task_result with automatic reconnection"

    def handle(self, *args, **options):
        broker_url = settings.BROKER_URL
        queue = Queue('task_result', Exchange('', type='direct'), routing_key='task_result')

        def consume():
            with conn.Consumer(queue, callbacks=[process_message]):
                while True:
                    try:
                        conn.drain_events(timeout=1)
                    except socket.timeout:
                        conn.heartbeat_check()

        def process_message(body, message):
            data = json.loads(body)
            AnalysisResult.objects.create(
                video_id=data['video_id'],
                status=data['status'],
                incidents_found=data['incidents_found']
            )
            message.ack()
            print(f"Saved result for video {data['video_id']}")

        with Connection(broker_url, heartbeat=60) as conn:
            # Correct usage: pass conn as 'obj' and consume as 'fun'
            safe_consume = conn.ensure(conn, consume,
                                       errback=lambda exception, interval: self.stderr.write(
                                          f"Reconnect failed: {exception}, retrying in {interval}s"),
                                       max_retries=None,
                                       interval_start=1,
                                       interval_step=2,
                                       interval_max=10)
            safe_consume()

