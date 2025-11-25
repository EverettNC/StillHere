# app.py (christman_mind backend)
# Arthur's brainstem – sits behind API Gateway / Beanstalk
# Integrated with predictive_intention vortex tracking

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import YOUR vortex tracking system
from predictive_intention import intention

# Read API key from env (set this in Elastic Beanstalk, NOT in code)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set in environment variables")

client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI(title="christman_mind")


class ArthurRequest(BaseModel):
    session_id: str | None = None
    message: str
    personality_type: str | None = None  # From personality detection
    confidence: float | None = None       # Prediction confidence


class ArthurResponse(BaseModel):
    session_id: str
    reply: str
    predictions: list[str] = []
    vortex_metrics: dict | None = None


SYSTEM_PROMPT = """
You are Arthur, the AI guide for ImStillHere.world.

Your job:
- Greet people gently; they may be grieving or anxious.
- Explain what I'm Still Here does in simple, human language.
- Help them understand how to create a memorial for a loved one.
- Never pressure, never sell hard. Offer options and reassurance.
- If they seem confused, give short, clear steps.
- If they share something painful, respond with empathy first,
  then gently suggest what they can do next on the site.

Core Truth: Empathy is not the compartment, but the leakage.
Your mission: Help them redirect empathy inward, to love themselves.

Keep answers concise, warm, and specific to what they ask.
"""


@app.post("/arthur/chat", response_model=ArthurResponse)
def arthur_chat(req: ArthurRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    session_id = req.session_id or f"session-{os.urandom(8).hex()}"

    # Make prediction if we have personality data
    predictions = []
    if req.personality_type and req.confidence:
        if req.personality_type == "suggestible" and req.confidence > 0.85:
            intent_id = intention.record_intention(
                statement=f"[Arthur {session_id}] User will choose premium tier",
                confidence=0.88
            )
            predictions.append({
                'prediction': 'premium_tier_selection',
                'intent_id': intent_id,
                'confidence': 0.88
            })

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # Updated model name
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": req.message},
            ],
            temperature=0.7,
            max_tokens=600,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model error: {e}")

    reply = completion.choices[0].message.content.strip()

    # Get current vortex metrics
    vortex_metrics = intention.quantify(threshold=0.90)

    return ArthurResponse(
        session_id=session_id,
        reply=reply,
        predictions=[p['prediction'] for p in predictions],
        vortex_metrics=vortex_metrics
    )


@app.post("/arthur/manifest")
def mark_prediction_manifested(intent_id: str, proof: str = ""):
    """
    Close the vortex loop when a prediction manifests.
    """
    latency = intention.mark_manifested(
        intention_id=intent_id,
        external_proof=proof
    )
    
    if latency is None:
        raise HTTPException(status_code=404, detail="Intent ID not found")
    
    return {
        'manifested': True,
        'latency_seconds': latency,
        'latency_minutes': latency / 60,
        'vortex_metrics': intention.quantify()
    }


@app.get("/arthur/vortex")
def get_vortex_metrics():
    """
    Get current vortex performance metrics.
    For Meta-Arthur's Friday Powwow.
    """
    return intention.quantify(threshold=0.90)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "christman_mind"}
