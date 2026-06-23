#!/usr/bin/env python3
"""
Pipeline orchestrator for OCR+LLM workflow.
Iterates over files in the INPUT_DIR, processes each with ocr_extractor.process_file,
structures the result as JSON and writes to ./output/.
Environment variables:
  INPUT_DIR  – directory containing input images/PDFs (default: ./input)
  OUTPUT_DIR – directory for JSON results (default: ./output)
The script avoids absolute paths and hard‑coded credentials.
"""

import os
import json
from pathlib import Path
from typing import List, Dict

# Local import – assumes ocr_extractor.py is in the same package
from ocr_extractor import process_file, clean_text


def get_input_files(input_dir: Path) -> List[Path]:
    """Return a list of image or PDF files in *input_dir* (non‑recursive)."""
    supported = {".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif", ".pdf"}
    return [p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() in supported]


def ensure_dir(path: Path) -> None:
    """Create *path* if it does not exist (idempotent)."""
    path.mkdir(parents=True, exist_ok=True)


def main() -> None:
    # Resolve directories from environment or defaults (relative to script location)
    base_dir = Path(__file__).resolve().parent
    input_dir = Path(os.getenv("INPUT_DIR", base_dir / "input"))
    output_dir = Path(os.getenv("OUTPUT_DIR", base_dir / "output"))

    ensure_dir(output_dir)

    files = get_input_files(input_dir)
    if not files:
        print(f"[INFO] No supported files found in {input_dir}")
        return

    for file_path in files:
        try:
            result = process_file(file_path)
            # Clean the raw OCR text for a nicer payload
            result["cleaned_text"] = clean_text(result.get("raw_text", ""))
            # Prepare JSON output
            output_data: Dict = {
                "file_name": file_path.name,
                "raw_text": result.get("raw_text", ""),
                "cleaned_text": result.get("cleaned_text", ""),
                "description": result.get("description", ""),
            }
            out_path = output_dir / f"{file_path.stem}.json"
            with out_path.open("w", encoding="utf-8") as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            print(f"[DONE] Processed {file_path.name} -> {out_path.name}")
        except Exception as e:
            print(f"[ERROR] Failed processing {file_path.name}: {e}")


if __name__ == "__main__":
    main()
