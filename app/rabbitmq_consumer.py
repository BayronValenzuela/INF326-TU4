import pika # type: ignore
import json
import threading

def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f"Recibido mensaje: {message}")

def start_consuming(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters('user_service_rabbitmq', 5672, '/', pika.PlainCredentials('user', 'password')))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(f"Esperando mensajes en la cola '{queue_name}'...")
    channel.start_consuming()

def run_consumer(queue_name):
    consumer_thread = threading.Thread(target=start_consuming, args=(queue_name,))
    consumer_thread.start()
