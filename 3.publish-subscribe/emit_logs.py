import re
import sys
import pika
import os
import dotenv

dotenv.load_dotenv()

host = os.getenv("HOST")

connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
channel = connection.channel()

# introduce một concept mới là exchange
# đại loại message sẽ không được push trực tiếp tới queue mà phải qua exchange
# lý do ? hỏi hay đấy
# nếu có một broker phía trước thì nó có thể đảm nhận việc điều hướng
# cụ thể hay ra sao thì xem các tutorial sau đó

channel.exchange_declare(exchange='logs', exchange_type='fanout')

messages = ' '.join(sys.argv[1:]) or "Hello World!"
for message in re.compile('\\s+').split(messages):
    # use exchange instead default exchange
    channel.basic_publish(exchange='logs',
                          routing_key='',
                          body=message)
    print(" [x] Sent %r" % message)
connection.close()
