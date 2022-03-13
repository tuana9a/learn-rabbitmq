import re
import sys
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='192.168.1.4'))
channel = connection.channel()

channel.queue_declare(queue='hello')

messages = ' '.join(sys.argv[1:]) or "Hello World!"
for message in re.compile('\\s+').split(messages):
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=message)
    print(" [x] Sent %r" % message)
connection.close()
