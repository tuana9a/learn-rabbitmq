import re
import sys
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='192.168.1.4'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

messages = ' '.join(sys.argv[1:]) or "Hello World!"
for message in re.compile('\\s+').split(messages):
    # use exchange instead default exchange
    channel.basic_publish(exchange='logs',
                          routing_key='',
                          body=message)
    print(" [x] Sent %r" % message)
connection.close()
