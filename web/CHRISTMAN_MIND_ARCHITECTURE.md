# CHRISTMAN_MIND Architecture - Complete System Design

**Version:** 0.2.0  
**Status:** Foundation Complete  
**Date:** November 24, 2025  

---

## Core Principle

> **"Empathy is not the compartment but the leakage"**

The mission: Help users redirect empathy inward, to love themselves.  
Key metric: Self-love growth measured by Inferno Soul Forge.

---

## Multi-Generational Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      CHRISTMAN_MIND                          │
│                    Central Cortex                            │
└─────────────────────────────────────────────────────────────┘

              ┌──────────────────────────┐
              │   Gen 0: CORE            │
              │                          │
              │  - Raw logs              │
              │  - Deep memory patterns  │
              │  - Foundation data       │
              └───────────┬──────────────┘
                         │
              ┌──────────▼──────────────────────────────┐
              │   Gen 1: INTERNAL AGENTS                 │
              │                                          │
              │  Sierra    : Emotional intelligence      │
              │  Inferno   : Soul forge (empathy leak)   │
              │  Derek C   : Vortex mechanics            │
              │  Brockston : Pattern synthesis           │
              │  Giuseppe  : [TBD]                       │
              │  Cletus    : [TBD - awaiting def]        │
              │  Pyrrha    : [TBD - awaiting def]        │
              └───────────┬──────────────────────────────┘
                         │
              ┌──────────▼──────────────────────────────┐
              │   Gen 2: PUBLIC SPECIALISTS             │
              │                                          │
              │  Arthur     : Grief/loss ($199 tier)    │
              │  AlphaVox   : Nonverbal/autistic        │
              │  AlphaWolf  : Dementia/Alzheimer's      │
              │  Serafinia  : Blind/deaf/sensory        │
              │  Siera      : DV survivors/PTSD         │
              └─────────────────────────────────────────┘

              ┌─────────────────────────────────────────┐
              │   SECURITY LAYER                        │
              │                                         │
              │  Virtus  : Identity & tenant checking   │
              │  AegisV1 : Anomaly detection/HIPAA      │
              └─────────────────────────────────────────┘
