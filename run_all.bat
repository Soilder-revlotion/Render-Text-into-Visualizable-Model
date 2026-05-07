@echo off
chcp 65001 >nul
echo =============================================
echo    Text Knowledge Planet - Pipeline
echo =============================================
echo.

REM ── 模型选择 ──
set MODEL_ID=gemini-2.5-flash
set MODEL_URL=
set USE_OLLAMA=0

echo Select model mode:
echo   1. Local Ollama (default: qwen2.5:7b)
echo   2. Google Gemini API (needs API key)
echo   3. Custom model
echo.
set /p CHOICE="Enter choice [1/2/3] (default=1): "

if "%CHOICE%"=="2" goto :MODE_API
if "%CHOICE%"=="3" goto :MODE_CUSTOM
:MODE_OLLAMA
  set USE_OLLAMA=1
  echo Enter Ollama model ID [qwen2.5:7b]:
  set /p MODEL_ID=
  if "%MODEL_ID%"=="" set MODEL_ID=qwen2.5:7b
  echo Enter Ollama URL [http://localhost:11434]:
  set /p MODEL_URL=
  if "%MODEL_URL%"=="" set MODEL_URL=http://localhost:11434
  goto :RUN_EXTRACT
:MODE_API
  echo Using Google Gemini API with model: %MODEL_ID%
  if "%LANGEXTRACT_API_KEY%"=="" if "%GOOGLE_API_KEY%"=="" (
      echo Enter your API key:
      set /p API_KEY_INPUT=
      set GOOGLE_API_KEY=%API_KEY_INPUT%
  )
  goto :RUN_EXTRACT
:MODE_CUSTOM
  echo Enter model ID:
  set /p MODEL_ID=
  echo Enter model URL (or leave blank):
  set /p MODEL_URL=
  goto :RUN_EXTRACT

:RUN_EXTRACT
echo.
echo [1/5] Running LangExtract extraction with model: %MODEL_ID%...

if "%USE_OLLAMA%"=="1" (
    set CMD_EXTRA=--model "%MODEL_ID%" --model-url "%MODEL_URL%"
) else (
    set CMD_EXTRA=--model "%MODEL_ID%"
)

python milestone2_extract.py --text-file sample_text.txt --output-dir . %CMD_EXTRA%
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Extraction failed. Check your model / API key / network.
    goto :END
)
echo [1/5] Done.

echo.
echo [2/5] Converting extraction results to graph data...
python milestone3_convert.py --input extraction_results.jsonl --output graph_data.json
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Conversion failed.
    goto :END
)
echo [2/5] Done.

echo.
echo [3/5] Running quality check...
python milestone5_quality.py --input graph_data.json --fix
if %ERRORLEVEL% neq 0 (
    echo [WARNING] Quality check had issues but continuing...
)
echo [3/5] Done.

echo.
echo [4/5] Building 3D cosmos visualization...
python build_cosmos.py
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Build failed.
    goto :END
)
echo [4/5] Done.

echo.
echo =============================================
echo    [5/5] Pipeline complete!
echo    Output Files:
echo    - cosmos.html          (3D interactive globe)
echo    - highlight.html       (text highlight verification)
echo    - graph_data.json      (graph structure data)
echo    - extraction_results.jsonl (raw extraction data)
echo =============================================
echo.
echo Open cosmos.html in a browser to explore your Text Knowledge Planet!
echo.
pause

:END
