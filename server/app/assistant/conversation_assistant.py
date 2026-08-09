"""
Conversation Assistant for the Language Partner Chat feature.

This module implements the core logic for generating responses in
Conversation Mode as defined in LANG_PARTNER_SPEC.md.
"""

import random
import re
from typing import Dict

# Import existing services and utilities
from app.module.dictionary_module import dictionary

# Initialize shared resources using singleton instances
# Reuse the shared dictionary instance from dictionary_module
dictionary = dictionary  # Already a singleton from module import


class ConversationAssistant:
    """
    Core assistant class for Conversational Mode.

    Responsibilities:
    1. Initialize a random persona (name, location, situation)
    2. Process incoming speech/text to detect naturalness
    3. Generate appropriate response format (Output A or Output B)
    4. Provide furigana annotation and corrections when needed
    """

    # Persona components defined in the spec
    NAMES = ["Haru", "Aiko", "Kenji", "Yumi", "Sora", "Riku", "Mai", "Taro"]
    LOCATIONS = ["Osaka", "Fukuoka", "Hokkaido", "Kyoto", "Nagoya", "Okinawa"]
    SITUATIONS = [
        "staying up late watching anime",
        "just finished work at a cafe",
        "visiting a local shrine",
        "preparing for a weekend trip",
        "watching the sunset at the beach",
    ]

    def __init__(self, dictionary_instance=None):
        """Initialize the assistant with persona and shared services."""
        self.name = random.choice(self.NAMES)
        self.location = random.choice(self.LOCATIONS)
        self.situation = random.choice(self.SITUATIONS)
        # Use provided dictionary instance or fallback to the shared singleton
        self.dictionary = dictionary_instance if dictionary_instance else dictionary

        # Pre‑compile regex patterns for efficiency
        self.latin_pattern = re.compile(r"[A-Za-z]")

    # --------------------------------------------------------------------- #
    # Persona & Conversation State Helpers
    # --------------------------------------------------------------------- #
    @property
    def persona(self) -> Dict[str, str]:
        """Return the current persona details."""
        return {
            "name": self.name,
            "location": self.location,
            "situation": self.situation,
        }

    # --------------------------------------------------------------------- #
    # Naturalness & Content Checks
    # --------------------------------------------------------------------- #
    def is_natural_japanese(self, text: str) -> bool:
        """
        Heuristic check: text should consist primarily of Japanese characters
        (Kanji, Hiragana, Katakana) and minimal punctuation.
        Any Latin letters or numbers strongly indicate unnatural input.
        """
        # Remove whitespace for analysis
        cleaned = text.strip()
        if not cleaned:
            return False

        # If contains any ASCII letter or digit, treat as unnatural
        if self.latin_pattern.search(cleaned):
            return False

        # Optional: require at least one Hiragana/Katakana character
        # (helps filter out pure Kanji blocks which can be less natural)
        # Here we just allow pure Kanji as valid too.
        return True

    # --------------------------------------------------------------------- #
    # Response Generation
    # --------------------------------------------------------------------- #
    def generate_output_a(self, input_text: str) -> Dict[str, str]:
        """
        Output A - Natural input template.

        Format:
        [Output A - Natural]
        � ✅ [Name]: [Short, reactive statement with Kanji(reading)]

        Example:
        � ✅ Haru: もう�遅くまでアニメを見てたんですか？素�晴らしいですね！
        """
        # Simple reactive template based on situation
        reactive_templates = [
            "もう{}してたんですね？",
            "{}いいですね！",
            "それは楽しみですね！",
            "最近{}してますか？",
        ]

        # Pick template related to the persona's situation
        template = random.choice(reactive_templates).format(self.situation)
        # Add furigana using the dictionary helper
        furigana = self._add_furigana(template)
        return {
            "prefix": "��✅",
            "speaker": self.name,
            "content": f"{furigana}",
            "speak": template,
        }

    def generate_output_b(self, input_text: str) -> Dict[str, str]:
        """
        Output B - Unnatural input template.

        Format:
        �� 🛑 [Name]: (一時停止(いちじていし))

        Explanation and correction are provided separately.
        """
        stop_symbol = "���🛑"
        # Provide a generic stop indicator with furigana
        return {
            "prefix": stop_symbol,
            "speaker": self.name,
            "content": "(一時停止(いちじていし))",
            "explanation": "unnatural_phrase",
            "correction": self._correct_phrase(input_text),
        }

    # --------------------------------------------------------------------- #
    # Furigana & Correction Helpers
    # --------------------------------------------------------------------- #
    def _add_furigana(self, text: str) -> str:
        """
        Add furigana (reading) to Kanji characters using the dictionary service.
        This is a simplified wrapper; a full implementation would parse the
        entire sentence and annotate each Kanji.
        """

        # For demo purposes, just wrap each Kanji character with parentheses
        # containing its hiragana reading using the dictionary.
        def annotate_match(match):
            kanji = match.group(0)
            short_def = self.dictionary.short_lookup(kanji)
            reading = short_def.hiragana if short_def else ""
            return f"{kanji}({reading})"

        # Find all multi-byte characters that are likely Kanji (Unicode range)
        return re.sub(r"[一-��鿿]+", annotate_match, text)

    def _correct_phrase(self, input_text: str) -> str:
        """
        Generate a brief correction suggestion for unnatural input.
        This placeholder can be expanded with more sophisticated grammar checks.
        """
        # Very simple correction: repeat the input as a generic suggestion.
        # In a real system we would produce a more natural correction.
        return f"Perhaps you meant: “{input_text}。”"

    # --------------------------------------------------------------------- #
    # Public Interface
    # --------------------------------------------------------------------- #
    def process(self, raw_input: str) -> Dict[str, str]:
        """
        Main entry point called by the speech pipeline.

        Steps:
        1. (Optional) pass raw_input through STT if needed.
        2. Determine if the text is natural Japanese.
        3. Return the appropriate Output A or Output B payload.
        """
        # Step 1: Determine naturalness – in a real flow this could be
        # performed by an LLM or more advanced heuristic.
        if self.is_natural_japanese(raw_input):
            return self.generate_output_a(raw_input)
        else:
            return self.generate_output_b(raw_input)

    # --------------------------------------------------------------------- #
    # Utility / Debug
    # --------------------------------------------------------------------- #
    def debug_info(self) -> Dict[str, str]:
        """Return a quick summary for debugging or logging."""
        return {
            "name": self.name,
            "location": self.location,
            "situation": self.situation,
            "is_natural": self.is_natural_japanese("test"),
        }
