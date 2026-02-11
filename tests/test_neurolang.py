from neurolang import NeuroLangEngine


def test_exact_intent_match():
    engine = NeuroLangEngine()
    result = engine.interpret("WATER", lang="en")
    assert result.intent == "WATER"
    assert result.localized_text == "I need water, please."


def test_fuzzy_match_synonym_phrase():
    engine = NeuroLangEngine()
    result = engine.interpret("Need help now", lang="en")
    assert result.intent in {"HELP", "SOS"}


def test_unknown_when_low_confidence():
    engine = NeuroLangEngine(match_threshold=0.95)
    result = engine.interpret("zxqv", lang="en")
    assert result.intent == "UNKNOWN"


def test_language_fallback_to_english():
    engine = NeuroLangEngine(default_lang="xx")
    result = engine.interpret("food", lang="xx")
    assert result.lang == "en"
    assert result.localized_text == "I need food, please."
