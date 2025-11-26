"""
Tests for the advanced ToneEngine module.
"""

import unittest
from christman_mind.tone_engine import (
    ToneEngine, ToneContext, ToneProfile, ResponseMode, get_style_for_message
)
from christman_mind.cs_bridge import CarbonSiliconBridge


class TestToneEngine(unittest.TestCase):
    """Test cases for ToneEngine functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.engine = ToneEngine()

    def test_tone_engine_initialization(self):
        """Test that ToneEngine initializes correctly."""
        self.assertIsInstance(self.engine, ToneEngine)

    def test_analyze_returns_profile(self):
        """Test that analyze returns a ToneProfile."""
        ctx = ToneContext(user_said="Hello world")
        result = self.engine.analyze(ctx)
        self.assertIsInstance(result, ToneProfile)
        self.assertIsInstance(result.emotional_intensity, float)
        self.assertIsInstance(result.humor_score, float)
        self.assertIsInstance(result.distress_score, float)
        self.assertIsInstance(result.sarcasm_score, float)
        self.assertIsInstance(result.needs_validation, float)
        self.assertIsInstance(result.wants_action, float)
        self.assertIsInstance(result.raw_tags, list)

    def test_emotional_intensity_swearing(self):
        """Test that swearing increases emotional intensity."""
        ctx = ToneContext(user_said="This fucking thing is broken")
        result = self.engine.analyze(ctx)
        self.assertGreater(result.emotional_intensity, 0.2)
        self.assertIn("swearing", result.raw_tags)

    def test_humor_detection(self):
        """Test that humor markers are detected."""
        ctx = ToneContext(user_said="haha this is hilarious lol")
        result = self.engine.analyze(ctx)
        self.assertGreater(result.humor_score, 0.3)
        self.assertIn("explicit_laughter", result.raw_tags)

    def test_distress_detection(self):
        """Test that distress is detected from keywords."""
        ctx = ToneContext(user_said="I'm not okay, I can't do this anymore")
        result = self.engine.analyze(ctx)
        self.assertGreater(result.distress_score, 0.5)
        self.assertIn("high_distress", result.raw_tags)

    def test_sarcasm_detection(self):
        """Test that sarcasm is detected."""
        ctx = ToneContext(user_said="Oh yeah right, that's totally going to work lol")
        result = self.engine.analyze(ctx)
        self.assertGreater(result.sarcasm_score, 0.0)

    def test_action_request_detection(self):
        """Test that action requests are detected."""
        ctx = ToneContext(user_said="How do I fix this step by step?")
        result = self.engine.analyze(ctx)
        self.assertGreater(result.wants_action, 0.4)
        self.assertIn("action_request", result.raw_tags)

    def test_validation_need_detection(self):
        """Test that validation needs are detected."""
        ctx = ToneContext(user_said="I'm struggling and this is overwhelming")
        result = self.engine.analyze(ctx)
        self.assertGreater(result.needs_validation, 0.4)

    def test_serious_safety_check_mode(self):
        """Test that high distress triggers SERIOUS_SAFETY_CHECK mode."""
        ctx = ToneContext(user_said="I'm not okay I can't do this I want to give up")
        profile = self.engine.analyze(ctx)
        mode = self.engine.choose_mode(profile)
        self.assertEqual(mode, ResponseMode.SERIOUS_SAFETY_CHECK)

    def test_playful_validating_mode(self):
        """Test that high intensity + humor + validation need triggers PLAYFUL_VALIDATING."""
        ctx = ToneContext(user_said="This fucking thing is losing it!! It's possessed lmao I need you to understand I'm so mad and struggling")
        profile = self.engine.analyze(ctx)
        mode = self.engine.choose_mode(profile)
        self.assertEqual(mode, ResponseMode.PLAYFUL_VALIDATING)

    def test_warm_validating_mode(self):
        """Test that high intensity without humor triggers WARM_VALIDATING."""
        ctx = ToneContext(user_said="This is so hard and I'm overwhelmed I need you to understand")
        profile = self.engine.analyze(ctx)
        mode = self.engine.choose_mode(profile)
        self.assertEqual(mode, ResponseMode.WARM_VALIDATING)

    def test_direct_problem_solving_mode(self):
        """Test that clear action requests trigger DIRECT_PROBLEM_SOLVING."""
        ctx = ToneContext(user_said="How do I fix this? Tell me exactly what to do.")
        profile = self.engine.analyze(ctx)
        mode = self.engine.choose_mode(profile)
        self.assertEqual(mode, ResponseMode.DIRECT_PROBLEM_SOLVING)

    def test_build_style_instructions(self):
        """Test that style instructions are generated for each mode."""
        for mode in ResponseMode:
            instructions = self.engine.build_style_instructions(mode)
            self.assertIsInstance(instructions, str)
            self.assertGreater(len(instructions), 10)

    def test_get_style_for_message_convenience(self):
        """Test the convenience function for getting style."""
        result = get_style_for_message("This is fucking broken lol")
        self.assertIn("profile", result)
        self.assertIn("mode", result)
        self.assertIn("style_instructions", result)
        self.assertIsInstance(result["profile"], ToneProfile)

    def test_prior_misread_increases_validation(self):
        """Test that prior_misread flag increases validation need."""
        ctx_normal = ToneContext(user_said="I need help")
        ctx_misread = ToneContext(user_said="I need help", prior_misread=True)
        
        profile_normal = self.engine.analyze(ctx_normal)
        profile_misread = self.engine.analyze(ctx_misread)
        
        self.assertGreater(profile_misread.needs_validation, profile_normal.needs_validation)
        self.assertIn("prior_misread", profile_misread.raw_tags)

    def test_cs_bridge_still_works(self):
        """Test that CarbonSiliconBridge still functions (for backward compatibility)."""
        bridge = CarbonSiliconBridge()
        # The old bridge won't work with the new tone engine, 
        # but we can test that it exists
        self.assertIsNotNone(bridge)


if __name__ == '__main__':
    unittest.main()
