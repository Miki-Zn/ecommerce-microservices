import pika
import json
import os

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")

def publish_order_created_event(order_data: dict):
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()
    
    channel.queue_declare(queue='order_created', durable=True)
    
    channel.basic_publish(
        exchange='',
        routing_key='order_created',
        body=json.dumps(order_data),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        )
    )
    connection.close()