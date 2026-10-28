# 🧠 AI Text Summarizer — Final Project

**Đề tài:** Xây dựng ứng dụng tóm tắt văn bản bằng Generative AI  
**Tên tiếng Anh:** AI-powered Text Summarization Web Application  
**Công nghệ:** Python · Streamlit · Gemini API  
**Ngôn ngữ giao diện:** Tiếng Việt

Đây là sản phẩm demo có thể chạy trên máy tính cá nhân. Ứng dụng nhận văn bản, cho phép tùy chọn độ dài và định dạng, trả lại bản tóm tắt, hiển thị thống kê và tải kết quả `.txt`.

## 1. Chức năng đã triển khai

| Tính năng | Tình trạng |
| --- | --- |
| Giao diện web bằng Streamlit | ✅ Có |
| Nhập trực tiếp hoặc tải TXT/MD UTF-8, Word DOCX, PDF có văn bản | ✅ Có |
| Tóm tắt bằng Gemini API | ✅ Có mã tích hợp; **cần API key** |
| Chọn bản tóm tắt Ngắn / Vừa / Chi tiết | ✅ Có |
| Chọn đoạn văn / gạch đầu dòng | ✅ Có |
| Chọn ngôn ngữ đầu ra cho Gemini | ✅ Có |
| Demo ngoại tuyến không cần API key | ✅ Có, **tóm tắt trích xuất, không phải AI tạo sinh** |
| Tải kết quả `.txt` | ✅ Có |
| Thống kê số từ, tỷ lệ rút gọn, thời gian | ✅ Có |
| Unit tests và script đánh giá | ✅ Có |

## 2. Chạy project trên Windows (dễ nhất)

**Yêu cầu:** Windows 10/11, Python 3.10 trở lên, Internet để cài thư viện; Internet + API key khi dùng Gemini.

1. Clone repository GitHub hoặc tải ZIP và mở thư mục chứa `app.py`.
2. Mở file `start_windows.bat`. Chương trình tự tạo môi trường Python, cài thư viện và khởi động ứng dụng.
3. Trình duyệt mở trang `http://localhost:8501` (nếu chưa mở, sao chép địa chỉ do cửa sổ lệnh hiển thị).
4. Chọn **Demo ngoại tuyến (trích xuất)**, nhấn **Điền văn bản mẫu** rồi **Tóm tắt văn bản** để thử trước.

### Chạy thủ công (PowerShell)

```powershell
cd AI_Text_Summarizer_Project
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Để dừng ứng dụng: `Ctrl + C` trong cửa sổ terminal.

### macOS / Linux

```bash
cd AI_Text_Summarizer_Project
bash start_mac_linux.sh
```

### Tải file Word và PDF

- Chọn **Tải file Word (.docx), PDF, TXT, MD** trên giao diện. Ứng dụng tự lấy nội dung từ đoạn văn/bảng Word và các trang PDF có lớp chữ rồi đưa vào ô văn bản để xem lại trước khi tóm tắt.
- File tối đa **50 MB**; tài liệu PDF tối đa **300 trang**. Văn bản dài hơn **200.000 ký tự** sẽ chỉ dùng phần đầu và **hiện cảnh báo**; nên chia nhỏ tài liệu nếu cần toàn bộ.
- PDF scan chỉ có ảnh, PDF khóa mật khẩu, và file Word `.doc` cũ không được hỗ trợ. Hãy chuyển thành PDF có text/OCR hoặc DOCX trước khi tải.
- Các file được đọc trong bộ nhớ, không lưu vào thư mục dự án. Khi chọn Gemini, nội dung văn bản sẽ được gửi tới nhà cung cấp mô hình; tránh tải tài liệu riêng tư.

## 3. Kết nối Generative AI thật (Gemini)

1. Mở trang **Google AI Studio**: https://aistudio.google.com/apikey
2. Tạo API key bằng tài khoản và dự án của bạn; giới hạn, điều kiện và chi phí dịch vụ tùy tài khoản/khu vực.
3. Trong ứng dụng, chọn **Gemini AI (tạo sinh)** và nhập key ở thanh bên trái (ô mật khẩu); **hoặc** sao chép `.env.example` thành `.env` rồi thêm:

```ini
GEMINI_API_KEY=YOUR_OWN_API_KEY
```

4. Nhập văn bản và nhấn **Tóm tắt văn bản**.

**Bảo mật:** Không đưa key vào GitHub, ảnh chụp màn hình hay báo cáo. Không nhập tài liệu bí mật vì văn bản sẽ được gửi tới dịch vụ Gemini khi chọn chế độ AI.

**Lưu ý:** Mã sử dụng `google-genai` và model mặc định `gemini-3.8-flash`. Ứng dụng cho phép chọn `gemini-3.8-flash` (mặc định), `gemini-3.6-flash` hoặc `gemini-3.5-flash-lite` trong thanh bên. Quyền truy cập và hạn mức phụ thuộc tài khoản/API key.

## 4. Minh họa luồng xử lý

```text
Người dùng nhập văn bản hoặc tải TXT
                ↓
        Giao diện Streamlit
                ↓
      Kiểm tra dữ liệu đầu vào
                ↓
       Chọn phương pháp xử lý
         ↙                ↘
    Gemini API         Demo ngoại tuyến
 (LLM tạo sinh)     (chọn câu có điểm cao)
         ↘                ↙
       Văn bản tóm tắt đầu ra
                ↓
   Hiển thị / thống kê / tải TXT
