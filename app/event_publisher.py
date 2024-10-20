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

connection = connect_to_rabbitmq()
channel = connection.channel()

channel.exchange_declare(exchange='professor_events', exchange_type='topic')

def publish_event(routing_key, message):
    channel.basic_publish(
        exchange='professor_events',
        routing_key=routing_key,
        body=json.dumps(message)
    )