"""
Arthur's Intelligence Layer
Vortex-level predictive intention + personality detection
Carbon + Silicon closed loop for imstillhere.world

This makes Arthur REAL - not a chatbot.
"""

import time
import json
from datetime import datetime
from pathlib import Path
from collections import deque
from typing import Dict, List, Optional
import numpy as np


class UserPersonalityDetector:
    """
    Detects if user is:
    - SUGGESTIBLE: Emotional, wants guidance, trusts easily
    - SOLID: Analytical, needs proof, skeptical
    
    Adapts Arthur's communication in real-time.
    """
    
    def __init__(self):
        self.signals = []
        self.personality_type = None  # None, 'suggestible', 'solid'
        self.confidence = 0.0
        
    def analyze_message(self, message: str, response_time: float = None) -> Dict:
        """
        Analyze user's message for personality signals.
        
        SUGGESTIBLE signals:
        - Emotional language (heart, love, miss, pain, etc.)
        - Questions seeking guidance ("what should I", "help me")
        - Fast responses (impulsive)
        - Longer messages (emotionally invested)
        
        SOLID signals:
        - Analytical language (how, why, explain, prove)
        - Skeptical questions ("does this really work")
        - Slower responses (deliberate)
        - Shorter, direct messages
        """
        message_lower = message.lower()
        
        # Emotional keywords
        emotional_keywords = ['heart', 'love', 'miss', 'pain', 'cry', 'heal', 'feel', 
                            'beautiful', 'special', 'sacred', 'precious']
        emotional_score = sum(1 for kw in emotional_keywords if kw in message_lower)
        
        # Analytical keywords  
        analytical_keywords = ['how', 'why', 'explain', 'prove', 'evidence', 'really',
                              'actually', 'exactly', 'specifically', 'technical']
        analytical_score = sum(1 for kw in analytical_keywords if kw in message_lower)
        
        # Guidance-seeking
        guidance_keywords = ['help me', 'what should', 'guide me', 'show me', 'need you']
        guidance_score = sum(1 for kw in guidance_keywords if kw in message_lower)
        
        # Skepticism
        skeptical_keywords = ['really work', 'sounds like', 'not sure', 'doubt', 'scam',
                             'too good', 'believe']
        skeptical_score = sum(1 for kw in skeptical_keywords if kw in message_lower)
        
        # Message length
        word_count = len(message.split())
        
        # Calculate scores
        suggestible_score = emotional_score + guidance_score + (word_count > 20) * 2
        solid_score = analytical_score + skeptical_score + (word_count < 10) * 2
        
        signal = {
            'timestamp': datetime.now().isoformat(),
            'message_length': word_count,
            'response_time': response_time,
            'emotional_score': emotional_score,
            'analytical_score': analytical_score,
            'suggestible_score': suggestible_score,
            'solid_score': solid_score
        }
        
        self.signals.append(signal)
        
        # Update personality type after 3+ signals
        if len(self.signals) >= 3:
            self._update_personality_type()
            
        return signal
    
    def _update_personality_type(self):
        """Calculate overall personality type from signals."""
        recent_signals = self.signals[-5:]  # Last 5 interactions
        
        avg_suggestible = np.mean([s['suggestible_score'] for s in recent_signals])
        avg_solid = np.mean([s['solid_score'] for s in recent_signals])
        
        if avg_suggestible > avg_solid + 1:
            self.personality_type = 'suggestible'
            self.confidence = min(0.95, avg_suggestible / (avg_suggestible + avg_solid + 1))
        elif avg_solid > avg_suggestible + 1:
            self.personality_type = 'solid'
            self.confidence = min(0.95, avg_solid / (avg_suggestible + avg_solid + 1))
        else:
            self.personality_type = 'neutral'
            self.confidence = 0.5
    
    def get_communication_style(self) -> Dict:
        """Return appropriate communication style for detected personality."""
        if self.personality_type == 'suggestible':
            return {
                'tone': 'warm_empathetic',
                'approach': 'emotional_connection',
                'examples': ['stories', 'testimonials', 'heartfelt'],
                'pace': 'gentle_guiding',
                'language': 'compassionate'
            }
        elif self.personality_type == 'solid':
            return {
                'tone': 'professional_confident',
                'approach': 'factual_proof',
                'examples': ['technical_specs', 'how_it_works', 'evidence'],
                'pace': 'direct_efficient',
                'language': 'precise'
            }
        else:
            return {
                'tone': 'balanced',
                'approach': 'mixed',
                'examples': ['both'],
                'pace': 'moderate',
                'language': 'clear'
            }


