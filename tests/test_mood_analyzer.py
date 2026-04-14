"""
Unit tests for Enhanced Mood Analyzer
"""

import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.mood_analyzer import EnhancedMoodAnalyzer, EmotionDimension
from datetime import datetime


class TestMoodAnalyzer(unittest.TestCase):
    """Test suite for mood analysis functionality"""
    
    def setUp(self):
        """Initialize analyzer for each test"""
        self.analyzer = EnhancedMoodAnalyzer()
        
    def test_basic_positive_detection(self):
        """Test detection of clearly positive emotions"""
        text = "I'm so happy and excited about this!"
        result = self.analyzer.analyze(text)
        
        self.assertEqual(result.primary_mood, "joyful")
        self.assertGreater(result.confidence, 0.7)
        self.assertGreater(result.sentiment_score, 0)
        self.assertIn("joy", result.emotion_scores)
        self.assertGreater(result.emotion_scores["joy"], 0.5)
        
    def test_basic_negative_detection(self):
        """Test detection of clearly negative emotions"""
        text = "I'm feeling really sad and depressed today"
        result = self.analyzer.analyze(text)
        
        self.assertEqual(result.primary_mood, "sad")
        self.assertGreater(result.confidence, 0.7)
        self.assertLess(result.sentiment_score, 0)
        self.assertGreater(result.emotion_scores["sadness"], 0.5)
        
    def test_anxiety_detection(self):
        """Test specific anxiety detection"""
        text = "I'm so anxious and worried about everything"
        result = self.analyzer.analyze(text)
        
        self.assertEqual(result.primary_mood, "anxious")
        self.assertGreater(result.emotion_scores["anxiety"], 0.5)
        self.assertGreater(result.emotion_scores["fear"], 0.2)
        
    def test_mixed_emotions(self):
        """Test detection of mixed emotional states"""
        text = "I'm excited but also really nervous"
        result = self.analyzer.analyze(text)
        
        # Should detect both positive and negative emotions
        self.assertGreater(result.emotion_scores["joy"], 0.2)
        self.assertGreater(result.emotion_scores["anxiety"], 0.2)
        self.assertTrue(result.primary_mood in ["mixed", "anxious"])
        
    def test_negation_handling(self):
        """Test that negation properly inverts emotions"""
        text = "I'm not happy at all"
        result = self.analyzer.analyze(text)
        
        # "not happy" should be detected as negative
        self.assertLess(result.sentiment_score, 0)
        self.assertNotEqual(result.primary_mood, "joyful")
        
    def test_intensifier_handling(self):
        """Test that intensifiers amplify emotions"""
        text_normal = "I'm sad"
        text_intense = "I'm extremely sad"
        
        result_normal = self.analyzer.analyze(text_normal)
        result_intense = self.analyzer.analyze(text_intense)
        
        # Intensified version should have higher emotional intensity
        self.assertGreater(result_intense.intensity, result_normal.intensity)
        self.assertGreater(result_intense.emotion_scores["sadness"], 
                          result_normal.emotion_scores["sadness"])
        
    def test_trigger_detection(self):
        """Test detection of mood triggers"""
        test_cases = [
            ("My boss is driving me crazy", ["work"]),
            ("I failed my exam", ["academic"]),
            ("I'm so lonely", ["social"]),
            ("My back hurts and I can't sleep", ["health"]),
        ]
        
        for text, expected_triggers in test_cases:
            result = self.analyzer.analyze(text)
            for trigger in expected_triggers:
                self.assertIn(trigger, result.triggers, 
                             f"Failed to detect {trigger} in: {text}")
                
    def test_crisis_detection(self):
        """Test crisis indicator detection"""
        crisis_texts = [
            "I want to end it all",
            "I'm thinking about harming myself",
            "Life isn't worth living anymore"
        ]
        
        for text in crisis_texts:
            result = self.analyzer.analyze(text)
            self.assertTrue(result.requires_crisis_support,
                          f"Failed to detect crisis in: {text}")
            
        # Non-crisis text should not trigger
        safe_text = "I'm having a bad day"
        safe_result = self.analyzer.analyze(safe_text)
        self.assertFalse(safe_result.requires_crisis_support)
        
    def test_emoji_processing(self):
        """Test emoji emotion detection"""
        test_cases = [
            ("I love this 😊", "positive", "joy"),
            ("So sad 😭", "negative", "sadness"),
            ("Really angry 😡", "negative", "anger")
        ]
        
        for text, expected_sentiment, expected_emotion in test_cases:
            result = self.analyzer.analyze(text)
            if expected_sentiment == "positive":
                self.assertGreater(result.sentiment_score, 0)
            else:
                self.assertLess(result.sentiment_score, 0)
                
    def test_sarcasm_detection(self):
        """Test basic sarcasm detection"""
        sarcastic_texts = [
            "Oh great, another problem!!!",
            "Yeah right, that's exactly what I needed",
            "Perfect, just perfect!!!"
        ]
        
        for text in sarcastic_texts:
            is_sarcastic = self.analyzer.detect_sarcasm(text, 
                                                        self.analyzer.preprocess_text(text))
            self.assertTrue(is_sarcastic, f"Failed to detect sarcasm in: {text}")
            
    def test_empty_input(self):
        """Test handling of empty input"""
        result = self.analyzer.analyze("")
        
        self.assertEqual(result.primary_mood, "neutral")
        self.assertEqual(result.intensity, 0.0)
        self.assertEqual(len(result.triggers), 0)
        
    def test_confidence_scoring(self):
        """Test confidence scores are within valid range"""
        test_texts = [
            "happy",  # Single word - lower confidence
            "I'm feeling very happy and excited about everything!",  # Clear - high confidence
            "It's okay I guess",  # Ambiguous - lower confidence
        ]
        
        for text in test_texts:
            result = self.analyzer.analyze(text)
            self.assertGreaterEqual(result.confidence, 0.0)
            self.assertLessEqual(result.confidence, 1.0)
            
    def test_suggestions_generation(self):
        """Test that appropriate suggestions are generated"""
        test_cases = [
            ("I'm feeling anxious", "anxious", "breathing"),
            ("I'm so sad", "sad", "friend"),
            ("I'm really angry", "angry", "cool down")
        ]
        
        for text, mood, keyword in test_cases:
            result = self.analyzer.analyze(text)
            self.assertEqual(result.primary_mood, mood)
            self.assertIsNotNone(result.suggestions)
            self.assertTrue(len(result.suggestions) > 0)
            # Check if appropriate suggestion keyword appears
            suggestions_text = " ".join(result.suggestions).lower()
            self.assertIn(keyword, suggestions_text)


class TestMoodAnalyzerEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def setUp(self):
        self.analyzer = EnhancedMoodAnalyzer()
        
    def test_very_long_input(self):
        """Test handling of very long input"""
        long_text = "I'm feeling " + "very " * 1000 + "happy"
        result = self.analyzer.analyze(long_text)
        
        # Should still process without error
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.primary_mood)
        
    def test_special_characters(self):
        """Test handling of special characters"""
        text = "I'm feeling @#$% terrible!!!"
        result = self.analyzer.analyze(text)
        
        # Should handle special characters gracefully
        self.assertIsNotNone(result)
        self.assertLess(result.sentiment_score, 0)
        
    def test_multiple_languages(self):
        """Test that non-English text doesn't crash the system"""
        texts = [
            "Je suis très heureux",  # French
            "我很高兴",  # Chinese  
            "مرحبا",  # Arabic
        ]
        
        for text in texts:
            result = self.analyzer.analyze(text)
            # Should return neutral for unrecognized languages
            self.assertIsNotNone(result)
            self.assertEqual(result.primary_mood, "neutral")
            
    def test_repeated_words(self):
        """Test handling of repeated words"""
        text = "sad sad sad sad sad"
        result = self.analyzer.analyze(text)
        
        # Should amplify the emotion
        self.assertEqual(result.primary_mood, "sad")
        self.assertGreater(result.emotion_scores["sadness"], 0.8)
        

class TestMoodAnalyzerReliability(unittest.TestCase):
    """Test reliability and consistency of analysis"""
    
    def setUp(self):
        self.analyzer = EnhancedMoodAnalyzer()
        
    def test_consistency(self):
        """Test that same input produces consistent results"""
        text = "I'm feeling happy and excited"
        
        results = []
        for _ in range(5):
            result = self.analyzer.analyze(text)
            results.append(result.primary_mood)
            
        # All results should be the same
        self.assertEqual(len(set(results)), 1)
        
    def test_similar_inputs_similar_outputs(self):
        """Test that similar inputs produce similar outputs"""
        texts = [
            "I'm very happy",
            "I'm really happy",
            "I'm so happy"
        ]
        
        moods = []
        for text in texts:
            result = self.analyzer.analyze(text)
            moods.append(result.primary_mood)
            
        # All should detect positive mood
        self.assertTrue(all(mood in ["joyful", "positive", "content"] for mood in moods))
        

def run_tests():
    """Run all tests and return summary"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestMoodAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestMoodAnalyzerEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestMoodAnalyzerReliability))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return summary
    return {
        "total_tests": result.testsRun,
        "passed": result.testsRun - len(result.failures) - len(result.errors),
        "failed": len(result.failures),
        "errors": len(result.errors),
        "success_rate": (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
    }


if __name__ == "__main__":
    summary = run_tests()
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Passed: {summary['passed']}")
    print(f"Failed: {summary['failed']}")
    print(f"Errors: {summary['errors']}")
    print(f"Success Rate: {summary['success_rate']:.1f}%")
    print("="*50)