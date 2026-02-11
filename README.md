# NeuroLang Emergency Voice Assistant

This repository contains a lightweight NLP-driven assistant that can be embedded in a button-based device ("Neurolang") to convert basic/emergency button text into spoken phrases in local or regional languages.

## What it does

- Accepts a button input label such as `FOOD`, `WATER`, `SOS`, `TOILET`, etc.
- Uses normalization and fuzzy intent matching to map the input to a known intent.
- Produces localized output text in the selected language.
- Optionally speaks the text using offline `pyttsx3` (if installed).
- Includes a CLI mode to simulate a hardware button press workflow.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python neurolang.py --input "water" --lang hi --speak
```

If `pyttsx3` is not installed, the app still works and prints output text.

## Example

```bash
python neurolang.py --input "sos" --lang ta
```

Output:

```text
Intent: SOS
Localized text: காப்பாற்றுங்கள்! அவசர உதவி தேவை.
```

## Integrating with a buttoned device

Your microcontroller/device software should send the button label to this script or module, e.g.:

- Button 1 -> `FOOD`
- Button 2 -> `WATER`
- Button 3 -> `TOILET`
- Emergency button -> `SOS`

Then call:

```python
from neurolang import NeuroLangEngine

engine = NeuroLangEngine(default_lang="en")
result = engine.interpret("SOS", lang="hi")
# result.intent -> "SOS"
# result.localized_text -> "कृपया बचाइए! आपातकालीन सहायता चाहिए।"
engine.speak(result.localized_text, lang="hi")
```

## Supported intents

- FOOD
- WATER
- SOS
- TOILET
- PAIN
- MEDICINE
- HELP
- YES
- NO

You can extend phrases and language outputs in `neurolang_data.py`.