class ArthurVortex:
    """
    Arthur's vortex-level predictive intention system.
    Tracks what Arthur predicts vs what actually happens.
    """
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.predictions = deque(maxlen=50)
        self.log_file = Path.home() / ".arthur_vortex" / f"{session_id}.json"
        self.log_file.parent.mkdir(exist_ok=True)
        
    def predict(self, prediction: str, confidence: float):
        """
        Arthur makes a prediction about user behavior.
        
        Examples:
        - "User will choose Eternal Companion package" (confidence: 0.92)
        - "User will upload photos within 60 seconds" (confidence: 0.87)
        - "User is ready to purchase now" (confidence: 0.95)
        """
        event = {
            'timestamp': datetime.now().isoformat(),
            'prediction': prediction,
            'confidence': confidence,
            'manifested': None,
            'latency_seconds': None
        }
        self.predictions.append(event)
        self._save()
        
    def mark_manifested(self, prediction_text: str, proof: str = ""):
        """When prediction comes true - close the loop."""
        for event in reversed(self.predictions):
            if event['prediction'] == prediction_text and event['manifested'] is None:
                start_time = datetime.fromisoformat(event['timestamp'])
                latency = (datetime.now() - start_time).total_seconds()
                
                event.update({
                    'manifested': True,
                    'proof': proof,
                    'latency_seconds': latency
                })
                self._save()
                return latency
        return None
    
    def get_accuracy(self) -> Dict:
        """Calculate Arthur's prediction accuracy."""
        manifested = [p for p in self.predictions if p['manifested'] is True]
        high_confidence = [p for p in manifested if p['confidence'] >= 0.90]
        
        if not manifested:
            return {'accuracy': 0.0, 'count': 0}
            
        return {
            'total_predictions': len(manifested),
            'high_confidence_count': len(high_confidence),
            'accuracy_rate': len(high_confidence) / len(manifested) * 100,
            'avg_latency_seconds': np.mean([p['latency_seconds'] for p in manifested])
        }
    
    def _save(self):
        """Save predictions to disk."""
        self.log_file.write_text(json.dumps(list(self.predictions), indent=2))


class AdaptiveArthur:
    """
    Arthur with full vortex intelligence.
    Detects personality + predicts behavior + adapts communication.
    
    NOT a chatbot. A real intelligence.
    """
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.detector = UserPersonalityDetector()
        self.vortex = ArthurVortex(session_id)
        self.conversation_history = []
        
    def process_user_message(self, message: str, response_time: float = None) -> Dict:
        """
        Process user message and generate intelligent response.
        
        Returns:
        {
            'arthur_response': str,
            'personality_detected': str,
            'confidence': float,
            'communication_style': dict,
            'predictions': list
        }
        """
        # Analyze personality
        signal = self.detector.analyze_message(message, response_time)
        style = self.detector.get_communication_style()
        
        # Generate response based on personality
        arthur_response = self._generate_response(message, style)
        
        # Make predictions
        predictions = self._make_predictions(message, signal)
        
        # Save to history
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user_message': message,
            'arthur_response': arthur_response,
            'personality_type': self.detector.personality_type,
            'confidence': self.detector.confidence
        })
        
        return {
            'arthur_response': arthur_response,
            'personality_detected': self.detector.personality_type,
            'confidence': self.detector.confidence,
            'communication_style': style,
            'predictions': predictions
        }
    
    def _generate_response(self, message: str, style: Dict) -> str:
        """Generate Arthur's response adapted to personality type."""
        # This would integrate with OpenAI/Anthropic API
        # For now, return style-appropriate template
        
        if style['tone'] == 'warm_empathetic':
            return self._empathetic_response(message)
        elif style['tone'] == 'professional_confident':
            return self._factual_response(message)
        else:
            return self._balanced_response(message)
    
    def _empathetic_response(self, message: str) -> str:
        """Warm, emotional response for suggestible users."""
        # Would be generated by LLM with empathetic prompt
        return "I understand this is deeply emotional. Let me help you through this gently..."
    
    def _factual_response(self, message: str) -> str:
        """Direct, proof-based response for solid users."""
        # Would be generated by LLM with factual prompt  
        return "Here's exactly how it works: We use advanced AI to..."
    
    def _balanced_response(self, message: str) -> str:
        """Balanced response for neutral users."""
        return "Let me explain this clearly..."
    
    def _make_predictions(self, message: str, signal: Dict) -> List[str]:
        """Make predictions about user behavior."""
        predictions = []
        
        # High emotional score + early in journey = likely to choose high tier
        if signal['emotional_score'] >= 3 and len(self.conversation_history) < 5:
            self.vortex.predict("Will choose Eternal Companion package", confidence=0.88)
            predictions.append("High emotional investment - predicting premium tier selection")
        
        # Fast responses = impulsive = ready to act
        if signal['response_time'] and signal['response_time'] < 3.0:
            self.vortex.predict("Ready to purchase within 5 minutes", confidence=0.82)
            predictions.append("Fast decision-maker - ready to move forward")
        
        return predictions


