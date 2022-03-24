import pika
import os
import dotenv

dotenv.load_dotenv()  # take environment variables from .env.

host = os.getenv("HOST")

connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
channel = connection.channel()

# create queue name hello
channel.queue_declare(queue='hello')

# use default exchange (will be explain later)
# queue name is routing key and also equals 'hello'
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
