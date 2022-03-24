import pika
import sys
import os
import dotenv

dotenv.load_dotenv()  # take environment variables from .env.


host = os.getenv("HOST")


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()

    # just for reduntdancy to make sure the queue is created
    # if two both declare queue then only one queue will be created
    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    # queue name is 'hello'
    # auto_ack is explain latter
    channel.basic_consume(
        queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
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