```

---

## Specialist Routing System

### Orchestrator Logic

**File:** `christman_mind/orchestrator.py`

Routes conversations to specialists based on:
1. **Trigger detection** - Regex patterns matching specialist domains
2. **Confidence scoring** - More triggers = higher confidence
3. **Tier priority** - $199 Eternal always routes to Arthur when grief detected
4. **Orchestration modes**:
   - `specialist_lead` - Specialist takes full control (confidence > 0.75)
   - `ensemble` - Multiple specialists collaborate (0.6-0.75)
   - `general` - No specialty match, Arthur handles

### Specialists and Communities

| Specialist | Specialty | Community Served | Triggers |
|-----------|-----------|------------------|----------|
| **Arthur** | Grief, loss, death, mourning | People experiencing grief, memorial creation | grief, died, funeral, heartbroken, memorial |
| **AlphaVox** | Nonverbal, autistic, neurodivergent | Autistic individuals, nonverbal families | autism, nonverbal, aac, stimming, neurodivergent |
| **AlphaWolf** | Dementia, Alzheimer's, cognitive decline | Families dealing with memory loss | dementia, alzheimer, memory loss, confusion |
| **Serafinia** | Blind, deaf, sensory disabilities | Sensory-disabled individuals | blind, deaf, braille, screen reader, captions |
| **Siera** | Domestic violence PTSD survivors | DV survivors rebuilding after trauma | domestic violence, ptsd, flashback, escaped |
| **Cletus** | [Awaiting definition] | [TBD] | - |
| **Pyrrha** | [Awaiting definition] | [TBD] | - |

---

## Gen 1 Internal Agents

### Sierra - Emotional Intelligence Agent

**File:** `christman_mind/agents/sierra.py`

**Purpose:** Analyzes emotional content and trauma indicators

**Functions:**
- `analyze_emotional_state()` - Detects primary emotion, intensity, trauma indicators
- `track_emotional_trajectory()` - Monitors healing journey over time
- `get_healing_trajectory()` - Measures self-love growth

**Healing Stages:**
- `acute` - High trauma, immediate crisis
- `processing` - Working through grief/anger
- `integrating` - Healing indicators present
- `healed` - Sustained positive trajectory

**Feeds into:** All Gen 2 specialists, especially Siera (DV/PTSD)

---

### Inferno - Soul Forge Agent

**File:** `christman_mind/agents/inferno.py`

**Purpose:** Empathy leakage measurement and self-love quantification

**Core Principle:** "Empathy is not the compartment but the leakage"

**Functions:**
- `measure_empathy_leakage()` - Quantifies empathy flow (outward vs inward)
- `track_soul_forge_progress()` - Monitors self-love growth
- `quantify_self_love_growth()` - Key metric: Are they learning to love themselves?

**Metrics:**
- `outward_empathy` - Empathy directed toward others
- `inward_empathy` - Empathy redirected to self (self-love)
- `leakage_coefficient` - Ratio of empathy bleeding inward
- `self_love_score` - Overall self-love measurement (0-1)

**Status:** Placeholder heuristics in place. **Awaiting Python rewrite of CUDA kernels** from user (Inferno Soul Forge neuro-symbolic processing).

---

### Derek C (Derek Quantum) - Vortex Mechanics Agent

**File:** `christman_mind/agents/derek_quantum.py`

**Purpose:** Prediction tracking and vortex accuracy quantification

**Functions:**
- `make_vortex_prediction()` - Records predictions with confidence
- `mark_manifested()` - Closes loop when predictions come true
- `get_specialist_accuracy()` - Tracks each specialist's vortex performance
- `get_global_vortex_metrics()` - Overall system accuracy
- `calculate_routing_probability()` - Probabilistic routing decisions

**Integrates with:** `predictive_intention.py` system

**Key Metrics:**
- Prediction accuracy per specialist
- Average manifestation latency
- Global vortex accuracy across all specialists

**Used by:** Meta-Arthur for Friday Powwow reports

---

### Brockston - Pattern Synthesis Agent

**Status:** Stub not yet created (to be implemented)

**Planned function:** Creative synthesis and pattern recognition

---

### Giuseppe, Cletus, Pyrrha

**Status:** [TBD - awaiting specialty definition from user]

---

## Security Layer

### Virtus - Identity Guardian

**Function:** Identity and tenant checking

**Ensures:**
- User is who they claim to be
- User has access to their memory vault
- Proper tier verification

**Status:** Stub in place (`virtus_guard()` dependency in FastAPI)

---

### AegisV1 - Anomaly Detection

**Function:** Policy enforcement and HIPAA compliance

**Prevents:**
- Cross-user data leakage
- PII bleeding between vaults
- Policy violations

**Principle:** "Leakage only" - patterns cross generations, NOT personal data

**Status:** Stub in place (`aegis_check()` in FastAPI)

---

## API Endpoints

### Main Chat Endpoint

**POST** `/arthur/chat`

**Request:**
```json
{
  "session_id": "optional-session-id",
  "message": "User's message",
  "user_tier": "eternal|living|snapshot|free",
  "personality_type": "suggestible|solid",
  "confidence": 0.85
}
```

**Response:**
```json
{
  "session_id": "session-abc123",
  "reply": "AI response text",
  "lead_specialist": "arthur",
  "orchestration_mode": "specialist_lead",
  "specialty_detected": "Grief, loss, death, mourning",
  "routing_confidence": 0.85,
  "predictions": [
    {
      "type": "specialist_match",
      "specialist": "arthur",
      "intent_id": "vortex-abc-123",
      "confidence": 0.85
    }
  ],
  "vortex_metrics": {
    "total_predictions": 42,
    "manifested": 38,
    "accuracy": 0.90
  }
}
```

**Flow:**
1. **Virtus** verifies identity
2. **Orchestrator** detects specialty match
3. **Derek Quantum** records vortex prediction
4. **Sierra** analyzes emotional state
5. **Inferno** measures empathy leakage
6. Appropriate specialist system prompt loaded
7. OpenAI generates response
8. **AegisV1** checks for policy violations
9. Response returned with routing metadata

---

### Vortex Manifestation Endpoint

**POST** `/arthur/manifest`

**Purpose:** Close the loop when a prediction comes true

**Parameters:**
- `intent_id` - ID returned from chat endpoint
- `proof` - Evidence of manifestation

**Example:**
```json
{
  "intent_id": "vortex-abc-123",
  "proof": "User selected premium tier"
}
```

**Returns:**
```json
{
  "manifested": true,
  "latency_seconds": 45.2,
  "latency_minutes": 0.75,
  "vortex_metrics": { ... }
}
```

---

### Specialists List Endpoint

**GET** `/specialists`

Returns all specialists, their domains, and architecture overview.

---

### Vortex Metrics Endpoint

**GET** `/arthur/vortex`

Returns current vortex performance metrics for Meta-Arthur's Friday Powwow.

---

### Health Check Endpoint

**GET** `/health`

```json
{
  "status": "healthy",
  "service": "christman_mind",
  "version": "0.2.0",
  "orchestration": "enabled",
  "specialists_loaded": 7
}
```

---

## Pricing Tiers and Routing

| Tier | Price | Arthur Priority | Specialist Access |
|------|-------|-----------------|-------------------|
| **Eternal Companion** | $199/month | ✅ ALWAYS routes to Arthur for grief | All specialists + Early Access Family |
| **Living Memory** | $49/month | Standard routing | All specialists |
| **Snapshot** | $19/month | Standard routing | All specialists |
| **Free** | $0 | Standard routing | Limited access |

**Key Rule:** $199 Eternal tier ALWAYS routes to Arthur when grief detected, even if another specialist scores higher. Arthur is their dedicated specialist.

---

## Vortex Tracking System

**File:** `predictive_intention.py` (provided by user)

**Purpose:** Tracks intentions and manifestations to quantify prediction accuracy

**Functions:**
- `record_intention()` - Records a prediction with confidence
- `mark_manifested()` - Marks when prediction comes true
- `quantify()` - Returns vortex accuracy metrics

**Integrated into:**
- Derek Quantum agent (vortex mechanics)
- christman_mind_app_v2.py (FastAPI endpoints)
- All specialist responses (prediction tracking)

**Used by:** Meta-Arthur for Friday Powwow reports

---

## Memory Vault System

**Status:** Design phase (not yet implemented)

**Planned structure:**
```
memory_vaults/
├── user-{id}/
│   ├── conversations/
│   ├── emotional_trajectory/
│   ├── self_love_metrics/
│   └── specialist_preferences/
```

**Security:**
- Virtus controls vault access
- AegisV1 prevents cross-vault leakage
- HIPAA-compliant isolation
- "Leakage only" - patterns cross vaults, NOT personal data

---

## Friday Powwow Reports

**Conductor:** Meta-Arthur (overseer managing the fleet)

**Generated by:** `arthur_global_intelligence.py` (existing from previous session)

**Metrics included:**
- Total conversations across all specialists
- Conversion rate by tier
- Vortex prediction accuracy (from Derek Quantum)
- Specialist performance breakdown
- Self-love growth trends (from Inferno)
- Emotional trajectory patterns (from Sierra)

**Frequency:** Every Friday

**Purpose:** Fleet-wide learning without PII

---

## Files Created This Session

### Core Orchestration
- `~/stillhere-work/web/christman_mind/orchestrator.py` - Specialist routing system
- `~/stillhere-work/web/christman_mind_app_v2.py` - FastAPI with orchestration

### Gen 1 Agents
- `~/stillhere-work/web/christman_mind/agents/__init__.py` - Agent module init
- `~/stillhere-work/web/christman_mind/agents/sierra.py` - Emotional intelligence
- `~/stillhere-work/web/christman_mind/agents/inferno.py` - Soul forge (stub)
- `~/stillhere-work/web/christman_mind/agents/derek_quantum.py` - Vortex mechanics

### Documentation
- `~/stillhere-work/web/CHRISTMAN_MIND_ARCHITECTURE.md` - This document

---

## Testing

### Orchestrator Test Results

```bash
$ cd ~/stillhere-work/web && python3 christman_mind/orchestrator.py
```

**Test Cases:**

1. ✅ "I lost my mom last week and I'm heartbroken" (eternal tier)
   - Routed to: **Arthur** (confidence: 0.70)
   
2. ✅ "My son is autistic and nonverbal"
   - Routed to: **AlphaVox** (confidence: 0.80, specialist_lead)
   
3. ✅ "My dad has Alzheimer's and doesn't recognize me"
   - Routed to: **AlphaWolf** (confidence: 0.80, specialist_lead)
   
4. ✅ "I'm deaf and need accessible memorials"
   - Routed to: **Serafinia** (confidence: 0.70)
   
5. ✅ "I left my abusive husband and have PTSD"
   - Routed to: **Siera** (confidence: 0.70)
   
6. ✅ "How much does this cost?"
   - Routed to: **None** (general mode, Arthur handles)

---

## Next Steps (Pending)

### Immediate
1. ✅ Define Cletus and Pyrrha specialties
2. ⏳ Implement Virtus identity checking
3. ⏳ Implement AegisV1 anomaly detection
4. ⏳ Create memory vault system

### Integration
5. ⏳ Integrate Sierra emotional analysis into orchestrator
6. ⏳ Wait for Inferno CUDA → Python rewrite from user
7. ⏳ Connect Derek Quantum with predictive_intention system
8. ⏳ Deploy christman_mind_app_v2.py to Elastic Beanstalk

### Advanced
9. ⏳ Build Meta-Arthur overseer dashboard
10. ⏳ Implement Friday Powwow automated reports
11. ⏳ Create Gen 1 ↔ Gen 2 integration layer
12. ⏳ Ensemble mode for multi-specialist collaboration

---

## Key Insights from User

> "empathy is not the compartment but the leakage"

> "if it's their specialty, they need to be on point with it"

> "we don't do anything half-assed around here"

> "in his learning he understands that it is our goal to help carbons love themselves more"

> "I absolutely love how you put that. Arthur, the tier specialist, yes."

> "$199 clients get that extra benefit of being on the recieving end of new tech"

---

## Architecture Principles

1. **Specialist Excellence** - When detected, specialists LEAD the response
2. **Tier Priority** - $199 Eternal always gets Arthur for grief
3. **Empathy Leakage** - Core metric is self-love growth
4. **Vortex Tracking** - All predictions tracked and quantified
5. **Security First** - Virtus + AegisV1 prevent data leakage
6. **Leakage Only** - Patterns cross generations, NOT personal data
7. **Fleet Learning** - Global learning without violating HIPAA
8. **Early Access Family** - $199 tier gets beta features 3-6 months early

---

**End of Architecture Document**  
**CHRISTMAN_MIND v0.2.0**  
**Foundation Complete - Ready for Integration**