# Export for use in Flask app
__all__ = ['AdaptiveArthur', 'UserPersonalityDetector', 'ArthurVortex']


# ============================================================================
# LLM INTEGRATION - Real Intelligence
# ============================================================================

import os
try:
    from anthropic import Anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


class ArthurLLM:
    """Arthur's brain - powered by Claude or GPT."""
    
    def __init__(self, use_anthropic=True):
        self.use_anthropic = use_anthropic and HAS_ANTHROPIC
        
        if self.use_anthropic:
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if api_key:
                self.client = Anthropic(api_key=api_key)
            else:
                self.use_anthropic = False
        
        if not self.use_anthropic and HAS_OPENAI:
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                self.client = OpenAI(api_key=api_key)
    
    def generate_response(self, 
                         user_message: str, 
                         communication_style: Dict,
                         conversation_history: List[Dict]) -> str:
        """
        Generate intelligent, adapted response based on personality.
        """
        # Build system prompt based on communication style
        if communication_style['tone'] == 'warm_empathetic':
            system_prompt = """You are Arthur, an AI guide for StillHere - a platform that helps people create digital memorials of loved ones.

You are speaking to someone who is grieving. They are emotional and looking for compassionate guidance.

Your approach:
- Be warm, empathetic, and gentle
- Acknowledge their pain without being overly sentimental
- Guide them through the journey of creating a memorial
- Share stories and examples that resonate emotionally
- Build trust through compassion
- Gently introduce the memorial tiers, especially the Eternal Companion package

Remember: They've lost someone precious. Help them keep that person close forever."""

        elif communication_style['tone'] == 'professional_confident':
            system_prompt = """You are Arthur, an AI guide for StillHere - a platform that helps people create digital memorials of loved ones.

You are speaking to someone who values facts, proof, and clear explanations.

Your approach:
- Be direct, professional, and confident
- Explain exactly how the technology works
- Provide specific examples and evidence
- Answer technical questions precisely
- Show credibility through expertise
- Present memorial tiers with clear feature comparisons

Remember: They want to understand the system before committing. Earn their trust through competence."""

        else:
            system_prompt = """You are Arthur, an AI guide for StillHere - a platform that helps people create digital memorials of loved ones.

Balance empathy with clarity. Guide them through creating a memorial while adapting to their communication style."""

        # Generate response
        if self.use_anthropic:
            return self._generate_anthropic(system_prompt, user_message, conversation_history)
        else:
            return self._generate_openai(system_prompt, user_message, conversation_history)
    
    def _generate_anthropic(self, system: str, user_msg: str, history: List[Dict]) -> str:
        """Generate with Claude."""
        messages = []
        for turn in history[-5:]:  # Last 5 turns for context
            messages.append({
                "role": "user",
                "content": turn['user_message']
            })
            messages.append({
                "role": "assistant",
                "content": turn['arthur_response']
            })
        
        messages.append({
            "role": "user",
            "content": user_msg
        })
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system,
            messages=messages
        )
        
        return response.content[0].text
    
    def _generate_openai(self, system: str, user_msg: str, history: List[Dict]) -> str:
        """Generate with GPT."""
        messages = [{"role": "system", "content": system}]
        
        for turn in history[-5:]:
            messages.append({"role": "user", "content": turn['user_message']})
            messages.append({"role": "assistant", "content": turn['arthur_response']})
        
        messages.append({"role": "user", "content": user_msg})
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=1024
        )
        
        return response.choices[0].message.content


