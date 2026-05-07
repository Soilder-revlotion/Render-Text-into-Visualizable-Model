@echo off
chcp 65001 >nul
echo =============================================
echo    Text Knowledge Planet - Pipeline
echo =============================================
echo.

REM Check for API key
if "%LANGEXTRACT_API_KEY%"=="" (
    if "%GOOGLE_API_KEY%"=="" (
        echo [WARNING] No API key found. Set LANGEXTRACT_API_KEY or GOOGLE_API_KEY.
        echo Using existing extraction_results.jsonl if available...
        echo.
        goto :SKIP_EXTRACT
    )
)

echo [1/5] Running LangExtract extraction...
python milestone2_extract.py --text-file sample_text.txt --output-dir .
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Extraction failed. Check your API key and network.
    goto :END
)
echo [1/5] Done.
goto :AFTER_EXTRACT

:SKIP_EXTRACT
echo [1/5] SKIPPED - using existing extraction_results.jsonl
echo.

:AFTER_EXTRACT
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
echo.
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

echo [5/5] Pipeline complete!
echo.
echo =============================================
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
