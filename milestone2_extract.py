"""
Milestone 2: LangExtract Extraction Script
==========================================
Runs LangExtract with the designed templates to extract entities
and causal chains from text, producing a JSONL file and highlight HTML.

Usage:
    # Set your API key first:
    set LANGEXTRACT_API_KEY=your_google_api_key
    # or: set GOOGLE_API_KEY=your_key
    # or pass --api-key

    python milestone2_extract.py [--text-file sample_text.txt] [--api-key YOUR_KEY]

Dependencies:
    pip install langextract
"""
from __future__ import annotations
import argparse
import pathlib
import sys

from langextract.core.data import ExampleData
import langextract as lx

from milestone1_design import PROMPT_DESCRIPTION, EXAMPLES


def run_extraction(
    text: str,
    output_dir: str = ".",
    api_key: str | None = None,
    model_id: str = "gemini-2.5-flash",
) -> str:
    """Run LangExtract extraction and save results.

    Args:
        text: Input text to extract from.
        output_dir: Directory for output files.
        api_key: Google API key (or set LANGEXTRACT_API_KEY env var).
        model_id: LLM model ID.

    Returns:
        Path to the JSONL output file.
    """
    out = pathlib.Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    print(f"Running extraction with model: {model_id}")
    print(f"Text length: {len(text)} characters")
    print(f"Examples: {len(EXAMPLES)}")
    print("-" * 50)

    # Run extraction
    annotated_doc = lx.extract(
        text,
        prompt_description=PROMPT_DESCRIPTION,
        examples=EXAMPLES,
        model_id=model_id,
        api_key=api_key,
        temperature=0.1,
        show_progress=True,
    )

    # Save to JSONL
    jsonl_path = out / "extraction_results.jsonl"
    lx.io.save_annotated_documents(
        iter([annotated_doc]),
        output_dir=str(out),
        output_name="extraction_results.jsonl",
    )
    print(f"\nExtraction results saved to: {jsonl_path}")
    print(f"Extracted {len(annotated_doc.extractions or [])} items")

    # Count by class
    classes: dict[str, int] = {}
    for ext in (annotated_doc.extractions or []):
        classes[ext.extraction_class] = classes.get(ext.extraction_class, 0) + 1
    print("\nExtraction summary:")
    for cls, count in sorted(classes.items()):
        print(f"  {cls}: {count}")

    # Generate highlight HTML
    html = lx.visualize(annotated_doc, animation_speed=1.5, gif_optimized=True)
    html_path = out / "highlight.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>Extraction Highlights</title></head><body>{html}</body></html>")
    print(f"Highlight HTML saved to: {html_path}")

    return str(jsonl_path)


def main():
    parser = argparse.ArgumentParser(description="LangExtract extraction runner")
    parser.add_argument("--text-file", default="sample_text.txt", help="Input text file")
    parser.add_argument("--text", default=None, help="Input text directly")
    parser.add_argument("--api-key", default=None, help="Google API key")
    parser.add_argument("--model", default="gemini-2.5-flash", help="Model ID")
    parser.add_argument("--output-dir", default=".", help="Output directory")
    args = parser.parse_args()

    if args.text:
        text = args.text
    else:
        text_path = pathlib.Path(args.text_file)
        if not text_path.exists():
            print(f"Error: Text file not found: {text_path}")
            sys.exit(1)
        text = text_path.read_text(encoding="utf-8")

    run_extraction(
        text=text,
        output_dir=args.output_dir,
        api_key=args.api_key,
        model_id=args.model,
    )


if __name__ == "__main__":
    main()
