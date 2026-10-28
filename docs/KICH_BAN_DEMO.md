# KỊCH BẢN DEMO (3–4 PHÚT)

**0:00 – 0:30 — Giới thiệu**  
"Em chọn hướng Generative AI và xây dựng ứng dụng tóm tắt văn bản bằng mô hình ngôn ngữ lớn. Ứng dụng dùng Python và Streamlit, kết nối Gemini API."

**0:30 – 1:00 — Kiến trúc**  
"Người dùng nhập văn bản, chọn độ dài, định dạng. Hệ thống xây dựng prompt, gửi Gemini rồi hiển thị bản tóm tắt. Em có thêm chế độ trích xuất ngoại tuyến để kiểm tra giao diện khi không có API key."

**1:00 – 2:30 — Thao tác**  
1. Mở ứng dụng.
2. Chọn Gemini AI, nhập API key (đã che).
3. Tải một file DOCX/PDF có lớp chữ (hoặc nhấn Điền văn bản mẫu).
4. Chọn Ngắn, nhấn Tóm tắt.
5. Đổi Vừa hoặc Chi tiết, chạy lại và chỉ ra sự khác biệt.
6. Tải kết quả TXT và giới thiệu các chỉ số.

**2:30 – 3:30 — Đánh giá & hạn chế**  
"Em dự kiến đánh giá theo tính chính xác, độ bao quát và độ mạch lạc; số từ và phần trăm rút gọn chỉ là các chỉ số bổ sung. Điểm hạn chế là phụ thuộc API, chỉ đọc PDF có lớp chữ và chưa hỗ trợ OCR file scan."

**Nếu không có API key:** Chuyển Demo ngoại tuyến, nói rõ đây là **tóm tắt trích xuất** và **không phải kết quả Generative AI**. Không gọi đây là demo Gemini.

## Câu hỏi có thể được thầy hỏi

**Có phải tự train AI không?** Không. Project tích hợp mô hình nền tảng qua API; giá trị nằm ở hệ thống, prompt và đánh giá.

**Generative AI khác Agentic AI thế nào?** Generative AI ở đây nhận đầu vào rồi sinh tóm tắt; Agentic AI còn có thể lập kế hoạch và dùng nhiều công cụ trong quy trình nhiều bước.

**Bản tóm tắt đúng hay sai bằng cách nào?** Đối chiếu văn bản gốc, chấm 3 tiêu chí theo thang 1–5; chưa thể đảm bảo 100%.

**Tại sao có chế độ Demo?** Để kiểm thử giao diện và cung cấp baseline trích xuất khi không có key hoặc không có mạng.
