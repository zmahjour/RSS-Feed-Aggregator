import pika
import json
from interactions.models import Notification
from accounts.models import User

def consumer(queue):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_consume(queue=queue, on_message_callback=notif_callback)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()
