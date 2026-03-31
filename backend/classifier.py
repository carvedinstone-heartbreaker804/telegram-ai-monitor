import json
from openai import OpenAI


SYSTEM_PROMPT = """
You classify Telegram community messages.

Return valid JSON only in this exact format:
{
  "category": "Spam" | "Important" | "Question" | "Normal",
  "reason": "short explanation",
  "confidence": 0.0
}

Classification rules:
- Spam: promotions, scams, irrelevant ads, repeated junk, obvious solicitation
- Important: urgent update, critical signal, admin-style notice, highly actionable content
- Question: user is asking for help, clarification, or information
- Normal: regular conversation that is not spam, not a key alert, and not a question

Confidence must be a number between 0 and 1.
Keep reason short and clear.
Do not include markdown.
"""


class MessageClassifier:
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def classify(self, message_text: str) -> dict:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Classify this message:\n\n{message_text}"
                },
            ],
        )

        content = response.choices[0].message.content
        parsed = json.loads(content)

        category = parsed.get("category", "Normal")
        reason = parsed.get("reason", "No reason provided")
        confidence = parsed.get("confidence", 0.5)

        allowed_categories = {"Spam", "Important", "Question", "Normal"}
        if category not in allowed_categories:
            category = "Normal"

        try:
            confidence = float(confidence)
        except (TypeError, ValueError):
            confidence = 0.5

        confidence = max(0.0, min(confidence, 1.0))

        return {
            "category": category,
            "reason": reason,
            "confidence": confidence,
        }