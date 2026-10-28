"""Vietnamese Streamlit UI for the Generative AI Text Summarizer project."""
from __future__ import annotations

import hashlib
import os
import time
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from document_reader import DocumentError, extract_document, MAX_UPLOAD_BYTES, MAX_TEXT_CHARS, MAX_PDF_PAGES
from summarizer import gemini_summarize, offline_summarize, word_count, split_text_chunks

load_dotenv()
ROOT = Path(__file__).resolve().parent
EXAMPLE = (ROOT / "examples" / "van_ban_mau.txt").read_text(encoding="utf-8")

st.set_page_config(
    page_title="AI Text Summarizer | Final Project",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.block-container {max-width: 1160px; padding-top: 2rem;}
.hero {background:linear-gradient(115deg,#0f172a,#1d4ed8);color:white;padding:25px 30px;
 border-radius:19px;margin-bottom:1.3rem;}
.hero h1 {font-size:2.0rem;margin:0 0 5px 0;color:white;}
.hero p {margin:0;color:#dbeafe;}
.small-note {font-size:0.87rem;color:#667085;}
</style>
""", unsafe_allow_html=True)

st.markdown('''<div class="hero"><h1>🧠 AI Text Summarizer</h1>
<p>Ứng dụng tóm tắt văn bản bằng Generative AI · Final Project · Python + Streamlit + Gemini</p></div>''',
unsafe_allow_html=True)

with st.sidebar:
    st.subheader("⚙️ Cấu hình")
    mode = st.radio("Chế độ xử lý", ["Gemini AI (tạo sinh)", "Demo ngoại tuyến (trích xuất)"],
                    help="Chế độ Demo chỉ chọn câu từ bài gốc, không tạo nội dung mới.")
    model = "gemini-2.5-flash"
    api_key = ""
    if mode.startswith("Gemini"):
        st.caption(f"Mô hình: `{model}`")
        api_key = st.text_input("Gemini API key", type="password", value="",
                                placeholder="Dán API key vào đây (nếu chưa đặt .env)")
        api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            st.warning("Chưa có API key. Bạn vẫn có thể chuyển sang Demo ngoại tuyến.")
        st.markdown("[Tạo API key tại Google AI Studio](https://aistudio.google.com/apikey)")
    else:
        st.info("Demo ngoại tuyến chạy không cần Internet hoặc API key. Kết quả là trích xuất câu, không phải Generative AI.")
    st.divider()
    st.caption("Đồ án minh họa: khảo sát Generative AI và triển khai ứng dụng tóm tắt văn bản. Không tải dữ liệu nhạy cảm lên dịch vụ bên ngoài.")

if "source" not in st.session_state:
    st.session_state.source = ""
if "result" not in st.session_state:
    st.session_state.result = None
if "last_duration" not in st.session_state:
    st.session_state.last_duration = None
if "last_mode" not in st.session_state:
    st.session_state.last_mode = None
if "last_source" not in st.session_state:
    st.session_state.last_source = ""

left, right = st.columns([1.15, 1], gap="large")

with left:
    st.markdown("### 📄 Văn bản đầu vào")
    a, b = st.columns([1, 2])
    if a.button("📋 Điền văn bản mẫu", use_container_width=True):
        st.session_state.source = EXAMPLE
    if b.button("🗑️ Xóa nội dung", use_container_width=True):
        st.session_state.source = ""
        st.session_state.result = None
    file = st.file_uploader(
        "Hoặc tải file Word (.docx), PDF, TXT, MD (tối đa 50 MB)",
        type=["txt", "md", "docx", "pdf"],
        help="PDF cần có lớp văn bản; PDF scan bằng ảnh chưa hỗ trợ OCR.",
    )
    if file is None:
        st.session_state.uploaded_signature = None
    else:
        raw = file.getvalue()
        signature = (file.name, hashlib.sha256(raw).hexdigest())
        if len(raw) > MAX_UPLOAD_BYTES:
            st.error("File lớn hơn 50 MB, hãy dùng file nhỏ hơn.")
        elif st.session_state.get("uploaded_signature") != signature:
            try:
                imported = extract_document(file.name, raw)
            except DocumentError as exc:
                st.error(str(exc))
            else:
                st.session_state.source = imported.text
                st.session_state.uploaded_signature = signature
                st.session_state.uploaded_truncated = imported.truncated
                st.session_state.result = None
                st.success(f"Đã đọc '{file.name}' — {word_count(imported.text):,} từ.")
        if st.session_state.get("uploaded_signature") == signature and st.session_state.get("uploaded_truncated"):
            st.warning(f"Tài liệu dài: chỉ {MAX_TEXT_CHARS:,} ký tự đầu được đọc. Hãy chia nhỏ tài liệu để tóm tắt toàn bộ.")
    source = st.text_area("Nội dung cần tóm tắt", key="source", height=320,
                          placeholder="Nhập một đoạn văn hoặc nhấn 'Điền văn bản mẫu'...")
    st.caption(f"{word_count(source):,} từ · {len(source):,} ký tự (giới hạn {MAX_TEXT_CHARS:,} ký tự)")
    with st.form("options_form"):
        length = st.radio("Độ dài bản tóm tắt", ["Ngắn", "Vừa", "Chi tiết"], horizontal=True, index=1)
        output_format = st.selectbox("Cách trình bày", ["Đoạn văn", "Gạch đầu dòng"])
        language = st.selectbox("Ngôn ngữ đầu ra (áp dụng với Gemini)",
                                ["Giữ ngôn ngữ gốc", "Tiếng Việt", "English"])
        submit = st.form_submit_button("✨ Tóm tắt văn bản", type="primary", use_container_width=True)

with right:
    st.markdown("### ✨ Kết quả tóm tắt")
    if submit:
        if not source.strip():
            st.error("Bạn chưa nhập văn bản.")
        elif word_count(source) < 25:
            st.error("Vui lòng nhập văn bản tối thiểu 25 từ để kết quả có ý nghĩa.")
        elif len(source) > MAX_TEXT_CHARS:
            st.error(f"Văn bản quá dài (giới hạn {MAX_TEXT_CHARS:,} ký tự).")
        elif mode.startswith("Gemini") and not api_key:
            st.error("Cần Gemini API key để gọi AI. Có thể chuyển sang chế độ Demo ngoại tuyến.")
        else:
            started = time.perf_counter()
            try:
                with st.spinner("Đang phân tích và tóm tắt..."):
                    if mode.startswith("Gemini"):
                        chunks = split_text_chunks(source)
                        if len(chunks) > 1:
                            st.info(f"Tài liệu dài sẽ cần {len(chunks) + 1} lượt gọi Gemini (có thể tốn thời gian/hạn mức API).")
                        progress_bar = st.progress(0, text="Đang tóm tắt...")
                        def update_progress(done: int, total: int) -> None:
                            progress_bar.progress(round(done / total * 100), text=f"Đã xử lý {done}/{total} lượt AI")
                        try:
                            result = gemini_summarize(source, api_key, length, output_format, language, model,
                                                      progress_callback=update_progress)
                        finally:
                            progress_bar.empty()
                    else:
                        result = offline_summarize(source, length, output_format)
                st.session_state.result = result
                st.session_state.last_duration = time.perf_counter() - started
                st.session_state.last_mode = mode
                st.session_state.last_source = source
            except Exception as exc:
                st.session_state.result = None
                st.error(f"Không thể xử lý yêu cầu: {exc}")
    result = st.session_state.result
    if result:
        st.success("Đã tạo bản tóm tắt")
        st.markdown(result)
        st.divider()
        st.download_button("⬇️ Tải kết quả (.txt)", data=result.encode("utf-8"),
                           file_name="ban_tom_tat.txt", mime="text/plain", use_container_width=True)
        if source != st.session_state.last_source:
            st.caption("Lưu ý: bạn đã sửa đầu vào; bản tóm tắt bên dưới thuộc văn bản ở lần chạy trước.")
        src_n, out_n = word_count(st.session_state.last_source), word_count(result)
        ratio = (1 - out_n / src_n) * 100 if src_n else 0
        m1, m2, m3 = st.columns(3)
        m1.metric("Từ đầu vào", f"{src_n:,}")
        m2.metric("Từ đầu ra", f"{out_n:,}")
        m3.metric("Rút gọn", f"{ratio:.0f}%")
        if st.session_state.last_duration is not None:
            st.caption(f"Thời gian xử lý: {st.session_state.last_duration:.2f} giây · Chế độ: {st.session_state.last_mode}")
        if st.session_state.last_mode and "Demo" in st.session_state.last_mode:
            st.warning("Đây là tóm tắt trích xuất (chọn câu gốc). Để trình diễn Generative AI thật, dùng Gemini API.")
        st.caption("AI có thể bỏ sót hoặc diễn giải sai thông tin. Hãy kiểm tra với bản gốc.")
    else:
        st.info("Kết quả xuất hiện tại đây sau khi nhấn **Tóm tắt văn bản**.")
        st.markdown("""**Gợi ý demo**

1. Nhấn **Điền văn bản mẫu**.
2. Chọn **Ngắn** hoặc **Vừa**.
3. Nhấn **Tóm tắt văn bản**.
4. Thử thay đổi độ dài và định dạng để so sánh.""")

st.divider()
st.caption("W5 Final Project · Hệ thống hỗ trợ học tập. Nhận xét độ chính xác phải dựa trên việc đối chiếu văn bản gốc.")
