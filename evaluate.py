"""Repeatable comparison of offline summaries. Does not invent accuracy ratings.

Usage:
    python evaluate.py
    python evaluate.py --mode gemini --length Vừa
Requires GEMINI_API_KEY in the environment or .env for Gemini mode.
"""
from __future__ import annotations

import argparse
import csv
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from summarizer import gemini_summarize, offline_summarize, word_count

ROOT = Path(__file__).parent
load_dotenv(ROOT / '.env')


def run(mode: str, length: str, output: Path) -> int:
    cases = [ROOT / 'examples' / 'van_ban_mau.txt', ROOT / 'examples' / 'english_sample.txt']
    output.parent.mkdir(parents=True, exist_ok=True)
    records = []
    for source_file in cases:
        source = source_file.read_text(encoding='utf-8')
        started = time.perf_counter()
        if mode == 'gemini':
            key = os.environ.get('GEMINI_API_KEY', '').strip()
            if not key:
                raise ValueError('Thiếu GEMINI_API_KEY; sửa .env hoặc dùng --mode demo')
            summary = gemini_summarize(source, key, length)
        else:
            summary = offline_summarize(source, length)
        seconds = round(time.perf_counter() - started, 3)
        count_in, count_out = word_count(source), word_count(summary)
        records.append({
            'input_file': source_file.name,
            'mode': mode,
            'length': length,
            'input_words': count_in,
            'output_words': count_out,
            'compression_percent': round(100 * (1 - count_out / count_in), 2),
            'processing_seconds': seconds,
            'accuracy_1_to_5_manual': '',
            'coverage_1_to_5_manual': '',
            'readability_1_to_5_manual': '',
            'summary': summary,
        })
    with output.open('w', encoding='utf-8-sig', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    print(f'Đã tạo: {output} ({len(records)} văn bản).')
    print('Ba cột đánh giá thủ công đang để trống: hãy đọc bản gốc rồi chấm, không tự suy đoán.')
    return len(records)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['demo', 'gemini'], default='demo')
    parser.add_argument('--length', choices=['Ngắn', 'Vừa', 'Chi tiết'], default='Vừa')
    parser.add_argument('--output', type=Path, default=ROOT / 'results' / 'evaluation.csv')
    args = parser.parse_args()
    run(args.mode, args.length, args.output)
