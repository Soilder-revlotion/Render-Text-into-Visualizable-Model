"""
Milestone 2: LangExtract Extraction Script
==========================================
Runs LangExtract with the designed templates to extract entities
and causal chains from text, producing a JSONL file and highlight HTML.

支持两种模型:

  1. 本地 Ollama 模型 (推荐，免费，无需 API Key):
     ollama serve                    # 启动 Ollama 服务 (默认 http://localhost:11434)
     ollama pull qwen2.5:7b          # 下载模型
     python milestone2_extract.py --text-file sample_text.txt --model qwen2.5:7b

  2. Google Gemini API (需要 API Key):
     set GOOGLE_API_KEY=your_google_api_key
     python milestone2_extract.py --text-file sample_text.txt --api-key YOUR_KEY
     python milestone2_extract.py --text-file sample_text.txt --model gemini-2.5-flash

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

# 本地 Ollama 模型默认地址
OLLAMA_DEFAULT_URL = "http://localhost:11434"


def run_extraction(
    text: str,
    output_dir: str = ".",
    api_key: str | None = None,
    model_id: str = "gemini-2.5-flash",
    model_url: str | None = None,
) -> str:
    """Run LangExtract extraction and save results.

    Args:
        text: Input text to extract from.
        output_dir: Directory for output files.
        api_key: API key (only needed for Gemini/OpenAI, not for Ollama).
        model_id: LLM model ID. Ollama models auto-detected by prefix
                  (gemma, llama, qwen, deepseek, mistral, phi, etc.).
        model_url: Custom model endpoint URL (e.g. http://localhost:11434 for Ollama).

    Returns:
        Path to the JSONL output file.
    """
    out = pathlib.Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    print(f"Running extraction with model: {model_id}")
    if model_url:
        print(f"Model URL: {model_url}")
    if api_key:
        print("Using API key from parameter")
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
        model_url=model_url,
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
    parser.add_argument("--api-key", default=None, help="API key (Gemini/OpenAI only; not needed for Ollama)")
    parser.add_argument("--model", default="gemini-2.5-flash", help="Model ID. For Ollama use e.g. qwen2.5:7b, gemma2:2b")
    parser.add_argument("--model-url", default=None, help="Custom model URL (for Ollama: http://localhost:11434)")
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
        model_url=args.model_url,
    )


if __name__ == "__main__":
    main()