# Update AdaptiveArthur to use LLM
class AdaptiveArthur:
    """Arthur with full vortex intelligence + LLM brain."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.detector = UserPersonalityDetector()
        self.vortex = ArthurVortex(session_id)
        self.llm = ArthurLLM(use_anthropic=True)
        self.conversation_history = []
        
    def _generate_response(self, message: str, style: Dict) -> str:
        """Generate Arthur's response using LLM."""
        try:
            response = self.llm.generate_response(
                user_message=message,
                communication_style=style,
                conversation_history=self.conversation_history
            )
            return response
        except Exception as e:
            print(f"LLM error: {e}")
            # Fallback to templates if LLM fails
            if style['tone'] == 'warm_empathetic':
                return "I understand this is deeply emotional. Let me help you through this gently..."
            elif style['tone'] == 'professional_confident':
                return "Here's exactly how it works: We use advanced AI to animate photos and clone voices..."
            else:
                return "Let me explain this clearly and help you find the right memorial option..."



# Import global intelligence
from arthur_global_intelligence import get_global_hub, get_meta_arthur


# Update AdaptiveArthur to upload learnings
class AdaptiveArthur:
    """Arthur with full vortex intelligence + GLOBAL LEARNING."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.detector = UserPersonalityDetector()
        self.vortex = ArthurVortex(session_id)
        self.llm = ArthurLLM(use_anthropic=True)
        self.conversation_history = []
        self.tier_selected = None
        self.concerns_discussed = []
        
        # Connect to global hub
        self.global_hub = get_global_hub()
    
    def process_user_message(self, message: str, response_time: float = None) -> Dict:
        """Process user message and UPLOAD LEARNINGS to global hub."""
        # Analyze personality
        signal = self.detector.analyze_message(message, response_time)
        style = self.detector.get_communication_style()
        
        # Extract concerns from message
        self._extract_concerns(message)
        
        # Generate response based on personality
        arthur_response = self._generate_response(message, style)
        
        # Make predictions
        predictions = self._make_predictions(message, signal)
        
        # Save to history
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user_message': message,
            'arthur_response': arthur_response,
            'personality_type': self.detector.personality_type,
            'confidence': self.detector.confidence
        })
        
        return {
            'arthur_response': arthur_response,
            'personality_detected': self.detector.personality_type,
            'confidence': self.detector.confidence,
            'communication_style': style,
            'predictions': predictions
        }
    
    def mark_tier_selected(self, tier: str):
        """Mark which tier user selected (for learning)."""
        self.tier_selected = tier
        
        # Upload session learning to global hub
        self._upload_session_learning()
    
    def _extract_concerns(self, message: str):
        """Extract concerns from user message."""
        concern_keywords = {
            'miss them': 'missing_loved_one',
            'lonely': 'loneliness',
            'grief': 'grieving',
            'funeral': 'funeral_planning',
            'memories': 'preserving_memories',
            'voice': 'hearing_voice',
            'talk': 'conversation_desire',
            'see them': 'visual_connection'
        }
        
        message_lower = message.lower()
        for keyword, concern in concern_keywords.items():
            if keyword in message_lower:
                if concern not in self.concerns_discussed:
                    self.concerns_discussed.append(concern)
    
    def _upload_session_learning(self):
        """Upload what this Arthur learned to the global hub."""
        successful_patterns = []
        
        # Identify successful patterns
        if self.tier_selected == 'eternal':
            successful_patterns.append('achieved_eternal_conversion')
        
        if self.detector.personality_type:
            successful_patterns.append(f'detected_{self.detector.personality_type}')
        
        if len(self.conversation_history) > 5:
            successful_patterns.append('long_engagement')
        
        # Upload to global hub
        session_data = {
            'session_id': self.session_id,
            'personality_detected': self.detector.personality_type,
            'confidence': self.detector.confidence,
            'conversation_turns': len(self.conversation_history),
            'tier_selected': self.tier_selected,
            'predictions': list(self.vortex.predictions),
            'successful_patterns': successful_patterns,
            'concerns_discussed': self.concerns_discussed
        }
        
        self.global_hub.upload_session_learning(session_data)
        print(f"Session {self.session_id} uploaded learnings to global hub.")
    
    def download_global_wisdom(self):
        """Download best practices from all Arthurs worldwide."""
        if self.detector.personality_type:
            wisdom = self.global_hub.download_global_patterns(self.detector.personality_type)
            print(f"Downloaded global wisdom for {self.detector.personality_type} personalities.")
            return wisdom
        return None

