import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch
from io import BytesIO

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from document_reader import DocumentError, extract_document, MAX_PDF_PAGES
from summarizer import gemini_summarize, split_text_chunks


class LargeDocumentTests(unittest.TestCase):
    def test_pdf_max_pages(self):
        from pypdf import PdfWriter
        writer = PdfWriter()
        for _ in range(MAX_PDF_PAGES + 1):
            writer.add_blank_page(width=250, height=250)
        bio = BytesIO()
        writer.write(bio)
        with self.assertRaisesRegex(DocumentError, "300 trang"):
            extract_document("long.pdf", bio.getvalue())

    def test_large_text_is_not_silently_accepted_entirely(self):
        text = "nội dung tài liệu " * 16_000
        result = extract_document("document.txt", text.encode("utf-8"))
        self.assertEqual(len(result.text), 200_000)
        self.assertTrue(result.truncated)

    def test_map_reduce_with_fake_model(self):
        # Mock SDK to verify number of calls and progress without real API key.
        calls = []
        fake_client = types.SimpleNamespace(
            models=types.SimpleNamespace(
                generate_content=lambda **kwargs: (
                    calls.append(kwargs), types.SimpleNamespace(text="Tóm tắt dữ liệu nguồn."))[1]),
            close=lambda: None,
        )
        fake_google = types.ModuleType("google")
        fake_genai = types.ModuleType("google.genai")
        fake_types = types.ModuleType("google.genai.types")
        fake_genai.Client = lambda api_key: fake_client
        fake_types.GenerateContentConfig = lambda **kwargs: kwargs
        fake_genai.types = fake_types
        fake_google.genai = fake_genai
        text = "Hội nghị tổng kết những kết quả mới của ngành khoa học. " * 750
        chunks = split_text_chunks(text)
        progress = []
        with patch.dict(sys.modules, {"google": fake_google, "google.genai": fake_genai,
                                     "google.genai.types": fake_types}):
            result = gemini_summarize(text, "fake-testing-key", progress_callback=lambda done, total: progress.append((done, total)))
        self.assertGreater(len(chunks), 1)
        self.assertEqual(len(calls), len(chunks) + 1)
        self.assertEqual(progress[-1], (len(calls), len(calls)))
        self.assertEqual(result, "Tóm tắt dữ liệu nguồn.")


if __name__ == "__main__":
    unittest.main()
