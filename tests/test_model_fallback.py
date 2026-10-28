"""Kiểm thử chuyển model dự phòng khi Gemini trả 503; không cần API key thật."""
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from summarizer import FALLBACK_MODELS, gemini_summarize


class FakeAPIError(Exception):
    def __init__(self, code):
        self.code = code
        super().__init__(f"{code} error")


def fake_sdk(handler):
    client = types.SimpleNamespace(
        models=types.SimpleNamespace(generate_content=handler),
        close=lambda: None,
    )
    google = types.ModuleType("google")
    genai = types.ModuleType("google.genai")
    genai_types = types.ModuleType("google.genai.types")
    genai.Client = lambda api_key: client
    genai_types.ThinkingConfig = lambda **kwargs: kwargs
    genai_types.GenerateContentConfig = lambda **kwargs: kwargs
    genai.types = genai_types
    google.genai = genai
    return {"google": google, "google.genai": genai, "google.genai.types": genai_types}


class GeminiFallbackTests(unittest.TestCase):
    def test_first_model_busy_uses_backup(self):
        calls, selected = [], []
        def generate_content(**kwargs):
            calls.append(kwargs["model"])
            if kwargs["model"] == "gemini-3.8-flash":
                raise FakeAPIError(503)
            return types.SimpleNamespace(text="Kết quả dự phòng.")
        with patch.dict(sys.modules, fake_sdk(generate_content)):
            result = gemini_summarize(
                "Văn bản thử nghiệm có đủ nội dung để tóm tắt.",
                "test-key", model_used_callback=selected.append
            )
        self.assertEqual(result, "Kết quả dự phòng.")
        self.assertEqual(calls, ["gemini-3.8-flash", FALLBACK_MODELS[0]])
        self.assertEqual(selected, [FALLBACK_MODELS[0]])

    def test_all_models_busy_reports_friendly_error(self):
        calls = []
        def generate_content(**kwargs):
            calls.append(kwargs["model"])
            raise FakeAPIError(503)
        with patch.dict(sys.modules, fake_sdk(generate_content)):
            with self.assertRaisesRegex(RuntimeError, "quá tải \\(503\\)"):
                gemini_summarize("Nội dung cần tóm tắt.", "test-key")
        self.assertEqual(calls, ["gemini-3.8-flash", *FALLBACK_MODELS])

    def test_invalid_key_does_not_trigger_fallback(self):
        calls = []
        def generate_content(**kwargs):
            calls.append(kwargs["model"])
            raise FakeAPIError(401)
        with patch.dict(sys.modules, fake_sdk(generate_content)):
            with self.assertRaises(FakeAPIError) as error:
                gemini_summarize("Nội dung cần tóm tắt.", "test-key")
        self.assertEqual(error.exception.code, 401)
        self.assertEqual(calls, ["gemini-3.8-flash"])

    def test_rate_limit_does_not_trigger_fallback(self):
        calls = []
        def generate_content(**kwargs):
            calls.append(kwargs["model"])
            raise FakeAPIError(429)
        with patch.dict(sys.modules, fake_sdk(generate_content)):
            with self.assertRaises(FakeAPIError):
                gemini_summarize("Nội dung cần tóm tắt.", "test-key")
        self.assertEqual(calls, ["gemini-3.8-flash"])


if __name__ == "__main__":
    unittest.main()
