import time
import pika
import sys
import os
import dotenv

dotenv.load_dotenv()

host = os.getenv("HOST")

# explain more details if there are more than 1 consumer
# with current code then rabbitmq will truly use round-robin algorithm
# to distribute messages to consumers one by one
# and if consumer is slow then it will be the next consumer
# example:
# if the tasks in queue are: 10s 1s 10s 1s ...
# worker 1 will take "10s task"
# worker 2 will tkae "1s task" and then it will take next 1s
# worker 2 SKIP "10s task" for worker 1 without waiting worker 1 to complete
# if then worker 1 compelete first "10s task" then it take next "10s task"
# and so on

# nếu chỉ có một worker tại thời điểm message tới và nếu bật auto_ack
# thì toàn bộ message sẽ được giao cho worker đó
# do vậy nếu bị kill thì mất toàn bộ message
# do bật auto_ack=True nên rabbit sẽ liên tục assign message cho worker này
# còn nếu mannual ack thì message sẽ cần phải được ack thì ms xóa khỏi queue
# từ đó nếu bị crash thì message vẫn còn nguyên ở đó


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        time.sleep(body.count(b'.'))
        print(" [x] Done")

    # auto_ack=True: khi consumer nhận message thì sẽ ack luôn
    # do vậy khi kill consumer sẽ mất message mà nó đang xử lý
    channel.basic_consume(
        queue='hello',
        on_message_callback=callback,
        auto_ack=True
        # nếu không có auto_ack=True và cũng không ack manually thì
        # message không bao giờ bị xóa khỏi queue
        # và message đó rất có thể bị process lặp đi lặp lại trên nhiều queue
        # vậy phải luôn đảm bảo message được process
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
