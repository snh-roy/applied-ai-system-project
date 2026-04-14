"""
Enhanced Mood Analyzer with Multi-dimensional Emotion Detection
"""

import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import numpy as np
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)


class EmotionDimension(Enum):
    """Primary emotion dimensions based on psychological models"""
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    TRUST = "trust"
    DISGUST = "disgust"
    SURPRISE = "surprise"
    ANTICIPATION = "anticipation"
    ANXIETY = "anxiety"
    HOPE = "hope"
    GUILT = "guilt"
    SHAME = "shame"
    PRIDE = "pride"
    CONTENTMENT = "contentment"
    FRUSTRATION = "frustration"


@dataclass
class MoodAnalysisResult:
    """Comprehensive mood analysis result"""
    primary_mood: str
    emotion_scores: Dict[str, float]
    confidence: float
    triggers: List[str]
    intensity: float
    sentiment_score: float
    context: Dict[str, any]
    timestamp: datetime
    suggestions: List[str] = None
    requires_crisis_support: bool = False
    

class EnhancedMoodAnalyzer:
    """
    Advanced mood analyzer with multi-dimensional emotion detection,
    context understanding, and pattern recognition.
    """
    
    def __init__(self):
        self.emotion_lexicon = self._load_emotion_lexicon()
        self.negation_words = {
            "not", "no", "never", "n't", "don't", "can't", "won't", 
            "shouldn't", "wouldn't", "couldn't", "hardly", "barely", "scarcely"
        }
        self.intensifiers = {
            "very": 1.5, "really": 1.5, "extremely": 2.0, "absolutely": 2.0,
            "completely": 2.0, "totally": 1.8, "quite": 1.3, "fairly": 1.1,
            "somewhat": 0.8, "slightly": 0.7, "barely": 0.5, "hardly": 0.5
        }
        self.crisis_keywords = {
            "suicide", "kill myself", "end it all", "not worth living",
            "better off dead", "want to die", "can't go on", "no point",
            "harm myself", "self harm", "cutting", "overdose"
        }
        
    def _load_emotion_lexicon(self) -> Dict[str, Dict[str, float]]:
        """Load comprehensive emotion lexicon with word-emotion mappings"""
        return {
            # Joy/Positive emotions
            "happy": {EmotionDimension.JOY.value: 0.9, EmotionDimension.CONTENTMENT.value: 0.7},
            "excited": {EmotionDimension.JOY.value: 0.8, EmotionDimension.ANTICIPATION.value: 0.9},
            "love": {EmotionDimension.JOY.value: 0.9, EmotionDimension.TRUST.value: 0.8},
            "grateful": {EmotionDimension.JOY.value: 0.7, EmotionDimension.CONTENTMENT.value: 0.8},
            "proud": {EmotionDimension.PRIDE.value: 0.9, EmotionDimension.JOY.value: 0.6},
            "amazing": {EmotionDimension.JOY.value: 0.8, EmotionDimension.SURPRISE.value: 0.5},
            "wonderful": {EmotionDimension.JOY.value: 0.8, EmotionDimension.CONTENTMENT.value: 0.7},
            
            # Sadness emotions
            "sad": {EmotionDimension.SADNESS.value: 0.9},
            "depressed": {EmotionDimension.SADNESS.value: 0.95, EmotionDimension.HOPE.value: -0.8},
            "lonely": {EmotionDimension.SADNESS.value: 0.7, EmotionDimension.FEAR.value: 0.3},
            "disappointed": {EmotionDimension.SADNESS.value: 0.6, EmotionDimension.FRUSTRATION.value: 0.5},
            "heartbroken": {EmotionDimension.SADNESS.value: 0.9, EmotionDimension.ANGER.value: 0.2},
            "crying": {EmotionDimension.SADNESS.value: 0.8},
            "miserable": {EmotionDimension.SADNESS.value: 0.9, EmotionDimension.HOPE.value: -0.7},
            
            # Anger emotions  
            "angry": {EmotionDimension.ANGER.value: 0.9},
            "furious": {EmotionDimension.ANGER.value: 0.95},
            "irritated": {EmotionDimension.ANGER.value: 0.5, EmotionDimension.FRUSTRATION.value: 0.7},
            "frustrated": {EmotionDimension.FRUSTRATION.value: 0.9, EmotionDimension.ANGER.value: 0.4},
            "annoyed": {EmotionDimension.ANGER.value: 0.4, EmotionDimension.FRUSTRATION.value: 0.6},
            "pissed": {EmotionDimension.ANGER.value: 0.8},
            "rage": {EmotionDimension.ANGER.value: 1.0},
            
            # Fear/Anxiety emotions
            "afraid": {EmotionDimension.FEAR.value: 0.9},
            "scared": {EmotionDimension.FEAR.value: 0.8},
            "anxious": {EmotionDimension.ANXIETY.value: 0.9, EmotionDimension.FEAR.value: 0.5},
            "worried": {EmotionDimension.ANXIETY.value: 0.7, EmotionDimension.FEAR.value: 0.4},
            "nervous": {EmotionDimension.ANXIETY.value: 0.6, EmotionDimension.ANTICIPATION.value: 0.3},
            "terrified": {EmotionDimension.FEAR.value: 1.0},
            "stressed": {EmotionDimension.ANXIETY.value: 0.8, EmotionDimension.FRUSTRATION.value: 0.4},
            "overwhelmed": {EmotionDimension.ANXIETY.value: 0.8, EmotionDimension.FEAR.value: 0.3},
            
            # Mixed/Complex emotions
            "confused": {EmotionDimension.SURPRISE.value: 0.3, EmotionDimension.FRUSTRATION.value: 0.5},
            "hopeful": {EmotionDimension.HOPE.value: 0.9, EmotionDimension.ANTICIPATION.value: 0.6},
            "guilty": {EmotionDimension.GUILT.value: 0.9, EmotionDimension.SHAME.value: 0.4},
            "ashamed": {EmotionDimension.SHAME.value: 0.9, EmotionDimension.GUILT.value: 0.5},
            "jealous": {EmotionDimension.ANGER.value: 0.4, EmotionDimension.FEAR.value: 0.3, EmotionDimension.SADNESS.value: 0.3},
            "nostalgic": {EmotionDimension.SADNESS.value: 0.3, EmotionDimension.JOY.value: 0.4, EmotionDimension.CONTENTMENT.value: 0.3},
            
            # Emojis
            "😊": {EmotionDimension.JOY.value: 0.7, EmotionDimension.CONTENTMENT.value: 0.6},
            "😭": {EmotionDimension.SADNESS.value: 0.8},
            "😡": {EmotionDimension.ANGER.value: 0.8},
            "😨": {EmotionDimension.FEAR.value: 0.7},
            "🥺": {EmotionDimension.SADNESS.value: 0.5, EmotionDimension.HOPE.value: 0.3},
            "💔": {EmotionDimension.SADNESS.value: 0.9},
            "❤️": {EmotionDimension.JOY.value: 0.8, EmotionDimension.TRUST.value: 0.7},
            "😰": {EmotionDimension.ANXIETY.value: 0.7, EmotionDimension.FEAR.value: 0.5},
        }
        
    def preprocess_text(self, text: str) -> List[str]:
        """Advanced text preprocessing with emoji and punctuation handling"""
        # Convert to lowercase while preserving emojis
        text = text.strip()
        
        # Extract emojis separately
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE
        )
        
        emojis = emoji_pattern.findall(text)
        text_lower = text.lower()
        
        # Tokenize text while preserving contractions
        tokens = re.findall(r"\b[\w']+\b|[^\w\s]", text_lower, re.UNICODE)
        
        # Add emojis back to tokens
        tokens.extend(emojis)
        
        return tokens
        
    def detect_negation_scope(self, tokens: List[str], position: int) -> bool:
        """Determine if a word at position is negated"""
        # Check up to 3 words before for negation
        start = max(0, position - 3)
        for i in range(start, position):
            if tokens[i] in self.negation_words:
                return True
        return False
        
    def apply_intensifiers(self, tokens: List[str], position: int, score: float) -> float:
        """Apply intensifier effects to emotion scores"""
        if position > 0 and tokens[position - 1] in self.intensifiers:
            return score * self.intensifiers[tokens[position - 1]]
        return score
        
    def detect_sarcasm(self, text: str, tokens: List[str]) -> bool:
        """Basic sarcasm detection based on patterns"""
        sarcasm_indicators = [
            "yeah right", "sure", "oh great", "wonderful", "fantastic",
            "perfect", "just what i needed", "how lovely"
        ]
        
        text_lower = text.lower()
        
        # Check for sarcasm phrases
        for phrase in sarcasm_indicators:
            if phrase in text_lower:
                # Check context - if surrounded by negative words, likely sarcastic
                return True
                
        # Check for excessive punctuation (!!!, ???)
        if re.search(r'[!?]{3,}', text):
            return True
            
        return False
        
    def calculate_emotion_scores(self, tokens: List[str]) -> Dict[str, float]:
        """Calculate scores for each emotion dimension"""
        emotion_scores = {dim.value: 0.0 for dim in EmotionDimension}
        word_count = 0
        
        for i, token in enumerate(tokens):
            if token in self.emotion_lexicon:
                word_count += 1
                token_emotions = self.emotion_lexicon[token]
                
                for emotion, score in token_emotions.items():
                    # Apply intensifiers
                    modified_score = self.apply_intensifiers(tokens, i, score)
                    
                    # Handle negation
                    if self.detect_negation_scope(tokens, i):
                        # Negation reverses positive emotions to negative ones
                        if emotion in ["joy", "hope", "trust", "contentment"]:
                            emotion_scores["sadness"] += abs(modified_score) * 0.7
                            emotion_scores[emotion] -= abs(modified_score)
                        elif emotion in ["sadness", "anger", "fear"]:
                            emotion_scores["contentment"] += abs(modified_score) * 0.5
                            emotion_scores[emotion] -= abs(modified_score)
                    else:
                        emotion_scores[emotion] += modified_score
                        
        # Normalize scores
        if word_count > 0:
            for emotion in emotion_scores:
                emotion_scores[emotion] = emotion_scores[emotion] / word_count
                # Clamp between -1 and 1
                emotion_scores[emotion] = max(-1, min(1, emotion_scores[emotion]))
                
        return emotion_scores
        
    def detect_triggers(self, text: str) -> List[str]:
        """Identify potential mood triggers from text"""
        triggers = []
        trigger_patterns = {
            "work": r'\b(work|job|boss|deadline|meeting|project)\b',
            "relationship": r'\b(boyfriend|girlfriend|partner|spouse|family|friend)\b',
            "health": r'\b(sick|pain|tired|exhausted|sleep|insomnia)\b',
            "financial": r'\b(money|bills|debt|pay|rent|broke)\b',
            "academic": r'\b(exam|test|homework|grades|study|school|college)\b',
            "social": r'\b(alone|lonely|rejected|ignored|left out)\b'
        }
        
        text_lower = text.lower()
        for trigger_type, pattern in trigger_patterns.items():
            if re.search(pattern, text_lower):
                triggers.append(trigger_type)
                
        return triggers
        
    def check_crisis_indicators(self, text: str) -> bool:
        """Check for crisis keywords requiring immediate support"""
        text_lower = text.lower()
        for keyword in self.crisis_keywords:
            if keyword in text_lower:
                logger.warning(f"Crisis indicator detected: {keyword}")
                return True
        return False
        
    def determine_primary_mood(self, emotion_scores: Dict[str, float]) -> Tuple[str, float]:
        """Determine primary mood from emotion scores"""
        # Group emotions into mood categories
        mood_groups = {
            "positive": ["joy", "hope", "trust", "contentment", "pride", "anticipation"],
            "negative": ["sadness", "anger", "fear", "disgust", "guilt", "shame", "frustration"],
            "anxious": ["anxiety", "fear", "anticipation"],
            "mixed": []  # Will be determined by balanced scores
        }
        
        # Calculate mood group scores
        group_scores = {}
        for group, emotions in mood_groups.items():
            if group != "mixed":
                scores = [emotion_scores.get(e, 0) for e in emotions]
                group_scores[group] = np.mean(scores) if scores else 0
                
        # Determine if mixed
        pos_score = group_scores.get("positive", 0)
        neg_score = group_scores.get("negative", 0)
        
        if abs(pos_score - neg_score) < 0.2 and (pos_score > 0.2 or neg_score > 0.2):
            return "mixed", 0.5
            
        # Find dominant mood
        if group_scores:
            primary = max(group_scores, key=group_scores.get)
            confidence = abs(group_scores[primary])
            
            # Refine based on specific emotions
            if primary == "positive":
                if emotion_scores.get("joy", 0) > 0.5:
                    return "joyful", confidence
                elif emotion_scores.get("contentment", 0) > 0.5:
                    return "content", confidence
                elif emotion_scores.get("hope", 0) > 0.5:
                    return "hopeful", confidence
                else:
                    return "positive", confidence
                    
            elif primary == "negative":
                if emotion_scores.get("sadness", 0) > 0.5:
                    return "sad", confidence
                elif emotion_scores.get("anger", 0) > 0.5:
                    return "angry", confidence
                elif emotion_scores.get("frustration", 0) > 0.5:
                    return "frustrated", confidence
                else:
                    return "negative", confidence
                    
            elif primary == "anxious":
                return "anxious", confidence
                
        return "neutral", 0.3
        
    def calculate_intensity(self, emotion_scores: Dict[str, float]) -> float:
        """Calculate overall emotional intensity"""
        # Calculate magnitude of emotion vector
        values = list(emotion_scores.values())
        if values:
            intensity = np.sqrt(np.sum(np.square(values))) / len(values)
            return min(1.0, intensity)
        return 0.0
        
    def generate_suggestions(self, result: MoodAnalysisResult) -> List[str]:
        """Generate personalized coping suggestions based on mood analysis"""
        suggestions = []
        
        if result.primary_mood == "sad":
            suggestions.extend([
                "Consider reaching out to a friend or loved one",
                "Try a short walk in nature",
                "Practice gratitude by writing down three good things",
                "Listen to uplifting music"
            ])
        elif result.primary_mood == "anxious":
            suggestions.extend([
                "Try deep breathing exercises (4-7-8 technique)",
                "Practice progressive muscle relaxation",
                "Write down your worries and potential solutions",
                "Take a break from screens"
            ])
        elif result.primary_mood == "angry":
            suggestions.extend([
                "Take a few minutes to cool down before responding",
                "Try physical exercise to release tension",
                "Practice mindfulness meditation",
                "Write in a journal about your feelings"
            ])
        elif result.primary_mood == "frustrated":
            suggestions.extend([
                "Break down the problem into smaller, manageable parts",
                "Take a short break and return with fresh perspective",
                "Talk through the issue with someone you trust",
                "Practice self-compassion"
            ])
            
        # Add trigger-specific suggestions
        if "work" in result.triggers:
            suggestions.append("Consider setting clearer work-life boundaries")
        if "relationship" in result.triggers:
            suggestions.append("Open communication might help resolve conflicts")
        if "health" in result.triggers:
            suggestions.append("Prioritize rest and self-care")
            
        return suggestions[:4]  # Return top 4 suggestions
        
    def analyze(self, text: str, context: Optional[Dict] = None) -> MoodAnalysisResult:
        """
        Perform comprehensive mood analysis on text
        
        Args:
            text: Input text to analyze
            context: Optional context information (e.g., time of day, recent events)
            
        Returns:
            MoodAnalysisResult with detailed mood analysis
        """
        # Preprocess text
        tokens = self.preprocess_text(text)
        
        # Check for crisis indicators
        requires_crisis = self.check_crisis_indicators(text)
        
        # Detect sarcasm
        is_sarcastic = self.detect_sarcasm(text, tokens)
        
        # Calculate emotion scores
        emotion_scores = self.calculate_emotion_scores(tokens)
        
        # Adjust for sarcasm if detected
        if is_sarcastic:
            # Invert certain emotions for sarcasm
            for emotion in ["joy", "contentment", "trust"]:
                if emotion in emotion_scores:
                    emotion_scores[emotion] = -emotion_scores[emotion]
                    
        # Determine primary mood and confidence
        primary_mood, confidence = self.determine_primary_mood(emotion_scores)
        
        # Calculate intensity
        intensity = self.calculate_intensity(emotion_scores)
        
        # Calculate overall sentiment
        positive_emotions = ["joy", "hope", "trust", "contentment", "pride"]
        negative_emotions = ["sadness", "anger", "fear", "disgust", "guilt", "shame"]
        
        pos_score = sum(emotion_scores.get(e, 0) for e in positive_emotions)
        neg_score = sum(emotion_scores.get(e, 0) for e in negative_emotions)
        sentiment_score = (pos_score - neg_score) / (len(positive_emotions) + len(negative_emotions))
        
        # Detect triggers
        triggers = self.detect_triggers(text)
        
        # Create result
        result = MoodAnalysisResult(
            primary_mood=primary_mood,
            emotion_scores=emotion_scores,
            confidence=confidence,
            triggers=triggers,
            intensity=intensity,
            sentiment_score=sentiment_score,
            context=context or {},
            timestamp=datetime.now(),
            requires_crisis_support=requires_crisis
        )
        
        # Generate suggestions
        result.suggestions = self.generate_suggestions(result)
        
        return result
        
    def explain_analysis(self, result: MoodAnalysisResult) -> str:
        """Generate human-readable explanation of analysis"""
        explanation = f"Primary mood: {result.primary_mood} (confidence: {result.confidence:.2f})\n"
        explanation += f"Emotional intensity: {result.intensity:.2f}\n"
        explanation += f"Overall sentiment: {result.sentiment_score:.2f}\n\n"
        
        explanation += "Top emotions detected:\n"
        sorted_emotions = sorted(result.emotion_scores.items(), 
                               key=lambda x: abs(x[1]), reverse=True)[:5]
        for emotion, score in sorted_emotions:
            if abs(score) > 0.1:
                explanation += f"  - {emotion}: {score:.2f}\n"
                
        if result.triggers:
            explanation += f"\nPotential triggers: {', '.join(result.triggers)}\n"
            
        if result.requires_crisis_support:
            explanation += "\n⚠️ Crisis indicators detected - immediate support recommended\n"
            
        return explanation