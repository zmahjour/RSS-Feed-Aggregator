from django.conf import settings
import pika
import json
from interactions.models import Notification
from accounts.models import User


def notif_callback(ch, method, properties, body):
    body = json.loads(body)
    user = User.objects.get(username=body["username"])
    Notification.objects.create(
        user=user, action=body["action"], content=body["notification"]
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consumer(queue):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.RABBITMQ_HOST)
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_consume(queue=queue, on_message_callback=notif_callback)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()
