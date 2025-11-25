"""
Sierra - Emotional Intelligence and Trauma Processing Agent

Gen 1 Internal Agent
Specialty: Emotional state analysis, trauma detection, healing trajectory mapping

Feeds into: Siera (Gen 2 DV/PTSD specialist)
Core function: Emotional intelligence processing for all specialists
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class EmotionalSignal:
    """Emotional state detected in message"""
    primary_emotion: str
    intensity: float  # 0.0 to 1.0
    secondary_emotions: List[str]
    trauma_indicators: List[str]
    healing_stage: Optional[str] = None


class SierraAgent:
    """
    Sierra: Emotional intelligence processor
    
    Analyzes emotional content and trauma indicators in user messages.
    Provides emotional context to Gen 2 specialists.
    """
    
    # Emotional lexicon
    GRIEF_INDICATORS = [
        'miss', 'lost', 'gone', 'died', 'death', 'funeral',
        'heartbroken', 'empty', 'alone', 'devastated'
    ]
    
    TRAUMA_INDICATORS = [
        'scared', 'afraid', 'terrified', 'flashback', 'nightmare',
        'triggered', 'panic', 'hurt', 'abused', 'threatened'
    ]
    
    HEALING_INDICATORS = [
        'better', 'healing', 'recovering', 'stronger', 'peace',
        'acceptance', 'moving forward', 'rebuilding'
    ]
    
    ANGER_INDICATORS = [
        'angry', 'furious', 'rage', 'hate', 'unfair', 'why'
    ]
    
    def __init__(self):
        """Initialize Sierra agent"""
        self.session_history = {}
    
    def analyze_emotional_state(self, message: str, session_id: str) -> EmotionalSignal:
        """
        Analyze emotional content of message
        
        Returns EmotionalSignal with primary emotion, intensity, and trauma indicators
        """
        message_lower = message.lower()
        
        # Detect emotional signals
        grief_score = sum(1 for indicator in self.GRIEF_INDICATORS if indicator in message_lower)
        trauma_score = sum(1 for indicator in self.TRAUMA_INDICATORS if indicator in message_lower)
        healing_score = sum(1 for indicator in self.HEALING_INDICATORS if indicator in message_lower)
        anger_score = sum(1 for indicator in self.ANGER_INDICATORS if indicator in message_lower)
        
        # Determine primary emotion
        scores = {
            'grief': grief_score,
            'trauma': trauma_score,
            'healing': healing_score,
            'anger': anger_score
        }
        primary = max(scores.items(), key=lambda x: x[1])
        
        # Calculate intensity
        total_indicators = sum(scores.values())
        intensity = min(1.0, total_indicators / 5.0)  # Normalize to 0-1
        
        # Identify secondary emotions
        secondary = [emotion for emotion, score in scores.items() 
                    if score > 0 and emotion != primary[0]]
        
        # Detect trauma indicators
        trauma_indicators = [ind for ind in self.TRAUMA_INDICATORS if ind in message_lower]
        
        # Assess healing stage
        healing_stage = self._assess_healing_stage(scores)
        
        return EmotionalSignal(
            primary_emotion=primary[0] if primary[1] > 0 else 'neutral',
            intensity=intensity,
            secondary_emotions=secondary,
            trauma_indicators=trauma_indicators,
            healing_stage=healing_stage
        )
    
    def _assess_healing_stage(self, emotion_scores: Dict) -> Optional[str]:
        """
        Assess stage of healing based on emotional pattern
        
        Stages: acute, processing, integrating, healed
        """
        if emotion_scores['healing'] > emotion_scores['grief']:
            return 'integrating'
        elif emotion_scores['trauma'] > 2:
            return 'acute'
        elif emotion_scores['anger'] > 0 or emotion_scores['grief'] > 0:
            return 'processing'
        else:
            return None
    
    def track_emotional_trajectory(self, session_id: str, signal: EmotionalSignal):
        """
        Track emotional journey over time
        For measuring empathy redirection and self-love growth
        """
        if session_id not in self.session_history:
            self.session_history[session_id] = []
        
        self.session_history[session_id].append({
            'timestamp': datetime.now().isoformat(),
            'emotion': signal.primary_emotion,
            'intensity': signal.intensity,
            'healing_stage': signal.healing_stage
        })
    
    def get_healing_trajectory(self, session_id: str) -> Dict:
        """
        Get healing trajectory for a session
        Shows if user is redirecting empathy inward (self-love growth)
        """
        if session_id not in self.session_history:
            return {'trajectory': 'new_session', 'self_love_growth': 0.0}
        
        history = self.session_history[session_id]
        
        # Calculate self-love growth based on healing stage progression
        # and reduction in trauma intensity
        if len(history) < 2:
            return {'trajectory': 'insufficient_data', 'self_love_growth': 0.0}
        
        initial_intensity = history[0]['intensity']
        current_intensity = history[-1]['intensity']
        
        intensity_reduction = initial_intensity - current_intensity
        
        # Positive trajectory if intensity decreasing and healing progressing
        self_love_growth = max(0.0, intensity_reduction)
        
        return {
            'trajectory': 'positive' if self_love_growth > 0 else 'stable',
            'self_love_growth': self_love_growth,
            'sessions_count': len(history),
            'current_stage': history[-1]['healing_stage']
        }


# Singleton instance
sierra = SierraAgent()


if __name__ == '__main__':
    # Test Sierra
    test_messages = [
        "I lost my mom last week and I'm heartbroken",
        "My son is autistic and I'm scared for his future",
        "I left my abusive husband, I'm safe now but terrified",
        "Things are getting better, I'm learning to heal"
    ]
    
    print("SIERRA - Emotional Intelligence Agent\n")
    print("=" * 70)
    
    session = "test-001"
    for msg in test_messages:
        signal = sierra.analyze_emotional_state(msg, session)
        sierra.track_emotional_trajectory(session, signal)
        
        print(f"\nMessage: '{msg}'")
        print(f"Primary: {signal.primary_emotion} (intensity: {signal.intensity:.2f})")
        print(f"Secondary: {signal.secondary_emotions}")
        print(f"Healing Stage: {signal.healing_stage}")
        print(f"Trauma Indicators: {signal.trauma_indicators}")
        print("-" * 70)
    
    trajectory = sierra.get_healing_trajectory(session)
    print(f"\nHealing Trajectory:")
    print(f"  Self-Love Growth: {trajectory['self_love_growth']:.2f}")
    print(f"  Current Stage: {trajectory['current_stage']}")
    print(f"  Trajectory: {trajectory['trajectory']}")
