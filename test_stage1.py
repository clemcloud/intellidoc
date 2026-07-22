# test_stage1.py
from extraction import extract_text
from analysis import analyze_with_gemini

def extract_and_analyze(file_path: str) -> dict:
    text = extract_text(file_path)
    result = analyze_with_gemini(text)
    return result

if __name__ == "__main__":
    result = extract_and_analyze("sample.pdf")
    print(result)