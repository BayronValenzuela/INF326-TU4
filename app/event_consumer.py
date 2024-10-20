import pika # type: ignore
import json
import time

def connect_to_rabbitmq():
    while True:
        try:
            credentials = pika.PlainCredentials('user', 'password')
            parameters = pika.ConnectionParameters('rabbitmq', credentials=credentials, heartbeat=600)
            connection = pika.BlockingConnection(parameters)
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ no está disponible, reintentando en 5 segundos...")
            time.sleep(5)

def callback(ch, method, properties, body):
    print(f" [x] Received {method.routing_key}: {body}")

connection = connect_to_rabbitmq()
channel = connection.channel()

channel.exchange_declare(exchange='professor_events', exchange_type='topic')

queue = channel.queue_declare(queue='', exclusive=True)
queue_name = queue.method.queue

channel.queue_bind(exchange='professor_events', queue=queue_name, routing_key='professor.*.*')

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()