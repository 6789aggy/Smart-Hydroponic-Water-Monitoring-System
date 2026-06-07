<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>
<h2 align="center">
   HỆ THỐNG GIÁM SÁT THỦY CANH THÔNG MINH 
</h2>
<div align="center">
    <p align="center">
        <img src="docs/aiotlab_logo.png" alt="AIoTLab Logo" width="170"/>
        <img src="docs/fitdnu_logo.png" alt="AIoTLab Logo" width="180"/>
        <img src="docs/dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>

<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>

<h2 align="center">
   GIÁM SÁT CHẤT LƯỢNG NƯỚC TRONG HỆ THỐNG THỦY CANH
</h2>

<div align="center">

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)

[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)

[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>

---
<p align="center">
  <img src="docs/PTs.jpg" alt="Poster đề tài" width="700"/>
</p>
<p align="center"><em>POSTER</em></p>

---

# 📖 1. Giới thiệu

Dự án được xây dựng nhằm giám sát các thông số quan trọng của nước trong hệ thống thủy canh theo thời gian thực. Dữ liệu từ các cảm biến được thu thập bởi Arduino UNO, truyền qua ESP8266 bằng WiFi đến Flask Server và hiển thị trên Dashboard Web.

Hệ thống hỗ trợ:

Giám sát độ pH
Giám sát độ đục nước
Giám sát mực nước
Giám sát lưu lượng nước
Điều khiển bơm thủ công
Điều khiển bơm tự động
Hiển thị biểu đồ thời gian thực
Lưu lịch sử hoạt động bằng SQLite

---

# 🛠️ 2. Công nghệ sử dụng

## IoT

* Arduino UNO
* ESP8266 NodeMCU
* pH Sensor
* Turbidity Sensor
* Water Level Sensor
* Water Flow Sensor
* Relay Module 5V
* Water Pump

## Software

* Python
* Flask
* SQLite
* HTML5

---

# 🚀 3. Kiến trúc hệ thống

```text
Cảm biến pH
Cảm biến độ đục
Cảm biến mực nước
Cảm biến lưu lượng
          │
          ▼
      Arduino UNO
          │ UART
          ▼
        ESP8266
          │ WiFi
          ▼
      Flask Server
      /         \
Dashboard      SQLite
    
```

---

# 🖼️ 4. Hình ảnh hệ thống

## Dashboard

<p align="center">
  <img src="docs/home.png" alt="Dashboard" width="700"/>
</p>

<p align="center">
  <em>Hình 2: Giao diện Dashboard IoT Pro</em>
</p>

Dashboard hiển thị các thông số môi trường theo thời gian thực bao gồm độ pH, độ đục, mực nước và lưu lượng nước. Người dùng có thể theo dõi trạng thái hoạt động của hệ thống và điều khiển bơm trực tiếp trên giao diện Web.

Hiển thị:

* pH
* Độ đục
* Mực nước
* Lưu lượng
* Trạng thái bơm
* Chế độ hoạt động

---

## Biểu đồ thời gian thực

<p align="center">
  <img src="docs/NK.png" alt="Realtime Chart" width="700"/>
</p>

<p align="center">
  <em>Hình 3: Biểu đồ dữ liệu cảm biến thời gian thực</em>
</p>

Biểu đồ cho phép theo dõi sự thay đổi của các thông số môi trường theo thời gian thực, hỗ trợ người dùng đánh giá tình trạng chất lượng nước trong hệ thống thủy canh.

Theo dõi dữ liệu cảm biến theo thời gian thực.

---

## Nhật ký phiên tưới

<p align="center">
  <img src="docs/PT.png" alt="Pump Log" width="700"/>
</p>

<p align="center">
  <em>Hình 4: Nhật ký các phiên tưới</em>
</p>

Mỗi phiên tưới được lưu lại bao gồm ngày vận hành, thời gian bắt đầu, thời gian kết thúc, thời lượng hoạt động của bơm và các thông số môi trường tại thời điểm ghi nhận.

Lưu:

* Ngày vận hành
* Thời gian bắt đầu
* Thời gian kết thúc
* Thời lượng bơm
* Giá trị cảm biến

---

# ⚙️ 5. Cài đặt hệ thống

## Bước 1: Clone Repository

```bash
git clone https://github.com/6789aggy/Smart-Hydroponic-Water-Monitoring-System.git
cd "vào thư mục vừa clone về"
```

---

## Bước 2: Cài đặt thư viện

```bash
pip install flask
pip install requests
pip install pyserial
pip install web3
```

---

## Bước 3: Chạy Flask Server

```bash
python blockchain.py
```

Server chạy tại:

```text
http://127.0.0.1:5000
```

---

## Bước 4: Nạp chương trình ESP8266

* Mở Arduino IDE.
* Chọn board ESP8266.
* Cập nhật địa chỉ IP Flask Server.
* Upload chương trình.

---

# 📊 6. Kết quả đạt được

| Chức năng                | Kết quả |
| ------------------------ | ------- |
| Giám sát pH              | Đạt     |
| Giám sát độ đục          | Đạt     |
| Giám sát mực nước        | Đạt     |
| Giám sát lưu lượng       | Đạt     |
| Điều khiển bơm           | Đạt     |
| Dashboard thời gian thực | Đạt     |
| SQLite                   | Đạt     |
| Lưu nhật ký phiên tưới   | Đạt     |

---

# 🔮 7. Hướng phát triển

* Tích hợp AI dự đoán chất lượng nước.
* Gửi cảnh báo qua điện thoại.
* Lưu trữ dữ liệu trên Cloud.
* Hỗ trợ nhiều mô hình thủy canh.
* Tự động tối ưu thời gian tưới.

---

# 📬 8. Liên hệ

* Họ và tên: Lò Đức Mạnh
* Khoa: Công nghệ Thông tin
* Trường: Đại học Đại Nam

---

© 2026 AIoTLab, Faculty of Information Technology, DaiNam University.

