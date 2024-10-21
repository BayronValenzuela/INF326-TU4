import pika # type: ignore

def send_message_to_rabbitmq(queue_name: str, message: str):
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='user_service_rabbitmq',
            port=5672,
            credentials=credentials
            )
    )
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )
    
    connection.close()