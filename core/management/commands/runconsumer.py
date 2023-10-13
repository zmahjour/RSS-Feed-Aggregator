from django.core.management.base import BaseCommand
from core.receive import consumer


class Command(BaseCommand):
    help = "Run the RabbitMQ consumer"

    def add_arguments(self, parser):
        parser.add_argument("queue", type=str)

    def handle(self, *args, **options):
        queue = options["queue"]
        consumer(queue=queue)
