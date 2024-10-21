import pika # type: ignore

def consume_all_messages():
    # Configuración de credenciales y conexión a RabbitMQ
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='user_service_rabbitmq',
            port=5672,
            credentials=credentials
        )
    )
    channel = connection.channel()

    # Declarar el exchange de tipo 'topic'
    exchange_name = 'entity_events'
    channel.exchange_declare(exchange=exchange_name, exchange_type='topic')

    # Declarar una cola exclusiva (temporal) para este consumidor
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    # Vincular la cola temporal al exchange con un binding genérico ('#' para recibir todos los mensajes)
    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='#')

    # Definir la función de callback para manejar los mensajes recibidos
    def callback(ch, method, properties, body):
        routing_key = method.routing_key
        print(f"Received message with routing_key={routing_key}: {body.decode()}")

    # Configurar el consumidor para la cola temporal
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print("Waiting for all messages. To exit press CTRL+C")
    channel.start_consuming()

# Ejemplo de uso
consume_all_messages()