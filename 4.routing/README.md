# note

- fanout exchange ignore routing_key value
  need to use direct exchange instead
- phân loại message (có hướng)
- nếu topic bay vào cái chưa có consume sẽ bay màu (mất hút)

# direct exchange

- binding: nhiều key nhiều consume
  <img style="background-color:white;" src="https://rabbitmq.com/img/tutorials/direct-exchange.png">
- multiple binding: nhiều consume một key
  <img style="background-color:white;" src="https://rabbitmq.com/img/tutorials/direct-exchange-multiple.png">
