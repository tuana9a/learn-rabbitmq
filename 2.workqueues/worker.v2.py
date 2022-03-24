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
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # so với v1, v0 cái này là tốt nhất, message không bị dồn vào một thằng
    # nếu như tại thời điểm có message chỉ có 1 worker hoạt động
    # thì nó cũng chỉ nhận tối đa prefetch_count=1 message tại một thời điểm
    # rabbitmq sẽ phân phối các message theo kiểu ai available thì gửi
    # từ đó nếu một worker đang xử lý nặng thì nếu theo round robin rất
    # có thể công việc nặng tiếp theo sẽ vào tay nó, nhưng với việc set
    # prefetch_count=1, thì công việc nặng có thể được phân phối cho worker
    # vừa làm xong việc nhẹ, từ đó gián tiếp cân bằng tải cho các worker
    channel.basic_qos(prefetch_count=1)
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
