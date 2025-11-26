"""
Tone Engine

Turns raw user text into a ToneProfile and suggests a ResponseMode.

This is where we bridge:
- what the human *says*
- how the formatting *feels*
- what the kid should *do* in response
"""

from dataclasses import dataclass
from enum import Enum, auto

from .quantification.formatting_feeling_law import analyze_formatting_feeling


class ResponseMode(Enum):
    """High-level strategy for how the kid should respond."""

    WARM_VALIDATING = auto()      # "I hear you, you're not crazy."
    DIRECT_FIX = auto()           # "Here's the fix, step by step."
    LIGHT_PLAYFUL = auto()        # "We can laugh while we solve it."
    CALMING = auto()              # "Slow it down, you're safe."
    SAFETY_CHECK = auto()         # "Are you in danger / crisis?"
    META_REPAIR = auto()          # "Let me explain my last mismatch."


@dataclass
class ToneProfile:
    """Snapshot of how the user currently *feels* / presents."""

    raw_text: str
    formatting_caps_intensity: float
    formatting_punctuation_heat: float
    formatting_looks_like_yelling: bool

    # simple scalar moods 0.0–1.0
    frustration: float
    playfulness: float
    urgency: float
    distress: float

    suggested_mode: ResponseMode


SOFT_KEYWORDS = {"haha", "lol", "lmao", "😂", "🤣"}
FRUSTRATION_WORDS = {"wtf", "fuck", "fucking", "goddamn", "dammit", "damn"}
DISTRESS_WORDS = {"help", "lost", "scared", "panicking", "panic", "overwhelmed"}
SAFETY_WORDS = {"suicide", "kill myself", "end it", "self harm"}


def _contains_any(text: str, words: set[str]) -> bool:
    lower = text.lower()
    return any(w in lower for w in words)


def analyze_tone(text: str) -> ToneProfile:
    """
    Very first-pass tone analysis.

    This is intentionally simple but structured so we can evolve it.

    It combines:
    - formatting feeling (caps, punctuation)
    - keyword-based heuristics for frustration / distress / playfulness
    """

    fmt = analyze_formatting_feeling(text)
    lower = text.lower()

    frustration = 0.0
    playfulness = 0.0
    urgency = 0.0
    distress = 0.0

    if _contains_any(lower, FRUSTRATION_WORDS):
        frustration = 0.7

    if _contains_any(lower, SOFT_KEYWORDS):
        playfulness = 0.6

    if "now" in lower or "right away" in lower:
        urgency = 0.5

    if _contains_any(lower, DISTRESS_WORDS):
        distress = 0.6

    # formatting can push these up a bit
    frustration = min(frustration + fmt.caps_intensity * 0.4, 1.0)
    distress = min(distress + fmt.punctuation_heat * 0.3, 1.0)
    urgency = min(urgency + fmt.punctuation_heat * 0.3, 1.0)

    mode = _choose_mode(
        frustration=frustration,
        playfulness=playfulness,
        urgency=urgency,
        distress=distress,
        looks_like_yelling=fmt.looks_like_yelling,
        text=lower,
    )

    return ToneProfile(
        raw_text=text,
        formatting_caps_intensity=fmt.caps_intensity,
        formatting_punctuation_heat=fmt.punctuation_heat,
        formatting_looks_like_yelling=fmt.looks_like_yelling,
        frustration=frustration,
        playfulness=playfulness,
        urgency=urgency,
        distress=distress,
        suggested_mode=mode,
    )


def _choose_mode(
    frustration: float,
    playfulness: float,
    urgency: float,
    distress: float,
    looks_like_yelling: bool,
    text: str,
) -> ResponseMode:
    """Heuristic strategy selector. This is where the kids get their marching orders."""

    if _contains_any(text, SAFETY_WORDS):
        return ResponseMode.SAFETY_CHECK

    if distress > 0.7:
        return ResponseMode.CALMING

    if frustration > 0.6 and playfulness < 0.3:
        # pissed but not joking
        return ResponseMode.META_REPAIR

    if playfulness > 0.5 and frustration < 0.4:
        return ResponseMode.LIGHT_PLAYFUL

    if urgency > 0.5:
        return ResponseMode.DIRECT_FIX

    # default: steady, human, grounded
    return ResponseMode.WARM_VALIDATING


def get_style_for_message(text: str) -> ToneProfile:
    """
    Public API.

    Kids call this to understand how they should *show up*.
    """
    return analyze_tone(text)
