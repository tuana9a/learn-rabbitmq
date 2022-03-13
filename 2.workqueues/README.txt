workqueues:
    cơ chế:
        hoạt động round robin
        lẻ chẵn lẻ chẵn, non blocking other consumer

    đặc biệt:
        auto_ack=True: kill consumer sẽ mất toàn bộ mess cho consumer đó
        consumer chủ động send ack thì nếu bị lỗi có thể resend lại được
        các message khi đang được xử lí sẽ có trạng thái messages_unacknowledged trên queue
            khi bị lỗi tự động đc add lại vào queue và số lượng messages_unacknowledged=0
                chứ không phải là số lượng message bị lỗi
        

    durability:
        có thể make queue được lưu lại khi reset
        có thể make message được lưu vào disk (weak guarantee)

    prefetch:
        không đẩy quá n message cho một worker mà đẩy cho các thằng rảnh khác
        kill consumer mà trước khi ack => sẽ giữ message và đẩy message cho một consumer khác

    
