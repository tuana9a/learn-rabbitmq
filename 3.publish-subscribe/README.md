# note

<img style="background-color:white" src="https://www.rabbitmq.com/img/tutorials/exchanges.png" />

message khi publish sẽ được đẩy vào exchange chứ không phải trực tiếp vào queue

cụ thể hơn: publiser chỉ quan tâm tới exchange
        
khi nó đẩy lên mà `k có consumer` thì message `bay màu`
    
consumer sẽ bind queue của nó với exchange        
- kiểu "ê exchange nếu có update gì thì báo tao với nhé"
- khá là hợp lí cho cuộc tình tay ba, một exchange í

QUESTION:

khi add nhiều callback, thì các callback sẽ được chọn theo round robin
- cơ mà cái này chưa thấy thực tế lắm làm rỗi vl :))
