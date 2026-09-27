#!/usr/bin/env python3
"""
Text Report Generator
A simple non-web CLI tool for Task 4.4 (High Distinction).

Reads all .txt files from an input directory, computes word-frequency
statistics, and writes a report (JSON + plain text) to an output directory.

Designed to be run inside Docker with host-mounted volumes:
    -v <input-folder>:/data/input
    -v <output-folder>:/data/output
"""

import sys
import os
import re
import json
import time
from collections import Counter
from datetime import datetime, timezone

INPUT_DIR = os.environ.get("INPUT_DIR", "/data/input")
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "/data/output")
TOP_N = int(os.environ.get("TOP_N", "15"))

WORD_RE = re.compile(r"[A-Za-z']+")


def log(msg: str) -> None:
    """Timestamped log line, flushed immediately so `docker logs` shows it live."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[{ts}] {msg}", flush=True)


def main() -> int:
    log("Text Report Generator starting")
    log(f"Input directory : {INPUT_DIR}")
    log(f"Output directory: {OUTPUT_DIR}")

    if not os.path.isdir(INPUT_DIR):
        log(f"ERROR: input directory '{INPUT_DIR}' does not exist. "
            f"Did you mount a volume with -v?")
        return 1

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    txt_files = sorted(
        f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".txt")
    )

    if not txt_files:
        log(f"WARNING: no .txt files found in {INPUT_DIR}. Nothing to analyze.")
        return 0

    log(f"Found {len(txt_files)} text file(s): {', '.join(txt_files)}")

    total_words = 0
    total_lines = 0
    word_counter = Counter()
    per_file_stats = {}

    for filename in txt_files:
        path = os.path.join(INPUT_DIR, filename)
        log(f"Processing {filename} ...")
        time.sleep(0.3)  # simulate work, makes log timestamps meaningfully progress

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        lines = content.splitlines()
        words = WORD_RE.findall(content.lower())

        word_counter.update(words)
        total_words += len(words)
        total_lines += len(lines)

        per_file_stats[filename] = {
            "lines": len(lines),
            "words": len(words),
        }
        log(f"  -> {filename}: {len(lines)} lines, {len(words)} words")

    top_words = word_counter.most_common(TOP_N)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files_processed": txt_files,
        "totals": {
            "files": len(txt_files),
            "lines": total_lines,
            "words": total_words,
            "unique_words": len(word_counter),
        },
        "per_file": per_file_stats,
        "top_words": [{"word": w, "count": c} for w, c in top_words],
    }

    json_path = os.path.join(OUTPUT_DIR, "report.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    log(f"Wrote {json_path}")

    txt_path = os.path.join(OUTPUT_DIR, "report.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("TEXT REPORT GENERATOR — SUMMARY\n")
        f.write("=" * 40 + "\n")
        f.write(f"Generated at : {report['generated_at']}\n")
        f.write(f"Files scanned: {len(txt_files)}\n")
        f.write(f"Total lines  : {total_lines}\n")
        f.write(f"Total words  : {total_words}\n")
        f.write(f"Unique words : {len(word_counter)}\n\n")
        f.write(f"Top {TOP_N} most common words:\n")
        for word, count in top_words:
            f.write(f"  {word:<15} {count}\n")
    log(f"Wrote {txt_path}")

    log("Done. Exiting with status 0.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
