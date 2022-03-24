import re
import sys
import pika
import os
import dotenv

dotenv.load_dotenv()  # take environment variables from .env.
host = os.getenv("HOST")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=host))
channel = connection.channel()

channel.queue_declare(queue='hello')

messages = ' '.join(sys.argv[1:]) or "Hello World!"
for message in re.compile('\\s+').split(messages):
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=message)
    print(" [x] Sent %r" % message)
connection.close()
