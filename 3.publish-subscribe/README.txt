đúng mô hình publiser subscriber
    tạo ra một queue tạm sau đó sẽ xoá queue này
    cụ thể dùng exchange có tên thay vì exchange mặc định như trước

chi tiết
    publiser chỉ quan tâm tới exchange
        khi nó đẩy lên mà k có consumer thì message bay màu
    nếu có consumer nó sẽ bind queue của nó với exchange
        kiểu "ê exchange nếu có update gì thì báo tao với nhé"
        khá là hợp lí cho cuộc tình tay ba

QUESTION:
    khi add nhiều callback, thì nó lân lần lượt các callback (round robin)
