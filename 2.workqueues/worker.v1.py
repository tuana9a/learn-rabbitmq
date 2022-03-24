import time
import pika
import sys
import os
import dotenv

dotenv.load_dotenv()

host = os.getenv("HOST")


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        # manually call ack ensure that task is process completed
        # so while processing worker is crash then is will be processed by
        # other worker and message is not lost

        # so với worker.v0.py thì điểm giống là message vẫn bị dồn vào một thằng
        # nếu như tại thời điểm có message chỉ có 1 worker hoạt động
        # tuy nhiên nếu worker nhận hết message này die thì do việc ack thủ công
        # nên các message chưa được ack (do crash) có thể được re-queue cho worker
        # mới vào sau đó
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue='hello',
        on_message_callback=callback
    )

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
