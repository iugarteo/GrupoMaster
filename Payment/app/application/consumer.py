import pika

public_key = None


def init_rabbitmq():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='global', exchange_type='topic', durable=True)
    #channel.exchange_declare(exchange='services', exchange_type='topic', durable=True)

    result = channel.queue_declare('payment', durable=True)
    #result = channel.queue_declare('services', durable=True)
    queue_name = result.method.queue

    channel.queue_bind(
        exchange='global', queue="payment", routing_key="client.key")
    #channel.queue_bind(
        #exchange='services', queue="services", routing_key="*.*")

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    print("Waiting for event...")
    channel.start_consuming()


def callback(ch, method, properties, body):
    print(" [x] {} {}".format(method.routing_key, body))
    public_key = body


def get_public_key():
    return public_key
