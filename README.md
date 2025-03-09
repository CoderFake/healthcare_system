# Hệ Thống Quản Lý Dịch Vụ Chăm Sóc Sức Khỏe

Một hệ thống quản lý chăm sóc sức khỏe toàn diện dành cho phòng khám và cơ sở y tế quy mô nhỏ, được thiết kế để quản lý bác sĩ, bệnh nhân, lịch khám và hồ sơ bệnh án.

## Tính Năng

- **Quản Lý Bác Sĩ**: Thêm, cập nhật và quản lý thông tin bác sĩ, chuyên khoa và lịch trình
- **Quản Lý Bệnh Nhân**: Duy trì hồ sơ bệnh nhân bao gồm thông tin cá nhân và tiền sử bệnh
- **Đặt Lịch Khám**: Lên lịch và theo dõi lịch hẹn của bệnh nhân với hiển thị lịch biểu
- **Bảng Điều Khiển**: Tổng quan về các hoạt động hàng ngày và thống kê
- **Xác Thực Người Dùng**: Kiểm soát truy cập dựa trên vai trò (quản trị viên, bác sĩ, nhân viên)
- **Bảo Mật Dữ Liệu**: Mã hóa mật khẩu và lưu trữ dữ liệu an toàn

## Cài Đặt

1. Sao chép mã nguồn:
```bash
git clone https://github.com/coderfake/healthcare-system.git
cd healthcare-system
```

2. Tạo và kích hoạt môi trường ảo:
```bash
python -m venv venv
source venv/bin/activate   # Trên Windows: venv\Scripts\activate
```

3. Cài đặt các gói phụ thuộc:
```bash
pip install -r requirements.txt
```

4. Thiết lập biến môi trường:
```bash
cp .env.example .env
```
Chỉnh sửa tệp `.env` với các cấu hình ưa thích của bạn.

5. Chạy ứng dụng:
```bash
python main.py
```

## Yêu Cầu Hệ Thống

- Python 3.8 trở lên
- Tkinter (thường đi kèm với Python)
- SQLite (được tích hợp trong Python)

## Di Chuyển Cơ Sở Dữ Liệu (Migration)

Hệ thống bao gồm chức năng migration để quản lý thay đổi cấu trúc cơ sở dữ liệu:

1. Tạo migration mới:
```bash
python -m scripts.create_migration them_tinh_nang_moi
```

2. Chỉnh sửa tệp migration được tạo trong thư mục `database/migrations/`

3. Các migration sẽ tự động được áp dụng khi ứng dụng khởi động

## Cấu Hình

Cấu hình được quản lý thông qua các biến môi trường trong tệp `.env`:

- `DB_FILE`: Đường dẫn tệp cơ sở dữ liệu
- `ADMIN_USERNAME`: Tên đăng nhập quản trị viên mặc định
- `ADMIN_PASSWORD`: Mật khẩu quản trị viên mặc định
- `APP_THEME`: Giao diện ứng dụng
- `ENABLE_LOGGING`: Bật/tắt ghi log
- `LOG_LEVEL`: Mức độ chi tiết của log

## Cấu Trúc Dự Án

```
healthcare_system/
│
├── main.py                    # Điểm vào chính
│
├── config/                    # Cấu hình
│   ├── __init__.py
│   └── settings.py            # Cài đặt ứng dụng
│
├── database/                  # Quản lý cơ sở dữ liệu
│   ├── __init__.py
│   ├── db_manager.py          # Kết nối và các thao tác cơ bản
│   ├── models.py              # Mô hình dữ liệu
│   ├── db_setup.py            # Khởi tạo cơ sở dữ liệu
│   └── migrations/            # Thư mục chứa các migration
│
├── controllers/               # Xử lý logic nghiệp vụ
│   ├── __init__.py
│   ├── auth_controller.py     # Xác thực
│   ├── doctor_controller.py   # Quản lý bác sĩ
│   ├── patient_controller.py  # Quản lý bệnh nhân
│   └── schedule_controller.py # Quản lý lịch khám
│
├── views/                     # Giao diện người dùng
│   ├── __init__.py
│   ├── app.py                 # Cửa sổ ứng dụng chính
│   ├── auth_view.py           # Màn hình đăng nhập
│   ├── base_view.py           # Lớp view cơ sở
│   ├── doctor_view.py         # Quản lý bác sĩ
│   ├── patient_view.py        # Quản lý bệnh nhân
│   ├── schedule_view.py       # Quản lý lịch khám
│   └── components/            # Các thành phần UI có thể tái sử dụng
│
├── utils/                     # Tiện ích
│   ├── __init__.py
│   ├── validators.py          # Kiểm tra dữ liệu
│   └── helpers.py             # Hàm trợ giúp
│
├── assets/                    # Tài nguyên
│   ├── icons/                 # Biểu tượng
│   └── images/                # Hình ảnh
│
├── requirements.txt           # Danh sách các gói phụ thuộc
├── .env.example               # Mẫu cấu hình biến môi trường
└── README.md                  # Tài liệu
```

## Tài Khoản Mặc Định

Sau khi cài đặt, bạn có thể đăng nhập bằng tài khoản quản trị viên mặc định:

- **Tên đăng nhập**: admin
- **Mật khẩu**: 123456

Lưu ý: Hãy thay đổi mật khẩu mặc định sau khi đăng nhập lần đầu tiên để đảm bảo an toàn.

## Hướng Dẫn Sử Dụng

### Quản Lý Bác Sĩ
- Thêm bác sĩ mới với thông tin cá nhân và chuyên khoa
- Cập nhật thông tin bác sĩ
- Xem danh sách tất cả bác sĩ và tìm kiếm

### Quản Lý Bệnh Nhân
- Đăng ký bệnh nhân mới với thông tin cá nhân
- Cập nhật hồ sơ bệnh nhân
- Tìm kiếm bệnh nhân

### Quản Lý Lịch Khám
- Đặt lịch khám cho bệnh nhân với bác sĩ cụ thể
- Xem lịch khám theo ngày, bác sĩ hoặc bệnh nhân
- Chỉnh sửa hoặc hủy các cuộc hẹn

### Bảng Điều Khiển
- Xem tổng quan về các cuộc hẹn trong ngày
- Thống kê về bác sĩ và bệnh nhân
- Truy cập nhanh các chức năng chính

## Đóng Góp

1. Fork dự án
2. Tạo nhánh tính năng (`git checkout -b feature/NewFeature`)
3. Commit thay đổi của bạn (`git commit -m 'Add some NewFeature'`)
4. Push lên nhánh (`git push origin feature/NewFeature`)
5. Mở Pull Request


## Liên Hệ

HoangDieuIT - hoangdieu22022002@gmail.com

Link dự án: [https://github.com/coderfake/healthcare-system](https://github.com/coderfake/healthcare-system)
