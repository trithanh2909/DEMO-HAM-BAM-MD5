# Bài tập nhóm: Tự cài đặt thuật toán băm MD5 bằng Python



## 1\. Mục tiêu

Dự án được tổ chức thành hai tệp để thuận tiện cho việc nộp bài và trình diễn:

* `main.py`: chứa phần lõi MD5 tự cài đặt theo RFC 1321, chức năng băm văn bản/tệp, kiểm tra tính toàn vẹn, trace trạng thái và các bài tự kiểm thử cơ bản.
* `README.md`: hướng dẫn cài đặt, chạy chương trình và giải thích các giới hạn.

Phần lõi `md5()` tự thực hiện padding, chia khối 512 bit, xử lý 64 bước, cập nhật trạng thái 32 bit và xuất digest 128 bit. Hàm `hashlib.md5()` chỉ được gọi trong chức năng tự kiểm thử để đối chiếu kết quả, không được dùng thay cho lõi MD5.

## 2\. Yêu cầu

* Python 3.10 trở lên.
* Không cần cài thư viện bên ngoài; chỉ dùng thư viện chuẩn Python.
* Chạy bằng Command Prompt, PowerShell hoặc Terminal.

Kiểm tra Python:

```bash
python --version
```

Trên Windows, nếu lệnh `python` không hoạt động nhưng `py` có sẵn, có thể thay `python` bằng `py` trong các lệnh bên dưới.

## 3\. Chạy chương trình

Mở terminal tại thư mục chứa `main.py` và `README.md`, sau đó chạy:

```
python main.py
```

Menu cung cấp các lựa chọn:

1. Tính MD5 cho văn bản.
2. Tính MD5 cho một tệp.
3. Kiểm tra tính toàn vẹn của tệp bằng digest tham chiếu.
4. Hiển thị trace 8 bước đầu của MD5 với thông điệp `abc`.
5. Chạy bộ tự kiểm thử.
6. Thoát.

## 4\. Chạy tự kiểm thử

Trong menu, chọn `5`. Hoặc chạy chương trình không tương tác bằng lệnh:

```
python main.py
```

Sau đó nhập `5` và kiểm tra kết quả ở cuối. Bộ tự kiểm thử hiện bao gồm:

* 7 test vector MD5 chuẩn theo RFC 1321.
* Kiểm thử các độ dài quanh ranh giới padding và khối dữ liệu.
* Kiểm thử văn bản tiếng Việt mã hóa UTF-8.
* Kiểm tra đầu vào không phải bytes.
* Kiểm tra trace có đủ 64 bước.
* Kiểm tra tệp nguyên bản khớp digest tham chiếu.
* Kiểm tra tệp đã thay đổi không khớp digest cũ.
* Kiểm tra digest tham chiếu sai định dạng.

Chỉ xem chương trình đạt khi tất cả các dòng kiểm tra hiện `\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\[PASS]` và kết quả cuối ghi `OK`.

