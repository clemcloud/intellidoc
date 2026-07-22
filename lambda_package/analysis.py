import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# telling gemini exactly what shape we want back so we don't have to
# guess-parse whatever text it feels like sending
PROMPT = """Analyze the following document and return a JSON object with exactly these fields:
- "summary": a 2-3 sentence summary
- "key_points": a list of 3-6 key points
- "document_type": your best guess at the type of document (e.g. contract, report, invoice, essay)

Return ONLY valid JSON, no markdown formatting, no backticks.

Document text:
{text}
"""


def analyze_with_gemini(text: str) -> dict:
    # cutting off long docs so we don't blow past token limits
    # 15k chars is rough but good enough for now
    text = text[:15000]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=PROMPT.format(text=text)
    )

    raw = response.text.strip()

    # gemini sometimes wraps the json in ```json ... ``` even when told not to
    # stripping that out before we try to parse it
    if raw.startswith("```"):
        raw = raw.strip("`").replace("json", "", 1).strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"gemini didn't return valid json: {raw[:200]}") from e