```

### Phân biệt rõ hai chế độ

- **Gemini AI** dùng mô hình ngôn ngữ lớn để **sinh ra** văn bản tóm tắt mới. Đây là chức năng chính của đề tài Generative AI.
- **Demo ngoại tuyến** dùng thống kê tần suất từ khóa để **chọn câu** đã xuất hiện trong văn bản. Đây là phương pháp trích xuất đơn giản dùng để kiểm tra giao diện khi chưa có API key; không nên trình bày như kết quả của mô hình Generative AI.

## 5. Kiểm thử

Unit test (không cần Internet hoặc API key, chỉ cần Python):

```bash
python -m unittest discover -s tests -v
```

Đánh giá mẫu (sau khi cài thư viện):

```bash
python evaluate.py --mode demo
python evaluate.py --mode gemini
```

Script xuất `results/evaluation.csv` với số từ, mức rút gọn, thời gian và ba cột đánh giá cần **chấm thủ công**. Chưa có điểm đánh giá chất lượng nào được giả định. Bạn cần đọc bản gốc và tự chấm **độ chính xác / độ bao quát / độ mạch lạc (1–5)**.

**Giới hạn hiện tại:** Nhận TXT, MD, DOCX và PDF có lớp văn bản; chưa đọc PDF scan chỉ gồm ảnh (chưa có OCR), không hỗ trợ .doc đời cũ. Mỗi file tối đa 50 MB, tối đa 300 trang PDF, tóm tắt 200.000 ký tự đầu và có cảnh báo nếu cắt bớt. Không có cơ sở dữ liệu; tài liệu dài được chia đoạn cho Gemini nhưng chỉ trong phạm vi 200.000 ký tự đầu và có thể tăng chi phí/hạn mức API. Chất lượng Gemini phụ thuộc API, văn bản và prompt. Mức rút gọn phần trăm không đại diện cho độ chính xác.

## 6. Cấu trúc mã nguồn

```text
AI_Text_Summarizer_Project/
├── app.py                 # Giao diện Streamlit
├── summarizer.py          # Prompt, Gemini API, demo trích xuất
├── document_reader.py     # Trích xuất TXT/MD/DOCX/PDF
├── evaluate.py            # Xuất bảng đánh giá
├── requirements.txt       # Các thư viện Python
├── .env.example           # Mẫu cấu hình API key
├── .gitignore             # Chặn upload file bí mật
├── start_windows.bat      # Chạy nhanh Windows
├── start_mac_linux.sh     # Chạy nhanh macOS/Linux
├── examples/
│   ├── van_ban_mau.txt
│   └── english_sample.txt
├── tests/
│   └── test_summarizer.py
├── tests/test_document_reader.py # Unit tests đọc Word/PDF
└── docs/
    ├── BAO_CAO_PROJECT.md
    └── KICH_BAN_DEMO.md
```

## 7. Nộp và thuyết trình

- **Nộp mã nguồn:** ZIP này hoặc đưa thư mục lên repository GitHub cá nhân (không đẩy `.env`).
- **Nộp báo cáo:** Từ `docs/BAO_CAO_PROJECT.md` chuyển thành Word/Google Docs và bổ sung ảnh chụp demo, số liệu đánh giá thực tế.
- **Demo nhanh:** Mở ứng dụng, chọn Gemini, dán văn bản mẫu, thử 3 mức độ dài rồi tải TXT. Nếu chưa có key, demo chỉ được trình bày là chế độ trích xuất.

## 8. Nguồn tham khảo

- [Google Gen AI SDK (Python)](https://googleapis.github.io/python-genai/)
- [Google Gemini API](https://ai.google.dev/gemini-api/docs)
- [Streamlit documentation](https://docs.streamlit.io/)
- [Hugging Face Transformers](https://github.com/huggingface/transformers)
- [A Survey of Large Language Models](https://arxiv.org/abs/2303.18223)

## Tài liệu dài (phiên bản 2)

- Với văn bản dài, Gemini chia nội dung thành các phần tối đa 16.000 ký tự, tóm tắt lần lượt rồi tổng hợp thành kết quả chung. Việc này sử dụng nhiều lượt gọi API, có thể chậm và tiêu thụ hạn mức Gemini.
- File đến **50 MB** được chấp nhận; PDF tối đa **300 trang**, nhưng chỉ trích xuất **200.000 ký tự đầu** trong mỗi lần xử lý. Nếu vượt giới hạn, ứng dụng **cảnh báo đã cắt bớt**. Để bao phủ toàn bộ tài liệu, hãy chia file trước khi tải.
- Cấu hình giới hạn tải lên ở `.streamlit/config.toml` bằng `server.maxUploadSize = 50` và kiểm tra riêng trong `document_reader.py`.
