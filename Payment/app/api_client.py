import json
from datetime import datetime

import pika


class ApiClient:
    @staticmethod
    def log(severity, method, message):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='payment', exchange_type='topic')

        now = datetime.now()
        timestamp = now.strftime("%m/%d/%Y %H:%M:%S")
        data = {'timestamp': timestamp,
                'severity': severity,
                'method': method,
                'message': message}

        json_message = json.dumps(data)
        channel.basic_publish(
            exchange='payment', routing_key="payment.log", body=json_message,
            properties=pika.BasicProperties(delivery_mode=2))
        connection.close()
