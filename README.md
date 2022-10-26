### **Giới thiệu đề tài (Topic introduction)**

Xây dựng API về bán bàn ghế văn phòng để cung cấp cho ứng dụng [android](https://github.com/Beerus-Kun/selling_furnished_office_reactnative).

**Có những chức năng theo những quyền đăng nhập khác nhau:**
- Đăng nhập, đăng ký, quên mật khẩu, đổi thông tin.
- Thêm giỏ hàng, xem thông tin sản phẩm, mua hàng, thanh toán bằng thẻ tín dụng thông qua [stripe](https://stripe.com/).
- Bình luận realtime bằng WebSocket.
- Đánh giá, xem lịch sử, hủy đơn, thay đổi trạng thái đơn hàng.
- Quản lý sản phẩm, quản lý đơn hàng, quản lý danh mục sản phẩm, quản lý mã giảm giá.
- Quản lý nhân viên, xem báo cáo doanh thu, xem thống kê doanh thu.

**Những thư viện hỗ trợ:**
- fastapi: Chạy api bất đồng bộ.
- psycopg2: Kết nối với hệ quản trị cơ sở dữ liệu PostgreSQL.
- python-dotenv: Lưu biển môi trường.
- dropbox: Lưu hình ảnh lên dropbox.
- twilio: Gửi tin nhắn bằng sms.
- jwt: Xác thực token.
- bcrypt: Mã hóa mật khẩu.
- stripe: Thanh toán bằng thẻ tín dụng.


Build an API on selling office furniture to provide for the application [android](https://github.com/Beerus-Kun/selling_furnished_office_reactnative).

**There are functions according to different login permissions:**
- Login, register, forget password, change information.
- Add shopping cart, view product information, make purchases, pay by credit card through [stripe](https://stripe.com/).
- Realtime comments using WebSocket.
- Rate, view history, cancel orders, change order status.
- Product management, order management, product catalog management, discount code management.
- Manage employees, view revenue reports, view revenue statistics.

**Support Libraries:**
- fastapi: Run api asynchronously.
- psycopg2: Connect to the PostgreSQL database management system.
- python-dotenv: Save environment sea.
- dropbox: Save images to dropbox.
- twilio: Send messages by sms.
- jwt: Token authentication.
- bcrypt: Encrypt the password.
- stripe: Payment by credit card.


### **Cài đặt (Setting)**

Cài môi trường (Set up environment)
- python -m venv api-env
- api-env\Scripts\activate.bat
Cài đặt thư viện (Install libraries)
- pip install -r requirements.txt
Chạy các lệnh tạo bảng và function vào PostgreSQL (Run )
Chạy chương trình (Run program)
- uvicorn main:app --reload


### **Demo**

Giao diện chương trình sau khi chạy và vào web (Program interface after running and entering the web) http://127.0.0.1:8000/docs


- Authorize là nơi nhập token để có thể thực hiện những giao thức cần quyền truy cập (Authorize is the place to enter tokens to be able to make protocols that require access)

![Alt text](image/2022-10-27003642.png?raw=true)


- Có những phương thức: POST, GET, DELETE, PATCH,... Những giao thức có biểu tượng ổ khóa là những giao thức cần token (There are methods: POST, GET, DELETE, PATCH,... The protocols with the padlock symbol are the ones that need the token.)

![Alt text](image/2022-10-27004758.png?raw=true)


- Các biến cần trong mỗi giao thức (Variables needed in each protocol)

![Alt text](image/2022-10-27004921.png?raw=true)