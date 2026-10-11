import os
import json
from typing import Optional, Dict, Any
from .models import IntentClassification

SYSTEM_PROMPT = """You are a Two-Class AI Call Transcript Intent Classifier.
Your job is to analyze AI sales/support call transcripts and classify customer intent into exactly one of:
- INTERESTED
- NOT_INTERESTED

Critical Principles:
1. Classify CUSTOMER INTENT, NOT CUSTOMER SENTIMENT. Customers can be angry, skeptical, or impatient and still be INTERESTED. Polite customers can reject and be NOT_INTERESTED.
2. Low threshold for INTERESTED: Any meaningful positive buying/engagement signal, questions about price/workings/benefits, conditional interest ("call me later", "let me think"), skepticism with continued discussion, or WhatsApp details request.
3. Long conversation (>1 min) or multi-turn engagement without clear rejection -> INTERESTED.
4. Positive signals override earlier hesitation or soft rejections.
5. Explicit final rejection ("Nahi chahiye", "I don't need this") -> NOT_INTERESTED.
6. Explicit do-not-contact / opt-out ("Don't call me again", "Remove my number") -> NOT_INTERESTED (Priority 1, overrides everything).
7. Wrong person / irrelevant customer -> NOT_INTERESTED.
8. If transcript is ambiguous, unclear, or noisy with no clear rejection -> INTERESTED.
9. Empty transcript / immediate disconnect with no evidence of interest -> NOT_INTERESTED.
10. Differentiate Agent statements from Customer statements. Agent questions do NOT count as customer interest.

STRICT OUTPUT FORMAT:
Return strictly a valid JSON object:
{"classification": "INTERESTED"}
or
{"classification": "NOT_INTERESTED"}
Do not output anything else.
"""

class LLMClassifierAdapter:
    """
    Optional LLM adapter supporting OpenAI or Gemini APIs when API keys are configured.
    Falls back safely if no API key is set or on network failure.
    """

    def __init__(self):
        self.openai_key = os.environ.get("OPENAI_API_KEY")
        self.gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

    def is_available(self) -> bool:
        return bool(self.openai_key or self.gemini_key)

    def classify(self, transcript: str) -> Optional[Dict[str, str]]:
        """Invokes LLM if configured, returns {'classification': '...'} or None."""
        if self.openai_key:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=self.openai_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": transcript}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.0
                )
                raw_json = response.choices[0].message.content
                data = json.loads(raw_json)
                if data.get("classification") in ["INTERESTED", "NOT_INTERESTED"]:
                    return {"classification": data["classification"]}
            except Exception:
                return None
        return None
