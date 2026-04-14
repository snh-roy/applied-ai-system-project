"""
Mental Health Knowledge Base for RAG System
"""

import json
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class MentalHealthResource:
    """Structure for mental health resources"""
    id: str
    title: str
    content: str
    category: str
    tags: List[str]
    source: str
    evidence_level: str  # "research-based", "expert-opinion", "community-wisdom"
    applicable_moods: List[str]
    applicable_triggers: List[str]
    effectiveness_rating: float
    metadata: Dict[str, Any]


class MentalHealthKnowledgeBase:
    """
    Knowledge base containing evidence-based mental health resources,
    coping strategies, and therapeutic techniques.
    """
    
    def __init__(self):
        self.resources = self._initialize_resources()
        self.coping_strategies = self._load_coping_strategies()
        self.crisis_resources = self._load_crisis_resources()
        self.therapeutic_techniques = self._load_therapeutic_techniques()
        
    def _initialize_resources(self) -> List[MentalHealthResource]:
        """Initialize built-in mental health resources"""
        resources = [
            MentalHealthResource(
                id="cbt_thought_challenging",
                title="CBT Thought Challenging",
                content="""Cognitive Behavioral Therapy (CBT) thought challenging helps identify and modify negative thought patterns:
                1. Identify the negative thought
                2. Examine evidence for and against
                3. Consider alternative perspectives
                4. Develop a balanced thought
                This technique is effective for anxiety and depression.""",
                category="therapeutic_technique",
                tags=["CBT", "cognitive", "anxiety", "depression"],
                source="Beck Institute for Cognitive Behavior Therapy",
                evidence_level="research-based",
                applicable_moods=["anxious", "sad", "worried"],
                applicable_triggers=["work", "relationship", "academic"],
                effectiveness_rating=0.85,
                metadata={"duration": "15-20 minutes", "difficulty": "moderate"}
            ),
            
            MentalHealthResource(
                id="breathing_478",
                title="4-7-8 Breathing Technique",
                content="""The 4-7-8 breathing technique helps calm the nervous system:
                1. Exhale completely
                2. Inhale through nose for 4 counts
                3. Hold breath for 7 counts
                4. Exhale through mouth for 8 counts
                Repeat 3-4 times. Effective for immediate anxiety relief.""",
                category="relaxation",
                tags=["breathing", "anxiety", "stress", "panic"],
                source="Dr. Andrew Weil",
                evidence_level="research-based",
                applicable_moods=["anxious", "stressed", "panicked"],
                applicable_triggers=["health", "work", "social"],
                effectiveness_rating=0.78,
                metadata={"duration": "5 minutes", "difficulty": "easy"}
            ),
            
            MentalHealthResource(
                id="progressive_muscle_relaxation",
                title="Progressive Muscle Relaxation",
                content="""PMR helps release physical tension associated with stress:
                1. Tense muscle group for 5 seconds
                2. Release and notice the relaxation for 15 seconds
                3. Move through body systematically (feet to head)
                Reduces physical symptoms of anxiety and improves sleep.""",
                category="relaxation",
                tags=["PMR", "relaxation", "stress", "sleep", "anxiety"],
                source="Edmund Jacobson Method",
                evidence_level="research-based",
                applicable_moods=["anxious", "stressed", "tense"],
                applicable_triggers=["health", "work", "academic"],
                effectiveness_rating=0.82,
                metadata={"duration": "15-20 minutes", "difficulty": "easy"}
            ),
            
            MentalHealthResource(
                id="mindfulness_body_scan",
                title="Mindfulness Body Scan",
                content="""Body scan meditation increases awareness and reduces stress:
                1. Lie down comfortably
                2. Focus attention on toes, notice sensations
                3. Gradually move awareness up through body
                4. Acknowledge feelings without judgment
                Helps with anxiety, depression, and chronic pain.""",
                category="mindfulness",
                tags=["meditation", "mindfulness", "stress", "awareness"],
                source="MBSR (Mindfulness-Based Stress Reduction)",
                evidence_level="research-based",
                applicable_moods=["anxious", "stressed", "sad", "overwhelmed"],
                applicable_triggers=["health", "work", "relationship"],
                effectiveness_rating=0.80,
                metadata={"duration": "20-45 minutes", "difficulty": "moderate"}
            ),
            
            MentalHealthResource(
                id="gratitude_practice",
                title="Three Good Things Exercise",
                content="""Daily gratitude practice improves mood and well-being:
                1. Each evening, write down 3 good things from your day
                2. Explain why each was meaningful
                3. Notice patterns over time
                Research shows this increases happiness and reduces depression.""",
                category="positive_psychology",
                tags=["gratitude", "positivity", "depression", "happiness"],
                source="Seligman et al., Positive Psychology",
                evidence_level="research-based",
                applicable_moods=["sad", "negative", "neutral"],
                applicable_triggers=["work", "relationship", "academic"],
                effectiveness_rating=0.75,
                metadata={"duration": "10 minutes", "difficulty": "easy"}
            ),
            
            MentalHealthResource(
                id="worry_time",
                title="Scheduled Worry Time",
                content="""Contain anxiety by scheduling specific worry periods:
                1. Set aside 15-30 minutes daily for worrying
                2. When worries arise, write them down for worry time
                3. During worry time, problem-solve or accept uncertainties
                4. Outside worry time, redirect to present moment
                Reduces overall anxiety and rumination.""",
                category="anxiety_management",
                tags=["anxiety", "worry", "rumination", "CBT"],
                source="Cognitive Behavioral Therapy",
                evidence_level="research-based",
                applicable_moods=["anxious", "worried", "overwhelmed"],
                applicable_triggers=["work", "financial", "academic", "health"],
                effectiveness_rating=0.73,
                metadata={"duration": "15-30 minutes daily", "difficulty": "moderate"}
            ),
            
            MentalHealthResource(
                id="behavioral_activation",
                title="Behavioral Activation for Depression",
                content="""Increase mood-boosting activities when depressed:
                1. Schedule pleasant activities even if unmotivated
                2. Start small (5-10 minute activities)
                3. Track mood before and after activities
                4. Gradually increase activity level
                Breaking the depression-inactivity cycle improves mood.""",
                category="depression_management",
                tags=["depression", "motivation", "activity", "mood"],
                source="Behavioral Activation Therapy",
                evidence_level="research-based",
                applicable_moods=["sad", "depressed", "unmotivated"],
                applicable_triggers=["health", "relationship", "work"],
                effectiveness_rating=0.81,
                metadata={"duration": "varies", "difficulty": "moderate"}
            ),
            
            MentalHealthResource(
                id="grounding_54321",
                title="5-4-3-2-1 Grounding Technique",
                content="""Ground yourself in the present during anxiety or panic:
                Name:
                - 5 things you can see
                - 4 things you can touch
                - 3 things you can hear
                - 2 things you can smell
                - 1 thing you can taste
                Interrupts anxiety spiral and returns focus to present.""",
                category="grounding",
                tags=["anxiety", "panic", "grounding", "mindfulness"],
                source="Trauma-Informed Care",
                evidence_level="expert-opinion",
                applicable_moods=["anxious", "panicked", "dissociated"],
                applicable_triggers=["social", "health", "trauma"],
                effectiveness_rating=0.76,
                metadata={"duration": "3-5 minutes", "difficulty": "easy"}
            ),
            
            MentalHealthResource(
                id="self_compassion_break",
                title="Self-Compassion Break",
                content="""Practice self-compassion during difficult moments:
                1. Acknowledge: 'This is a moment of suffering'
                2. Common humanity: 'Suffering is part of human experience'
                3. Self-kindness: 'May I be kind to myself'
                Reduces self-criticism and improves emotional resilience.""",
                category="self_compassion",
                tags=["self-compassion", "kindness", "resilience", "mindfulness"],
                source="Kristin Neff, Self-Compassion Research",
                evidence_level="research-based",
                applicable_moods=["sad", "guilty", "ashamed", "frustrated"],
                applicable_triggers=["relationship", "work", "academic"],
                effectiveness_rating=0.79,
                metadata={"duration": "5 minutes", "difficulty": "easy"}
            ),
            
            MentalHealthResource(
                id="exercise_mood_boost",
                title="Exercise for Mood Enhancement",
                content="""Physical activity is a powerful mood regulator:
                - 20-30 minutes of moderate exercise
                - Walking, jogging, yoga, or dancing
                - Releases endorphins and reduces stress hormones
                - As effective as medication for mild-moderate depression
                Start small and build consistency.""",
                category="lifestyle",
                tags=["exercise", "depression", "anxiety", "stress"],
                source="American Psychological Association",
                evidence_level="research-based",
                applicable_moods=["sad", "anxious", "stressed", "angry"],
                applicable_triggers=["health", "work", "relationship"],
                effectiveness_rating=0.83,
                metadata={"duration": "20-30 minutes", "difficulty": "moderate"}
            )
        ]
        
        return resources
        
    def _load_coping_strategies(self) -> Dict[str, List[str]]:
        """Load coping strategies mapped to emotional states"""
        return {
            "anxious": [
                "Practice deep breathing exercises",
                "Use grounding techniques (5-4-3-2-1)",
                "Try progressive muscle relaxation",
                "Take a mindful walk",
                "Write down worries and action steps",
                "Listen to calming music"
            ],
            "sad": [
                "Reach out to a supportive friend",
                "Engage in a pleasant activity",
                "Practice self-compassion",
                "Get some sunlight or light therapy",
                "Listen to uplifting music",
                "Watch something that makes you laugh"
            ],
            "angry": [
                "Take time to cool down before responding",
                "Use physical exercise to release energy",
                "Practice assertive communication",
                "Write in a journal",
                "Try progressive muscle relaxation",
                "Count to 10 slowly"
            ],
            "stressed": [
                "Break tasks into smaller steps",
                "Practice time management",
                "Set boundaries",
                "Take regular breaks",
                "Practice saying no",
                "Delegate when possible"
            ],
            "overwhelmed": [
                "Make a priority list",
                "Focus on one task at a time",
                "Practice the 2-minute rule",
                "Ask for help",
                "Take a mental health day",
                "Simplify your schedule"
            ],
            "lonely": [
                "Reach out to someone you trust",
                "Join a support group or club",
                "Volunteer in your community",
                "Practice self-compassion",
                "Engage in online communities",
                "Schedule regular social activities"
            ]
        }
        
    def _load_crisis_resources(self) -> Dict[str, Any]:
        """Load crisis intervention resources"""
        return {
            "hotlines": [
                {
                    "name": "National Suicide Prevention Lifeline",
                    "number": "988",
                    "availability": "24/7",
                    "description": "Free, confidential crisis support"
                },
                {
                    "name": "Crisis Text Line",
                    "number": "Text HOME to 741741",
                    "availability": "24/7",
                    "description": "Text-based crisis support"
                },
                {
                    "name": "SAMHSA National Helpline",
                    "number": "1-800-662-4357",
                    "availability": "24/7",
                    "description": "Treatment referral and information"
                }
            ],
            "immediate_steps": [
                "Ensure immediate safety",
                "Remove means of self-harm",
                "Stay with someone or call a friend",
                "Contact crisis hotline",
                "Go to nearest emergency room if in immediate danger"
            ],
            "safety_plan_template": {
                "warning_signs": "What thoughts, feelings, or behaviors indicate a crisis?",
                "coping_strategies": "What can you do on your own to feel better?",
                "social_contacts": "Who can you reach out to for distraction?",
                "support_contacts": "Who can you contact for help?",
                "professional_contacts": "What professionals can you contact?",
                "safe_environment": "How can you make your environment safer?"
            }
        }
        
    def _load_therapeutic_techniques(self) -> Dict[str, Any]:
        """Load therapeutic techniques and interventions"""
        return {
            "CBT": {
                "name": "Cognitive Behavioral Therapy",
                "techniques": [
                    "Thought challenging",
                    "Behavioral experiments",
                    "Activity scheduling",
                    "Problem-solving"
                ],
                "effective_for": ["depression", "anxiety", "panic", "OCD"]
            },
            "DBT": {
                "name": "Dialectical Behavior Therapy",
                "techniques": [
                    "Distress tolerance",
                    "Emotion regulation",
                    "Interpersonal effectiveness",
                    "Mindfulness"
                ],
                "effective_for": ["borderline personality", "self-harm", "emotional dysregulation"]
            },
            "ACT": {
                "name": "Acceptance and Commitment Therapy",
                "techniques": [
                    "Mindfulness",
                    "Values clarification",
                    "Committed action",
                    "Cognitive defusion"
                ],
                "effective_for": ["anxiety", "depression", "chronic pain", "stress"]
            },
            "MBCT": {
                "name": "Mindfulness-Based Cognitive Therapy",
                "techniques": [
                    "Mindfulness meditation",
                    "Body scan",
                    "Mindful movement",
                    "3-minute breathing space"
                ],
                "effective_for": ["depression relapse", "anxiety", "stress"]
            }
        }
        
    def get_resources_for_mood(self, mood: str, triggers: List[str] = None) -> List[MentalHealthResource]:
        """Get relevant resources for a specific mood and triggers"""
        relevant_resources = []
        
        for resource in self.resources:
            score = 0.0
            
            # Check mood applicability
            if mood in resource.applicable_moods:
                score += 0.5
                
            # Check trigger applicability
            if triggers:
                for trigger in triggers:
                    if trigger in resource.applicable_triggers:
                        score += 0.3
                        
            # Add effectiveness rating as a factor
            score *= resource.effectiveness_rating
            
            if score > 0:
                relevant_resources.append((resource, score))
                
        # Sort by relevance score
        relevant_resources.sort(key=lambda x: x[1], reverse=True)
        
        return [r[0] for r in relevant_resources[:5]]  # Return top 5 resources
        
    def get_coping_strategies(self, mood: str) -> List[str]:
        """Get coping strategies for a specific mood"""
        return self.coping_strategies.get(mood, [])
        
    def get_crisis_resources(self) -> Dict[str, Any]:
        """Get crisis intervention resources"""
        return self.crisis_resources
        
    def search_resources(self, query: str, category: str = None) -> List[MentalHealthResource]:
        """Search resources by query and optional category"""
        query_lower = query.lower()
        results = []
        
        for resource in self.resources:
            # Check category match if specified
            if category and resource.category != category:
                continue
                
            # Search in title, content, and tags
            if (query_lower in resource.title.lower() or
                query_lower in resource.content.lower() or
                any(query_lower in tag.lower() for tag in resource.tags)):
                results.append(resource)
                
        return results
        
    def get_technique_info(self, technique_type: str) -> Dict[str, Any]:
        """Get information about a therapeutic technique"""
        return self.therapeutic_techniques.get(technique_type, {})
        
    def add_resource(self, resource: MentalHealthResource) -> None:
        """Add a new resource to the knowledge base"""
        self.resources.append(resource)
        logger.info(f"Added resource: {resource.title}")
        
    def export_knowledge_base(self, filepath: str) -> None:
        """Export knowledge base to JSON file"""
        export_data = {
            "resources": [
                {
                    "id": r.id,
                    "title": r.title,
                    "content": r.content,
                    "category": r.category,
                    "tags": r.tags,
                    "source": r.source,
                    "evidence_level": r.evidence_level,
                    "applicable_moods": r.applicable_moods,
                    "applicable_triggers": r.applicable_triggers,
                    "effectiveness_rating": r.effectiveness_rating,
                    "metadata": r.metadata
                }
                for r in self.resources
            ],
            "coping_strategies": self.coping_strategies,
            "crisis_resources": self.crisis_resources,
            "therapeutic_techniques": self.therapeutic_techniques
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        logger.info(f"Knowledge base exported to {filepath}")