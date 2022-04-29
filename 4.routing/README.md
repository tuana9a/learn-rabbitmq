# note

fanout exchange ignore routing_key value so need to use direct exchange instead

sử dụng exchange_type=`direct` để exchange có thể điều hướng theo `routing_key`

```python
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
```

nếu topic bay vào cái chưa có consume sẽ bay màu (mất hút)

# direct exchange

binding: nhiều key nhiều consume

<img style="background-color: white;" src="https://rabbitmq.com/img/tutorials/direct-exchange.png" />

multiple binding: nhiều consume một key

<img style="background-color: white;" src="https://rabbitmq.com/img/tutorials/direct-exchange-multiple.png" />
