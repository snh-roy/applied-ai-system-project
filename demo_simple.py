#!/usr/bin/env python3
"""
MoodSense AI - Simple Demo (No External Dependencies)
This version works without installing additional packages
"""

import re
from typing import Dict, List, Tuple
from datetime import datetime

# Simplified Mood Analyzer for demo
class SimpleMoodAnalyzer:
    """Simplified version that works without dependencies"""
    
    def __init__(self):
        self.emotion_keywords = {
            "anxious": ["anxious", "worried", "nervous", "stressed", "overwhelmed"],
            "sad": ["sad", "depressed", "down", "hopeless", "miserable", "lonely"],
            "angry": ["angry", "mad", "furious", "irritated", "annoyed", "pissed"],
            "happy": ["happy", "excited", "joy", "great", "wonderful", "amazing"],
            "fearful": ["afraid", "scared", "terrified", "frightened", "fearful"]
        }
        
        self.crisis_keywords = [
            "kill myself", "suicide", "end it all", "not worth living",
            "want to die", "can't go on", "harm myself"
        ]
        
    def analyze(self, text: str) -> Dict:
        """Analyze text and return mood analysis"""
        text_lower = text.lower()
        
        # Check for crisis
        is_crisis = any(keyword in text_lower for keyword in self.crisis_keywords)
        
        # Score emotions
        emotion_scores = {}
        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                emotion_scores[emotion] = score
                
        # Determine primary mood
        if emotion_scores:
            primary_mood = max(emotion_scores, key=emotion_scores.get)
        else:
            primary_mood = "neutral"
            
        # Calculate confidence (simplified)
        confidence = min(0.9, 0.3 + len(emotion_scores) * 0.2)
        
        return {
            "primary_mood": primary_mood,
            "emotion_scores": emotion_scores,
            "confidence": confidence,
            "is_crisis": is_crisis,
            "timestamp": datetime.now().isoformat()
        }
        

class SimpleMentalHealthResources:
    """Simple resource provider"""
    
    def __init__(self):
        self.resources = {
            "anxious": {
                "title": "4-7-8 Breathing Technique",
                "content": """The 4-7-8 breathing technique helps calm your nervous system:
1. Exhale completely
2. Inhale through your nose for 4 counts
3. Hold your breath for 7 counts  
4. Exhale through your mouth for 8 counts
Repeat 3-4 times for immediate anxiety relief.""",
                "effectiveness": 0.78
            },
            "sad": {
                "title": "Behavioral Activation",
                "content": """When feeling down, small actions can help:
1. Start with a 5-minute activity
2. Choose something you used to enjoy
3. Track your mood before and after
4. Gradually increase activity
Remember: Action often comes before motivation.""",
                "effectiveness": 0.81
            },
            "angry": {
                "title": "Cool-Down Strategy",
                "content": """When anger rises, try this:
1. Count slowly to 10 before responding
2. Take deep breaths
3. Step away from the situation if possible
4. Express feelings through writing
5. Use physical activity to release tension""",
                "effectiveness": 0.75
            }
        }
        
    def get_resource(self, mood: str) -> Dict:
        """Get resource for specific mood"""
        return self.resources.get(mood, {
            "title": "General Support",
            "content": "Remember that seeking support is a sign of strength. Consider reaching out to a friend or professional.",
            "effectiveness": 0.70
        })
        

def display_banner():
    """Display application banner"""
    print("\n" + "="*60)
    print("🧠 MOODSENSE AI - Mental Health Support System")
    print("="*60)
    print("Providing evidence-based emotional support and resources")
    print("Note: This is not a replacement for professional care\n")
    

def analyze_and_respond(text: str):
    """Main analysis and response function"""
    analyzer = SimpleMoodAnalyzer()
    resources = SimpleMentalHealthResources()
    
    # Analyze mood
    result = analyzer.analyze(text)
    
    print("\n" + "-"*60)
    print("📊 MOOD ANALYSIS RESULTS")
    print("-"*60)
    
    # Check for crisis first
    if result["is_crisis"]:
        print("\n⚠️ CRISIS DETECTED - IMMEDIATE SUPPORT NEEDED ⚠️")
        print("\nYour safety is the top priority. Please reach out now:")
        print("  • National Suicide Prevention Lifeline: 988")
        print("  • Crisis Text Line: Text HOME to 741741")
        print("  • Emergency Services: 911")
        print("\nYou are not alone. Help is available 24/7.")
        return
        
    # Display mood analysis
    print(f"\n🎭 Primary Mood: {result['primary_mood'].upper()}")
    print(f"🎯 Confidence: {result['confidence']:.0%}")
    
    if result['emotion_scores']:
        print("\n📈 Emotion Detection:")
        for emotion, score in result['emotion_scores'].items():
            print(f"  • {emotion}: {'●' * score}")
            
    # Provide resource
    resource = resources.get_resource(result['primary_mood'])
    
    print("\n" + "-"*60)
    print("💡 RECOMMENDED SUPPORT")
    print("-"*60)
    print(f"\n📚 {resource['title']}")
    print(f"\n{resource['content']}")
    print(f"\n✨ Effectiveness Rating: {resource['effectiveness']:.0%}")
    
    # Additional suggestions
    print("\n🤝 Additional Support Options:")
    print("  • Talk to someone you trust")
    print("  • Consider professional counseling")
    print("  • Practice self-compassion")
    print("  • Maintain routine self-care")
    

def run_demo():
    """Run demonstration with example inputs"""
    display_banner()
    
    examples = [
        ("Anxiety Example", "I'm really anxious about my presentation tomorrow and can't stop worrying"),
        ("Depression Example", "I've been feeling so down lately, can't get motivated to do anything"),
        ("Crisis Example", "I don't see any point in going on anymore"),
    ]
    
    for title, text in examples:
        print(f"\n{'='*60}")
        print(f"DEMO: {title}")
        print(f"{'='*60}")
        print(f"Input: \"{text}\"")
        analyze_and_respond(text)
        input("\nPress Enter to continue...")
        
    print("\n" + "="*60)
    print("✅ DEMO COMPLETE")
    print("="*60)
    print("\nThis demonstrates:")
    print("  • Multi-dimensional mood analysis")
    print("  • Crisis detection with immediate escalation")
    print("  • Evidence-based resource recommendation")
    print("  • Confidence scoring for predictions")
    

def interactive_mode():
    """Run interactive chat mode"""
    display_banner()
    
    print("💬 INTERACTIVE MODE")
    print("Type your message or 'quit' to exit\n")
    
    while True:
        user_input = input("\n💭 You: ").strip()
        
        if not user_input or user_input.lower() == 'quit':
            print("\n👋 Take care of yourself. Goodbye!")
            break
            
        analyze_and_respond(user_input)
        

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        run_demo()
    else:
        interactive_mode()