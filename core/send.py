from django.conf import settings
import pika
import json


def publisher(body):
    queue = body.get("action")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.RABBITMQ_HOST)
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    body = json.dumps(body)
    channel.basic_publish(exchange="", routing_key=queue, body=body)

    print("Message sent.")
    connection.close()
