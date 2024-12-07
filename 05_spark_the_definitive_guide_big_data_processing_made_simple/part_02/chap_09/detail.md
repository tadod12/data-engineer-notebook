## predicates

Trong Spark, phương thức jdbc của DataFrameReader cho phép bạn đọc dữ liệu từ cơ sở dữ liệu qua JDBC. Tham số predicates
trong phương thức jdbc có vai trò quan trọng trong việc tối ưu hóa truy vấn và phân phối công việc.

Cụ thể, predicates là một mảng các điều kiện phân mảnh (partitioning conditions) được áp dụng để chia nhỏ bảng cơ sở dữ
liệu thành các phân vùng độc lập, mà sau đó Spark có thể xử lý song song. Mỗi phần của bảng sẽ được truy vấn và xử lý
bởi một phân vùng trong Spark, giúp cải thiện hiệu suất và khả năng mở rộng của quy trình xử lý dữ liệu.

Trong đoạn mã của bạn:

    val predicates = Array(
    "DEST_COUNTRY_NAME = 'Sweden' OR ORIGIN_COUNTRY_NAME = 'Sweden'",
    "DEST_COUNTRY_NAME = 'Anguilla' OR ORIGIN_COUNTRY_NAME = 'Anguilla'")

predicates chứa hai điều kiện phân mảnh:

- Điều kiện phân mảnh 1: "DEST_COUNTRY_NAME = 'Sweden' OR ORIGIN_COUNTRY_NAME = 'Sweden'" - Chọn các hàng mà quốc gia
  đích hoặc quốc gia nguồn là 'Sweden'.
- Điều kiện phân mảnh 2: "DEST_COUNTRY_NAME = 'Anguilla' OR ORIGIN_COUNTRY_NAME = 'Anguilla'" - Chọn các hàng mà quốc
  gia đích hoặc quốc gia nguồn là 'Anguilla'.

Khi bạn gọi spark.read.jdbc(url, tablename, predicates, props), Spark sẽ gửi các truy vấn SQL tương ứng với từng điều
kiện phân mảnh đến cơ sở dữ liệu. Kết quả từ mỗi truy vấn sẽ được tải về và xử lý song song, giúp tăng tốc độ xử lý dữ
liệu.

Câu lệnh spark.read.jdbc(url, tablename, predicates, props).rdd.getNumPartitions trả về số phân vùng mà dữ liệu được
chia thành sau khi được tải về. Trong trường hợp này, kết quả là 2, nghĩa là dữ liệu được phân phối thành hai phần tương
ứng với hai điều kiện phân mảnh.