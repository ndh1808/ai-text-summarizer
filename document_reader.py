"""Trích xuất văn bản từ tài liệu người dùng tải lên (không thực hiện OCR).

Tệp chỉ được xử lý trong bộ nhớ, không được lưu lại trên máy chủ.
"""
from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile, BadZipFile

MAX_UPLOAD_BYTES = 50 * 1024 * 1024
MAX_TEXT_CHARS = 200_000
MAX_PDF_PAGES = 300
SUPPORTED_SUFFIXES = {".txt", ".md", ".docx", ".pdf"}


class DocumentError(ValueError):
    """Lỗi đầu vào có thể trình bày trực tiếp cho người sử dụng."""


@dataclass(frozen=True)
class ParsedDocument:
    text: str
    truncated: bool = False


def _read_docx(content: bytes) -> str:
    from docx import Document
    from docx.table import Table

    try:
        # Tệp DOCX là ZIP: tránh đọc archive nén bất thường vào RAM.
        with ZipFile(BytesIO(content)) as archive:
            inflated = sum(item.file_size for item in archive.infolist())
            if inflated > 120 * 1024 * 1024:
                raise DocumentError("File Word có dữ liệu giải nén quá lớn (giới hạn 120 MB).")
        document = Document(BytesIO(content))
        sections: list[str] = []
        count = 0
        # Giữ thêm 1 ký tự để có thể báo cắt bớt chính xác.
        def append(value: str) -> None:
            nonlocal count
            if not value or count > MAX_TEXT_CHARS:
                return
            piece = value[: MAX_TEXT_CHARS + 1 - count]
            sections.append(piece)
            count += len(piece) + 1

        # Đọc văn bản và bảng theo thứ tự, dừng sớm khi đã đủ giới hạn.
        for block in document.iter_inner_content():
            if isinstance(block, Table):
                for row in block.rows:
                    cells = [cell.text.strip() for cell in row.cells]
                    if any(cells):
                        append(" | ".join(cells))
                    if count > MAX_TEXT_CHARS:
                        break
            else:
                append(block.text.strip())
            if count > MAX_TEXT_CHARS:
                break
        return "\n".join(sections)
    except DocumentError:
        raise
    except Exception as exc:
        raise DocumentError("Không đọc được file Word. Vui lòng dùng file .docx hợp lệ (không phải .doc cũ).") from exc


def _read_pdf(content: bytes) -> str:
    from pypdf import PdfReader

    try:
        reader = PdfReader(BytesIO(content), strict=False)
        if reader.is_encrypted:
            raise DocumentError("PDF có mật khẩu/mã hóa. Hãy mở khóa trước khi tải lên.")
        if len(reader.pages) > MAX_PDF_PAGES:
            raise DocumentError(f"PDF quá dài (tối đa {MAX_PDF_PAGES} trang). Hãy chia nhỏ tài liệu.")
        chunks = []
        count = 0
        for page in reader.pages:
            # Chỉ đọc lớp text; PDF scan thuần ảnh cần OCR bên ngoài.
            extracted = (page.extract_text() or "").strip()
            if extracted:
                piece = extracted[: MAX_TEXT_CHARS + 1 - count]
                chunks.append(piece)
                count += len(piece) + 2
            # Dừng sớm và đánh dấu vượt quá giới hạn nội dung.
            if count > MAX_TEXT_CHARS:
                break
        return "\n\n".join(chunks)
    except DocumentError:
        raise
    except Exception as exc:
        raise DocumentError("Không thể đọc PDF. Hãy kiểm tra file có bị hỏng hoặc mã hóa không.") from exc


def extract_document(filename: str, content: bytes) -> ParsedDocument:
    """Đọc TXT, MD, DOCX hoặc PDF và báo nếu phải giới hạn ký tự."""
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise DocumentError("Chỉ hỗ trợ tệp TXT, MD, DOCX và PDF.")
    if not content:
        raise DocumentError("File trống. Vui lòng chọn file có nội dung.")
    if len(content) > MAX_UPLOAD_BYTES:
        raise DocumentError("File lớn hơn 50 MB. Hãy chia nhỏ hoặc nén tài liệu rồi tải lại.")

    if suffix in {".txt", ".md"}:
        try:
            text = content.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise DocumentError("Tệp TXT/MD phải sử dụng mã hóa UTF-8.") from exc
    elif suffix == ".docx":
        text = _read_docx(content)
    else:
        text = _read_pdf(content)

    text = text.strip()
    if not text:
        if suffix == ".pdf":
            raise DocumentError(
                "PDF không có lớp văn bản có thể sao chép (thường là file scan/ảnh). "
                "Ứng dụng chưa hỗ trợ OCR. Hãy chuyển PDF qua OCR hoặc dùng PDF có văn bản."
            )
        raise DocumentError("Không tìm thấy nội dung văn bản trong file.")
    truncated = len(text) > MAX_TEXT_CHARS
    return ParsedDocument(text=text[:MAX_TEXT_CHARS], truncated=truncated)
