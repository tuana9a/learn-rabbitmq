# workqueues:

- cơ chế hoạt động:

  - round robin
  - lẻ chẵn lẻ chẵn, non blocking other consumer
  - tại 1 thời điểm khi message tới, nếu chỉ có 1 worker

- đặc biệt:

  - auto_ack=True: kill consumer sẽ mất toàn bộ mess cho consumer đó
  - consumer chủ động send ack thì nếu bị lỗi có thể resend lại được
    - các message khi đang được xử lí sẽ có trạng thái messages_unacknowledged trên queue
    - message đang trạng thái unacknowledged khi bị lỗi tự động đc add lại vào queue và có thể được xử lý bởi worker mà trước đó đã skip do round robin
  - nếu worker không ack trong 30p (có thể config = [Delivery Acknowledgement Timeout](https://www.rabbitmq.com/consumers.html#acknowledgement-timeout)) thì sẽ coi như hỏng và được "re queue"

# durability:

- mặc định các queue và message sẽ bị mất khi reset rabbitmq tuy nhiên:
  - có thể khiến queue có thể được lưu vào disk như sau
    ```python
    # chú ý nếu queue được declare trước đó không bật durable thì
    # rabbitmq không cho re declare lại queue, do vậy phải xóa queue, hoặc tạo queue mới
    # declare này PHẢI được apply ở cả producer và consumer
    channel.queue_declare(queue='hello', durable=True)
    ```
  - có thể make message được lưu vào disk (weak guarantee)
    ```python
    # chỉ cần thêm thuộc tính (properties) cho message là có thể khiến message được lưu vào disk
    # tuy nhiên không đảm bảo việc message không bị mất, vì rabbitmq sẽ cached lại trên bộ đệm
    # sau đó mới đẩy xuống disk, do vậy vẫn có tỉ lệ mất message
    # để đảm bảo hơn tham khảo link sau https://www.rabbitmq.com/confirms.html
    channel.basic_publish(exchange='',
                          routing_key="task_queue",
                          body=message,
                          properties=pika.BasicProperties(
                            delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
                          )
                        )
    ```

# prefetch:

- không đẩy quá n message cho một worker mà đẩy cho các thằng rảnh khác
- kill consumer mà trước khi ack => sẽ giữ message và đẩy message cho một consumer khác
