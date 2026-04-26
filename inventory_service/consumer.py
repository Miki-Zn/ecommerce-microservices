import pika
import json
import os
from sqlalchemy.orm import Session
from database import SessionLocal
import models

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")

def process_order_message(ch, method, properties, body):
    """This function is called every time a new message arrives."""
    print(f" [x] Received message: {body}")
    try:
        event_data = json.loads(body)
        product_id = event_data.get("product_id")
        quantity_to_deduct = event_data.get("quantity")

        db: Session = SessionLocal()
        product = db.query(models.Product).filter(models.Product.id == product_id).first()

        if product:
            if product.quantity_in_stock >= quantity_to_deduct:
                product.quantity_in_stock -= quantity_to_deduct
                db.commit()
                print(f" [V] Deducted {quantity_to_deduct} items. New stock for product {product_id}: {product.quantity_in_stock}")
            else:
                print(f" [!] Not enough stock for product {product_id}")
        else:
            print(f" [?] Product {product_id} not found")

        db.close()
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f" [x] Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def start_consuming():
    """Настраивает подключение и начинает бесконечно слушать очередь"""
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()
    channel.queue_declare(queue='order_created', durable=True)
    channel.basic_qos(prefetch_count=1)
    
    channel.basic_consume(queue='order_created', on_message_callback=process_order_message)

    print(' [*] Waiting for messages...')
    channel.start_consuming()