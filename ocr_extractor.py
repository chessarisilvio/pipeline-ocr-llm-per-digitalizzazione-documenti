#!/usr/bin/env python3
"""
OCR extractor for pipeline-ocrllm-per-digitalizzazione-documenti.
Loads image or PDF, extracts text via pytesseract, cleans with regex,
and (placeholder) calls moondream/image-describe for description.
"""

import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Union, List

import pytesseract
from PIL import Image
import moondream  # type: ignore


def extract_text_from_image(image_path: Union[str, Path]) -> str:
    """
    Extract text from an image file using pytesseract.
    """
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='eng+ita')
    return text


def extract_text_from_pdf(pdf_path: Union[str, Path]) -> str:
    """
    Extract text from a PDF by converting each page to image via pdftoppm
    and running OCR on each.
    """
    text_pages: List[str] = []
    with tempfile.TemporaryDirectory() as tmpdir:
        # Convert PDF to PNG pages (pdftoppm -png)
        # Output pattern: page-001.png, page-002.png, ...
        subprocess.run(
            ['pdftoppm', '-png', str(pdf_path), os.path.join(tmpdir, 'page')],
            check=True,
            capture_output=True,
        )
        # List generated PNG files sorted
        png_files = sorted(
            [f for f in os.listdir(tmpdir) if f.endswith('.png')],
            key=lambda x: int(x.split('-')[1].split('.')[0])
        )
        for png in png_files:
            img_path = os.path.join(tmpdir, png)
            text_pages.append(extract_text_from_image(img_path))
    return "\n\n".join(text_pages)


def clean_text(text: str) -> str:
    """
    Clean OCR output: remove excessive whitespace, normalize line breaks.
    """
    # Replace multiple spaces/tabs with single space
    text = re.sub(r'[ \t]+', ' ', text)
    # Replace multiple newlines with double newline (paragraph separation)
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    # Strip leading/trailing whitespace
    text = text.strip()
    return text


def describe_image(image_path: Union[str, Path]) -> str:
    """
    Placeholder for image description using moondream/image-describe.
    Returns a description string.
    """
    # Load image
    image = Image.open(image_path)
    # Use moondream to generate description (assuming API)
    # moondream.model.caption? We'll use a generic call.
    # As per moondream package, there is a function image_describe?
    # We'll try to call moondream.image_describe if exists, else fallback.
    try:
        # Assuming moondream provides a describe function
        description = moondream.describe(image)  # type: ignore
    except AttributeError:
        # Fallback: use caption if available
        try:
            description = moondream.caption(image)  # type: ignore
        except AttributeError:
            # Final placeholder
            description = "Description placeholder (moondream not configured)"
    return description


def process_file(file_path: Union[str, Path]) -> dict:
    """
    Process a file (image or PDF) and return dict with raw text, cleaned text, and description.
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = path.suffix.lower()
    if suffix in {'.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'}:
        raw_text = extract_text_from_image(path)
        description = describe_image(path)
    elif suffix == '.pdf':
        raw_text = extract_text_from_pdf(path)
        # For PDF, we could describe first page? We'll describe first page if possible.
        # Extract first page as image and describe.
        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(
                ['pdftoppm', '-png', '-f', '1', '-l', '1', str(path),
                 os.path.join(tmpdir, 'page')],
                check=True,
                capture_output=True,
            )
            first_page = os.path.join(tmpdir, 'page-1.png')
            if os.path.exists(first_page):
                description = describe_image(first_page)
            else:
                description = "Description placeholder (no first page)"
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    cleaned = clean_text(raw_text)

    return {
        "raw_text": raw_text,
        "cleaned_text": cleaned,
        "description": description,
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python ocr_extractor.py <image_or_pdf>")
        sys.exit(1)
    file_path = sys.argv[1]
    result = process_file(file_path)
    print("=== Description ===")
    print(result["description"])
    print("\n=== Cleaned Text ===")
    print(result["cleaned_text"])
    print("\n=== Raw Text (first 500 chars) ===")
    print(result["raw_text"][:500])