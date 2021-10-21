import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='payment', exchange_type='topic')

result = channel.queue_declare('log', durable=True)
queue_name = result.method.queue


def callback(ch, method, properties, body):
    print(" [x] {} {}".format(method.routing_key, body))


channel.queue_bind(
        exchange='payment', queue="log", routing_key="payment.log")

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

print("Waiting for event...")
channel.start_consuming()
