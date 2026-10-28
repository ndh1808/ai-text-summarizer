# BÁO CÁO FINAL PROJECT — ỨNG DỤNG TÓM TẮT VĂN BẢN BẰNG GENERATIVE AI

**Sinh viên:** [Điền họ tên]  
**Môn học:** Trí tuệ nhân tạo và ứng dụng  
**Đề tài:** AI-powered Text Summarization Web Application

## 1. Lý do chọn đề tài

Khối lượng tài liệu học tập và nghiên cứu lớn dẫn đến nhu cầu đọc nhanh và chọn lọc thông tin. Generative AI, đặc biệt là các mô hình ngôn ngữ lớn (LLM), có thể tạo bản tóm tắt theo yêu cầu người dùng. Đề tài này tập trung vào xây dựng sản phẩm thực tế bằng cách tích hợp mô hình sẵn có thay vì tự huấn luyện mô hình.

## 2. Mục tiêu

Xây dựng ứng dụng web cho phép: (1) nhập văn bản tiếng Việt/Anh; (2) lựa chọn độ dài bản tóm tắt; (3) lựa chọn hình thức trình bày; (4) tóm tắt thông qua Gemini API; (5) xuất kết quả TXT; (6) thống kê một số chỉ số vận hành.

## 3. Cơ sở công nghệ

- **Generative AI:** Sinh văn bản mới dựa trên ngữ cảnh và yêu cầu của người dùng.
- **LLM:** Mô hình ngôn ngữ lớn cho các tác vụ xử lý văn bản.
- **Prompt engineering:** Hướng dẫn mô hình chỉ giữ ý chính, không thêm thông tin mới và tuân thủ độ dài.
- **Streamlit:** Framework Python để tạo giao diện ứng dụng web.
- **Gemini API:** Cổng truy cập mô hình LLM dùng trong chức năng tóm tắt.

## 4. Phân tích và thiết kế hệ thống

**Đầu vào:** Văn bản TXT/MD hoặc văn bản nhập thủ công; độ dài Ngắn/Vừa/Chi tiết; kiểu đoạn văn/gạch đầu dòng; ngôn ngữ.  
**Xử lý:** Kiểm tra đầu vào → tạo prompt → gửi API → nhận phản hồi → hiển thị và lưu kết quả.  
**Đầu ra:** Bản tóm tắt, số từ, tỷ lệ rút gọn, thời gian xử lý, tệp `.txt`.

Các khối chức năng được tách thành `app.py` (giao diện) và `summarizer.py` (thuật toán và gọi API) để dễ bảo trì.

## 5. Triển khai

Môi trường Python 3.10+, các thư viện `streamlit`, `google-genai`, `python-dotenv`. Sử dụng SDK `google.genai` để gọi `client.models.generate_content`. Cấu hình API key bằng biến môi trường hoặc nhập trực tiếp trên giao diện. Chế độ demo không sử dụng LLM mà chọn câu tiêu biểu theo tần suất từ, chỉ phục vụ chạy thử không kết nối mạng.

## 6. Kiểm thử và đánh giá

**Kiểm thử chức năng:** văn bản trống; văn bản quá ngắn; văn bản đủ dài; chọn 3 độ dài; chọn định dạng; tải TXT; lỗi API key.  
**Đánh giá chất lượng dự kiến:** Chọn tối thiểu 15–20 văn bản, chấm 3 tiêu chí (1–5): (1) độ chính xác so với nguồn; (2) độ bao quát ý chính; (3) độ mạch lạc. Ghi số từ và thời gian xử lý. Có thể so sánh ba mức độ dài và ảnh hưởng của prompt.

**Kết quả thực nghiệm:** [Điền sau khi chạy Gemini thật và chấm thủ công. Không báo cáo số liệu chưa thu thập.]

**Ảnh minh họa giao diện:** [Chèn ảnh sau khi mở Streamlit và chụp màn hình.]

## 7. Hạn chế và hướng phát triển

Phiên bản hiện tại phụ thuộc Gemini API ở chế độ tạo sinh; xử lý tối đa 25.000 ký tự; không hỗ trợ PDF và tóm tắt nhiều tài liệu. Hướng phát triển: đọc PDF, chia đoạn văn bản dài, so sánh nhiều LLM, đánh giá bằng bộ dữ liệu chuẩn, phát triển tính năng truy hồi tài liệu (RAG).

## 8. Kết luận

Đề tài minh họa quy trình tích hợp LLM vào một ứng dụng web và cung cấp cơ sở để đánh giá kết quả AI. Việc tách giao diện và xử lý cho phép nâng cấp dễ dàng. Kết quả tóm tắt cần được người dùng đối chiếu với văn bản gốc trước khi sử dụng vào học tập, nghiên cứu.

## Tài liệu tham khảo

1. https://arxiv.org/abs/2303.18223
2. https://ai.google.dev/gemini-api/docs
3. https://googleapis.github.io/python-genai/
4. https://docs.streamlit.io/
5. https://github.com/huggingface/transformers
