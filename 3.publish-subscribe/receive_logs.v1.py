import time
import pika
import sys
import os
import dotenv

dotenv.load_dotenv()

host = os.getenv("HOST")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)    

    queue_name = result.method.queue
    channel.queue_bind(exchange='logs', queue=queue_name)

    def callback1(ch, method, properties, body):
        print(" [x]1 %r" % body)

    def callback2(ch, method, properties, body):
        print(" [x]2 %r" % body)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.basic_consume(queue=queue_name, on_message_callback=callback1, auto_ack=True)
    channel.basic_consume(queue=queue_name, on_message_callback=callback2, auto_ack=True)

    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
