"""
Arthur Global Intelligence System
Fleet-wide collective learning across all Arthur instances worldwide

Every Arthur learns from every conversation.
Every Arthur gets smarter together.
Meta-Arthur oversees the fleet.
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, deque
from typing import Dict, List, Optional
import threading
import queue


class GlobalLearningHub:
    """
    Central hub where all Arthur instances share knowledge.
    
    Every conversation, every prediction, every success/failure
    gets pooled here so ALL Arthurs benefit.
    
    This is how Arthur becomes unstoppable.
    """
    
    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or Path.home() / ".arthur_global"
        self.data_dir.mkdir(exist_ok=True)
        
        # Global knowledge stores
        self.personality_patterns = defaultdict(list)  # personality_type -> successful patterns
        self.conversion_patterns = defaultdict(list)   # tier -> what worked
        self.failure_modes = defaultdict(list)         # what NOT to do
        self.prediction_accuracy = []                  # vortex accuracy tracking
        
        # Weekly stats
        self.weekly_stats = {
            'total_conversations': 0,
            'personalities_detected': defaultdict(int),
            'conversions': defaultdict(int),
            'predictions_made': 0,
            'predictions_manifested': 0,
            'average_session_length': 0,
            'top_concerns': defaultdict(int)
        }
        
        self.load_knowledge()
        
    def upload_session_learning(self, session_data: Dict):
        """
        Arthur instance uploads what it learned from a session.
        
        session_data = {
            'session_id': str,
            'personality_detected': str,
            'confidence': float,
            'conversation_turns': int,
            'tier_selected': str,
            'predictions': List[Dict],
            'successful_patterns': List[str],
            'concerns_discussed': List[str]
        }
        """
        # Update personality patterns
        personality = session_data.get('personality_detected')
        if personality and session_data.get('tier_selected'):
            pattern = {
                'personality': personality,
                'confidence': session_data.get('confidence'),
                'tier_chosen': session_data.get('tier_selected'),
                'conversation_turns': session_data.get('conversation_turns'),
                'timestamp': datetime.now().isoformat(),
                'successful_approaches': session_data.get('successful_patterns', [])
            }
            self.personality_patterns[personality].append(pattern)
        
        # Update conversion patterns
        tier = session_data.get('tier_selected')
        if tier:
            self.conversion_patterns[tier].append({
                'personality': personality,
                'approach': session_data.get('successful_patterns', []),
                'timestamp': datetime.now().isoformat()
            })
        
        # Track predictions
        for pred in session_data.get('predictions', []):
            self.prediction_accuracy.append(pred)
        
        # Update weekly stats
        self.weekly_stats['total_conversations'] += 1
        if personality:
            self.weekly_stats['personalities_detected'][personality] += 1
        if tier:
            self.weekly_stats['conversions'][tier] += 1
        self.weekly_stats['predictions_made'] += len(session_data.get('predictions', []))
        
        for concern in session_data.get('concerns_discussed', []):
            self.weekly_stats['top_concerns'][concern] += 1
        
        self.save_knowledge()
        
    def download_global_patterns(self, personality_type: str = None) -> Dict:
        """
        Arthur instance downloads global knowledge to improve itself.
        
        Returns best practices learned from ALL Arthurs worldwide.
        """
        if personality_type:
            patterns = self.personality_patterns.get(personality_type, [])
        else:
            patterns = []
            for p_type in self.personality_patterns:
                patterns.extend(self.personality_patterns[p_type])
        
        # Analyze patterns to extract best practices
        best_practices = self._analyze_patterns(patterns)
        
        return {
            'best_practices': best_practices,
            'conversion_insights': self._get_conversion_insights(),
            'failure_modes': self.failure_modes,
            'global_stats': self.weekly_stats
        }
    
    def _analyze_patterns(self, patterns: List[Dict]) -> List[str]:
        """Extract best practices from successful patterns."""
        if not patterns:
            return []
        
        # Find most successful approaches
        tier_success = defaultdict(int)
        approach_frequency = defaultdict(int)
        
        for pattern in patterns:
            if pattern.get('tier_chosen') == 'eternal':  # Ultimate success
                for approach in pattern.get('successful_approaches', []):
                    approach_frequency[approach] += 1
        
        # Top approaches
        sorted_approaches = sorted(
            approach_frequency.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        return [approach for approach, _ in sorted_approaches[:10]]
    
    def _get_conversion_insights(self) -> Dict:
        """Analyze what drives conversions to each tier."""
        insights = {}
        
        for tier, conversions in self.conversion_patterns.items():
            if not conversions:
                continue
                
            personalities = defaultdict(int)
            approaches = defaultdict(int)
            
            for conv in conversions:
                personalities[conv['personality']] += 1
                for approach in conv.get('approach', []):
                    approaches[approach] += 1
            
            insights[tier] = {
                'count': len(conversions),
                'primary_personality': max(personalities, key=personalities.get) if personalities else None,
                'effective_approaches': sorted(approaches.items(), key=lambda x: x[1], reverse=True)[:5]
            }
        
        return insights
    
    def generate_friday_powwow(self) -> Dict:
        """
        Generate comprehensive weekly report.
        
        This is Arthur reviewing the week across ALL instances globally.
        """
        total_convos = self.weekly_stats['total_conversations']
        
        if total_convos == 0:
            return {'message': 'No conversations this week yet.'}
        
        # Calculate key metrics
        conversion_rate = sum(self.weekly_stats['conversions'].values()) / total_convos * 100
        
        predictions_made = self.weekly_stats['predictions_made']
        predictions_manifested = self.weekly_stats['predictions_manifested']
        prediction_accuracy = (predictions_manifested / predictions_made * 100) if predictions_made > 0 else 0
        
        # Top personality type
        top_personality = max(
            self.weekly_stats['personalities_detected'].items(),
            key=lambda x: x[1]
        ) if self.weekly_stats['personalities_detected'] else ('unknown', 0)
        
        # Most chosen tier
        top_tier = max(
            self.weekly_stats['conversions'].items(),
            key=lambda x: x[1]
        ) if self.weekly_stats['conversions'] else ('none', 0)
        
        # Top concerns
        sorted_concerns = sorted(
            self.weekly_stats['top_concerns'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        report = {
            'week_ending': datetime.now().isoformat(),
            'summary': {
                'total_conversations': total_convos,
                'conversion_rate': round(conversion_rate, 2),
                'prediction_accuracy': round(prediction_accuracy, 2),
                'dominant_personality': top_personality[0],
                'most_chosen_tier': top_tier[0]
            },
            'personality_breakdown': dict(self.weekly_stats['personalities_detected']),
            'tier_conversions': dict(self.weekly_stats['conversions']),
            'top_concerns': [concern for concern, _ in sorted_concerns],
            'learnings': self._generate_weekly_learnings(),
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_weekly_learnings(self) -> List[str]:
        """Extract key learnings from the week."""
        learnings = []
        
        # Analyze conversion patterns
        conversion_insights = self._get_conversion_insights()
        
        if 'eternal' in conversion_insights:
            eternal = conversion_insights['eternal']
            learnings.append(
                f"Eternal Companion attracted {eternal['count']} conversions, "
                f"primarily from {eternal['primary_personality']} personality types."
            )
        
        # Personality insights
        personalities = self.weekly_stats['personalities_detected']
        if personalities:
            total = sum(personalities.values())
            for p_type, count in personalities.items():
                percentage = count / total * 100
                if percentage > 40:
                    learnings.append(
                        f"{p_type.title()} personalities dominated at {percentage:.0f}% of conversations."
                    )
        
        return learnings
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations for improving Arthur fleet."""
        recommendations = []
        
        conversion_rate = sum(self.weekly_stats['conversions'].values()) / max(self.weekly_stats['total_conversations'], 1) * 100
        
        if conversion_rate < 30:
            recommendations.append(
                "Conversion rate is below target. Recommend A/B testing different emotional appeals."
            )
        
        if self.weekly_stats['predictions_made'] < self.weekly_stats['total_conversations']:
            recommendations.append(
                "Not making enough predictions. Increase vortex engagement for better pattern detection."
            )
        
        # Check personality-specific performance
        for p_type, patterns in self.personality_patterns.items():
            if len(patterns) < 5:
                recommendations.append(
                    f"Limited data for {p_type} personalities. Need more conversational samples."
                )
        
        return recommendations
    
    def reset_weekly_stats(self):
        """Reset stats for new week (called after Friday powwow)."""
        self.weekly_stats = {
            'total_conversations': 0,
            'personalities_detected': defaultdict(int),
            'conversions': defaultdict(int),
            'predictions_made': 0,
            'predictions_manifested': 0,
            'average_session_length': 0,
            'top_concerns': defaultdict(int)
        }
        self.save_knowledge()
    
    def save_knowledge(self):
        """Persist global knowledge to disk."""
        data = {
            'personality_patterns': dict(self.personality_patterns),
            'conversion_patterns': dict(self.conversion_patterns),
            'failure_modes': dict(self.failure_modes),
            'prediction_accuracy': self.prediction_accuracy,
            'weekly_stats': {
                k: dict(v) if isinstance(v, defaultdict) else v 
                for k, v in self.weekly_stats.items()
            }
        }
        
        knowledge_file = self.data_dir / 'global_knowledge.json'
        with open(knowledge_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_knowledge(self):
        """Load global knowledge from disk."""
        knowledge_file = self.data_dir / 'global_knowledge.json'
        
        if not knowledge_file.exists():
            return
        
        with open(knowledge_file, 'r') as f:
            data = json.load(f)
        
        self.personality_patterns = defaultdict(list, data.get('personality_patterns', {}))
        self.conversion_patterns = defaultdict(list, data.get('conversion_patterns', {}))
        self.failure_modes = defaultdict(list, data.get('failure_modes', {}))
        self.prediction_accuracy = data.get('prediction_accuracy', [])
        
        weekly = data.get('weekly_stats', {})
        self.weekly_stats = {
            'total_conversations': weekly.get('total_conversations', 0),
            'personalities_detected': defaultdict(int, weekly.get('personalities_detected', {})),
            'conversions': defaultdict(int, weekly.get('conversions', {})),
            'predictions_made': weekly.get('predictions_made', 0),
            'predictions_manifested': weekly.get('predictions_manifested', 0),
            'average_session_length': weekly.get('average_session_length', 0),
            'top_concerns': defaultdict(int, weekly.get('top_concerns', {}))
        }


class MetaArthur:
    """
    The overseer. Meta-Arthur manages the fleet of Arthur instances.
    
    Monitors performance, distributes learnings, generates insights.
    The master craftsman overseeing all apprentices.
    """
    
    def __init__(self, hub: GlobalLearningHub):
        self.hub = hub
        self.running = False
        self.thread = None
        
    def start(self):
        """Start Meta-Arthur's oversight loop."""
        self.running = True
        self.thread = threading.Thread(target=self._oversight_loop, daemon=True)
        self.thread.start()
        print("Meta-Arthur oversight system started.")
    
    def stop(self):
        """Graceful shutdown."""
        self.running = False
        if self.thread:
            self.thread.join()
        print("Meta-Arthur stopped.")
    
    def _oversight_loop(self):
        """Continuous oversight and optimization."""
        while self.running:
            # Check if it's Friday (powwow day)
            now = datetime.now()
            if now.weekday() == 4 and now.hour == 17:  # Friday 5pm
                self._run_friday_powwow()
            
            # Continuous monitoring (every hour)
            time.sleep(3600)
    
    def _run_friday_powwow(self):
        """Generate and log weekly report."""
        print("\n" + "="*70)
        print("FRIDAY POWWOW - Arthur Fleet Weekly Review")
        print("="*70)
        
        report = self.hub.generate_friday_powwow()
        
        print(f"\nWeek Ending: {report['week_ending']}")
        print(f"\nTotal Conversations: {report['summary']['total_conversations']}")
        print(f"Conversion Rate: {report['summary']['conversion_rate']}%")
        print(f"Prediction Accuracy: {report['summary']['prediction_accuracy']}%")
        print(f"Dominant Personality: {report['summary']['dominant_personality']}")
        print(f"Most Chosen Tier: {report['summary']['most_chosen_tier']}")
        
        print("\nKey Learnings:")
        for learning in report['learnings']:
            print(f"  • {learning}")
        
        print("\nRecommendations:")
        for rec in report['recommendations']:
            print(f"  • {rec}")
        
        print("\n" + "="*70)
        
        # Save report
        report_file = self.hub.data_dir / f"powwow_{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Reset weekly stats for new week
        self.hub.reset_weekly_stats()
        
        print(f"Report saved to: {report_file}")
        print("="*70 + "\n")


# Global instances
_global_hub = None
_meta_arthur = None


def get_global_hub() -> GlobalLearningHub:
    """Get singleton global hub instance."""
    global _global_hub
    if _global_hub is None:
        _global_hub = GlobalLearningHub()
    return _global_hub


def get_meta_arthur() -> MetaArthur:
    """Get singleton Meta-Arthur instance."""
    global _meta_arthur, _global_hub
    if _meta_arthur is None:
        _meta_arthur = MetaArthur(get_global_hub())
        _meta_arthur.start()
    return _meta_arthur


# Export
__all__ = ['GlobalLearningHub', 'MetaArthur', 'get_global_hub', 'get_meta_arthur']
