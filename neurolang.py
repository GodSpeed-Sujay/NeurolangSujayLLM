"""NeuroLang: NLP intent-to-voice bridge for assistive button devices."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Optional

from neurolang_data import INTENT_SYNONYMS, LOCALIZED_OUTPUTS

try:
    import pyttsx3
except ImportError:  # Optional runtime dependency.
    pyttsx3 = None


@dataclass
class InterpretationResult:
    """Result of mapping a user/button input to an intent and localized text."""

    raw_input: str
    normalized_input: str
    intent: str
    confidence: float
    lang: str
    localized_text: str


class NeuroLangEngine:
    """Intent matching + localized output + optional text-to-speech."""

    def __init__(self, default_lang: str = "en", match_threshold: float = 0.6) -> None:
        self.default_lang = default_lang
        self.match_threshold = match_threshold

    @staticmethod
    def normalize(text: str) -> str:
        text = text.strip().lower()
        text = re.sub(r"\s+", " ", text)
        return text

    def _best_intent(self, normalized_text: str) -> tuple[str, float]:
        best_intent = "UNKNOWN"
        best_score = 0.0

        for intent, phrases in INTENT_SYNONYMS.items():
            for phrase in phrases:
                score = SequenceMatcher(None, normalized_text, phrase).ratio()
                if normalized_text == phrase:
                    return intent, 1.0
                if phrase in normalized_text or normalized_text in phrase:
                    score = max(score, 0.88)
                if score > best_score:
                    best_score = score
                    best_intent = intent

        if best_score < self.match_threshold:
            return "UNKNOWN", best_score
        return best_intent, best_score

    def interpret(self, button_text: str, lang: Optional[str] = None) -> InterpretationResult:
        normalized = self.normalize(button_text)
        selected_lang = lang or self.default_lang
        if selected_lang not in LOCALIZED_OUTPUTS:
            selected_lang = "en"

        intent, confidence = self._best_intent(normalized)
        localized_text = LOCALIZED_OUTPUTS[selected_lang].get(
            intent,
            LOCALIZED_OUTPUTS[selected_lang]["UNKNOWN"],
        )

        return InterpretationResult(
            raw_input=button_text,
            normalized_input=normalized,
            intent=intent,
            confidence=confidence,
            lang=selected_lang,
            localized_text=localized_text,
        )

    def speak(self, text: str, lang: str = "en") -> bool:
        """Speak output text if pyttsx3 is installed. Returns True when spoken."""
        if pyttsx3 is None:
            return False

        tts = pyttsx3.init()
        for voice in tts.getProperty("voices"):
            voice_name = getattr(voice, "name", "").lower()
            voice_id = getattr(voice, "id", "").lower()
            if lang in voice_name or lang in voice_id:
                tts.setProperty("voice", voice.id)
                break
        tts.say(text)
        tts.runAndWait()
        return True


def build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NeuroLang emergency assistant")
    parser.add_argument("--input", required=True, help="Button text (e.g., FOOD, SOS)")
    parser.add_argument("--lang", default="en", help="Language code (en/hi/ta/te)")
    parser.add_argument(
        "--speak",
        action="store_true",
        help="Enable text-to-speech output when pyttsx3 is available",
    )
    return parser


def main() -> None:
    parser = build_cli()
    args = parser.parse_args()

    engine = NeuroLangEngine(default_lang=args.lang)
    result = engine.interpret(args.input, lang=args.lang)

    print(f"Intent: {result.intent}")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Localized text: {result.localized_text}")

    if args.speak:
        spoken = engine.speak(result.localized_text, lang=result.lang)
        if not spoken:
            print("TTS unavailable: install pyttsx3 for audio output.")


if __name__ == "__main__":
    main()
