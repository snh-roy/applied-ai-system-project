"""
Autonomous Support Agent for Mental Health Interventions
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json

logger = logging.getLogger(__name__)


class ActionType(Enum):
    """Types of actions the agent can take"""
    ANALYZE_MOOD = "analyze_mood"
    RETRIEVE_RESOURCES = "retrieve_resources"
    PROVIDE_TECHNIQUE = "provide_technique"
    SUGGEST_ACTIVITY = "suggest_activity"
    CHECK_IN = "check_in"
    ESCALATE = "escalate"
    JOURNAL_PROMPT = "journal_prompt"
    TRACK_PROGRESS = "track_progress"
    SET_REMINDER = "set_reminder"
    OFFER_REFLECTION = "offer_reflection"


class InterventionStage(Enum):
    """Stages of intervention process"""
    ASSESSMENT = "assessment"
    PLANNING = "planning"
    INTERVENTION = "intervention"
    MONITORING = "monitoring"
    REFLECTION = "reflection"
    FOLLOW_UP = "follow_up"


@dataclass
class AgentAction:
    """Represents a single action taken by the agent"""
    action_type: ActionType
    parameters: Dict[str, Any]
    rationale: str
    timestamp: datetime
    expected_outcome: str
    priority: int = 1  # 1 (highest) to 5 (lowest)
    completed: bool = False
    result: Optional[Any] = None
    effectiveness: Optional[float] = None


@dataclass
class InterventionPlan:
    """Complete intervention plan for a user"""
    user_id: str
    mood_state: Dict[str, Any]
    goals: List[str]
    actions: List[AgentAction]
    stage: InterventionStage
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    success_metrics: Dict[str, float] = field(default_factory=dict)


class SupportAgent:
    """
    Autonomous agent that plans, executes, and monitors mental health
    support interventions. Implements a complete agentic workflow with
    planning, action, and reflection capabilities.
    """
    
    def __init__(self, mood_analyzer, rag_system, database=None):
        self.mood_analyzer = mood_analyzer
        self.rag_system = rag_system
        self.database = database
        self.active_plans: Dict[str, InterventionPlan] = {}
        self.action_history: List[AgentAction] = []
        
    def create_intervention_plan(
        self,
        user_id: str,
        user_input: str,
        context: Optional[Dict[str, Any]] = None
    ) -> InterventionPlan:
        """
        Create a comprehensive intervention plan based on user's state
        
        Args:
            user_id: Unique user identifier
            user_input: User's message or journal entry
            context: Additional context (history, preferences, etc.)
            
        Returns:
            Complete intervention plan
        """
        # Step 1: Assess current state
        mood_analysis = self.mood_analyzer.analyze(user_input, context)
        
        # Step 2: Determine intervention goals
        goals = self._determine_goals(mood_analysis, context)
        
        # Step 3: Plan actions
        actions = self._plan_actions(mood_analysis, goals, context)
        
        # Step 4: Create plan
        plan = InterventionPlan(
            user_id=user_id,
            mood_state={
                "primary_mood": mood_analysis.primary_mood,
                "intensity": mood_analysis.intensity,
                "triggers": mood_analysis.triggers,
                "requires_crisis_support": mood_analysis.requires_crisis_support
            },
            goals=goals,
            actions=actions,
            stage=InterventionStage.ASSESSMENT,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata=context or {}
        )
        
        # Store plan
        self.active_plans[user_id] = plan
        
        logger.info(f"Created intervention plan for user {user_id} with {len(actions)} actions")
        
        return plan
        
    def _determine_goals(
        self,
        mood_analysis: Any,
        context: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """Determine intervention goals based on mood analysis"""
        goals = []
        
        # Crisis intervention takes priority
        if mood_analysis.requires_crisis_support:
            goals.append("Ensure immediate safety and provide crisis resources")
            goals.append("Connect with professional support")
            return goals
            
        # Based on primary mood
        mood_goals = {
            "sad": [
                "Improve mood through behavioral activation",
                "Increase social connection",
                "Identify and challenge negative thoughts"
            ],
            "anxious": [
                "Reduce anxiety through relaxation techniques",
                "Develop coping strategies for worry",
                "Practice grounding and mindfulness"
            ],
            "angry": [
                "Manage anger through healthy expression",
                "Identify triggers and early warning signs",
                "Develop conflict resolution skills"
            ],
            "stressed": [
                "Reduce stress through time management",
                "Build resilience and coping skills",
                "Establish work-life balance"
            ],
            "overwhelmed": [
                "Break down tasks into manageable steps",
                "Prioritize self-care activities",
                "Build support network"
            ]
        }
        
        primary_mood = mood_analysis.primary_mood
        if primary_mood in mood_goals:
            goals.extend(mood_goals[primary_mood])
            
        # Add intensity-based goals
        if mood_analysis.intensity > 0.7:
            goals.append("Provide immediate coping strategies")
            goals.append("Monitor for escalation")
            
        # Add trigger-specific goals
        if "work" in mood_analysis.triggers:
            goals.append("Develop workplace stress management strategies")
        if "relationship" in mood_analysis.triggers:
            goals.append("Improve communication and relationship skills")
            
        return goals[:3]  # Limit to top 3 goals for focus
        
    def _plan_actions(
        self,
        mood_analysis: Any,
        goals: List[str],
        context: Optional[Dict[str, Any]] = None
    ) -> List[AgentAction]:
        """Plan specific actions to achieve intervention goals"""
        actions = []
        
        # Always start with mood analysis
        actions.append(AgentAction(
            action_type=ActionType.ANALYZE_MOOD,
            parameters={"detailed": True},
            rationale="Establish baseline emotional state",
            timestamp=datetime.now(),
            expected_outcome="Clear understanding of user's emotional state",
            priority=1
        ))
        
        # Crisis actions if needed
        if mood_analysis.requires_crisis_support:
            actions.append(AgentAction(
                action_type=ActionType.ESCALATE,
                parameters={"level": "crisis", "resources": True},
                rationale="User shows crisis indicators",
                timestamp=datetime.now(),
                expected_outcome="User receives crisis resources and support",
                priority=1
            ))
            return actions  # Return immediately for crisis
            
        # Retrieve relevant resources
        actions.append(AgentAction(
            action_type=ActionType.RETRIEVE_RESOURCES,
            parameters={
                "mood": mood_analysis.primary_mood,
                "triggers": mood_analysis.triggers,
                "count": 3
            },
            rationale="Provide evidence-based resources",
            timestamp=datetime.now() + timedelta(minutes=1),
            expected_outcome="User has access to relevant coping resources",
            priority=2
        ))
        
        # Mood-specific actions
        if mood_analysis.primary_mood == "anxious":
            actions.append(AgentAction(
                action_type=ActionType.PROVIDE_TECHNIQUE,
                parameters={"technique": "breathing_478"},
                rationale="Immediate anxiety reduction technique",
                timestamp=datetime.now() + timedelta(minutes=2),
                expected_outcome="Reduced anxiety symptoms",
                priority=1
            ))
            
        elif mood_analysis.primary_mood == "sad":
            actions.append(AgentAction(
                action_type=ActionType.SUGGEST_ACTIVITY,
                parameters={"type": "behavioral_activation"},
                rationale="Counter depression through activity",
                timestamp=datetime.now() + timedelta(minutes=2),
                expected_outcome="Increased engagement and mood improvement",
                priority=2
            ))
            
        # Add journaling prompt
        actions.append(AgentAction(
            action_type=ActionType.JOURNAL_PROMPT,
            parameters={
                "focus": mood_analysis.primary_mood,
                "type": "reflection"
            },
            rationale="Encourage emotional processing through writing",
            timestamp=datetime.now() + timedelta(minutes=5),
            expected_outcome="Increased emotional awareness and processing",
            priority=3
        ))
        
        # Schedule check-in
        actions.append(AgentAction(
            action_type=ActionType.CHECK_IN,
            parameters={"delay_hours": 24},
            rationale="Monitor progress and adjust support",
            timestamp=datetime.now() + timedelta(hours=24),
            expected_outcome="Continued engagement and support",
            priority=4
        ))
        
        # Add reflection
        actions.append(AgentAction(
            action_type=ActionType.OFFER_REFLECTION,
            parameters={"focus": "progress"},
            rationale="Consolidate learning and progress",
            timestamp=datetime.now() + timedelta(hours=48),
            expected_outcome="Increased self-awareness and skill retention",
            priority=5
        ))
        
        return sorted(actions, key=lambda x: x.priority)
        
    def execute_action(
        self,
        action: AgentAction,
        user_id: str
    ) -> Tuple[bool, Any]:
        """
        Execute a single action from the plan
        
        Args:
            action: Action to execute
            user_id: User identifier
            
        Returns:
            Tuple of (success, result)
        """
        try:
            logger.info(f"Executing action {action.action_type.value} for user {user_id}")
            
            if action.action_type == ActionType.ANALYZE_MOOD:
                result = self._execute_mood_analysis(action.parameters)
                
            elif action.action_type == ActionType.RETRIEVE_RESOURCES:
                result = self._execute_resource_retrieval(action.parameters)
                
            elif action.action_type == ActionType.PROVIDE_TECHNIQUE:
                result = self._execute_technique_provision(action.parameters)
                
            elif action.action_type == ActionType.SUGGEST_ACTIVITY:
                result = self._execute_activity_suggestion(action.parameters)
                
            elif action.action_type == ActionType.JOURNAL_PROMPT:
                result = self._execute_journal_prompt(action.parameters)
                
            elif action.action_type == ActionType.CHECK_IN:
                result = self._execute_check_in(user_id, action.parameters)
                
            elif action.action_type == ActionType.ESCALATE:
                result = self._execute_escalation(action.parameters)
                
            elif action.action_type == ActionType.OFFER_REFLECTION:
                result = self._execute_reflection(user_id, action.parameters)
                
            else:
                result = {"error": f"Unknown action type: {action.action_type}"}
                
            # Mark as completed
            action.completed = True
            action.result = result
            
            # Store in history
            self.action_history.append(action)
            
            return True, result
            
        except Exception as e:
            logger.error(f"Error executing action {action.action_type}: {e}")
            action.result = {"error": str(e)}
            return False, {"error": str(e)}
            
    def _execute_mood_analysis(self, parameters: Dict) -> Dict:
        """Execute mood analysis action"""
        return {
            "action": "mood_analysis",
            "message": "I'm here to understand how you're feeling. Your emotions are valid and important.",
            "next_step": "Based on your mood, I'll suggest helpful resources and techniques."
        }
        
    def _execute_resource_retrieval(self, parameters: Dict) -> Dict:
        """Execute resource retrieval action"""
        resources = self.rag_system.retrieve_relevant_resources(
            query="",
            mood=parameters.get("mood"),
            triggers=parameters.get("triggers"),
            n_results=parameters.get("count", 3)
        )
        
        return {
            "action": "resource_retrieval",
            "resources": [
                {
                    "title": r.resource.title,
                    "content": r.resource.content,
                    "effectiveness": r.resource.effectiveness_rating
                }
                for r in resources
            ],
            "message": "I've found some evidence-based resources that might help."
        }
        
    def _execute_technique_provision(self, parameters: Dict) -> Dict:
        """Execute technique provision action"""
        technique_map = {
            "breathing_478": {
                "name": "4-7-8 Breathing",
                "steps": [
                    "Exhale completely",
                    "Inhale through nose for 4 counts",
                    "Hold breath for 7 counts",
                    "Exhale through mouth for 8 counts"
                ],
                "duration": "5 minutes"
            },
            "grounding_54321": {
                "name": "5-4-3-2-1 Grounding",
                "steps": [
                    "Name 5 things you can see",
                    "Name 4 things you can touch",
                    "Name 3 things you can hear",
                    "Name 2 things you can smell",
                    "Name 1 thing you can taste"
                ],
                "duration": "3-5 minutes"
            }
        }
        
        technique = technique_map.get(parameters.get("technique"), {})
        
        return {
            "action": "provide_technique",
            "technique": technique,
            "message": f"Let's try the {technique.get('name', 'relaxation')} technique together."
        }
        
    def _execute_activity_suggestion(self, parameters: Dict) -> Dict:
        """Execute activity suggestion action"""
        activity_type = parameters.get("type", "general")
        
        activities = {
            "behavioral_activation": [
                "Take a 10-minute walk outside",
                "Call or text a friend",
                "Do a small creative activity",
                "Listen to uplifting music"
            ],
            "stress_relief": [
                "Practice yoga or stretching",
                "Take a warm bath",
                "Do a puzzle or game",
                "Watch something funny"
            ],
            "general": [
                "Engage in a hobby you enjoy",
                "Spend time in nature",
                "Practice gratitude",
                "Do something kind for yourself"
            ]
        }
        
        return {
            "action": "suggest_activity",
            "activities": activities.get(activity_type, activities["general"]),
            "message": "Small actions can make a big difference. Choose what feels right for you."
        }
        
    def _execute_journal_prompt(self, parameters: Dict) -> Dict:
        """Execute journal prompt action"""
        focus = parameters.get("focus", "general")
        
        prompts = {
            "anxious": [
                "What specific worries are on your mind right now?",
                "What would you tell a friend in your situation?",
                "What's one small step you could take today?"
            ],
            "sad": [
                "What brought you joy recently, even if small?",
                "What are you grateful for today?",
                "What would self-compassion look like right now?"
            ],
            "angry": [
                "What's really behind this anger?",
                "What boundaries might need to be set?",
                "How can you express this feeling constructively?"
            ],
            "general": [
                "How are you really feeling right now?",
                "What do you need most today?",
                "What's one thing you're proud of?"
            ]
        }
        
        return {
            "action": "journal_prompt",
            "prompts": prompts.get(focus, prompts["general"]),
            "message": "Writing can help process emotions. There's no right or wrong way to journal."
        }
        
    def _execute_check_in(self, user_id: str, parameters: Dict) -> Dict:
        """Execute check-in action"""
        return {
            "action": "check_in",
            "message": "Hi! I wanted to check in and see how you're doing today.",
            "questions": [
                "How has your mood been since we last connected?",
                "Have you tried any of the suggested techniques?",
                "Is there anything specific you'd like support with?"
            ]
        }
        
    def _execute_escalation(self, parameters: Dict) -> Dict:
        """Execute escalation for crisis support"""
        level = parameters.get("level", "standard")
        
        if level == "crisis":
            return {
                "action": "crisis_escalation",
                "immediate_resources": [
                    "National Suicide Prevention Lifeline: 988",
                    "Crisis Text Line: Text HOME to 741741",
                    "Emergency Services: 911"
                ],
                "message": "Your safety is the top priority. Please reach out for immediate support.",
                "urgent": True
            }
        
        return {
            "action": "escalation",
            "message": "It might be helpful to talk to a mental health professional.",
            "resources": ["Find a therapist: psychologytoday.com", "SAMHSA Helpline: 1-800-662-4357"]
        }
        
    def _execute_reflection(self, user_id: str, parameters: Dict) -> Dict:
        """Execute reflection action"""
        plan = self.active_plans.get(user_id)
        
        if plan:
            completed_actions = [a for a in plan.actions if a.completed]
            success_rate = len(completed_actions) / len(plan.actions) if plan.actions else 0
            
            return {
                "action": "reflection",
                "message": "Let's reflect on your progress:",
                "insights": [
                    f"You've completed {len(completed_actions)} supportive actions",
                    f"Your engagement level: {success_rate * 100:.0f}%",
                    "Every small step is progress"
                ],
                "next_steps": "Continue building on what's working for you."
            }
            
        return {
            "action": "reflection",
            "message": "Take a moment to appreciate your journey.",
            "insights": ["You're taking steps to support your mental health", "Progress isn't always linear"]
        }
        
    def monitor_and_adjust(
        self,
        user_id: str,
        feedback: Optional[Dict[str, Any]] = None
    ) -> InterventionPlan:
        """
        Monitor progress and adjust intervention plan
        
        Args:
            user_id: User identifier
            feedback: User feedback on interventions
            
        Returns:
            Updated intervention plan
        """
        plan = self.active_plans.get(user_id)
        
        if not plan:
            logger.warning(f"No active plan found for user {user_id}")
            return None
            
        # Evaluate effectiveness
        effectiveness_scores = []
        for action in plan.actions:
            if action.completed and action.effectiveness is not None:
                effectiveness_scores.append(action.effectiveness)
                
        avg_effectiveness = sum(effectiveness_scores) / len(effectiveness_scores) if effectiveness_scores else 0
        
        # Update plan based on effectiveness
        if avg_effectiveness < 0.5:
            # Plan not working well, adjust approach
            logger.info(f"Adjusting plan for user {user_id} due to low effectiveness")
            
            # Add new actions or modify existing ones
            new_actions = self._generate_alternative_actions(plan)
            plan.actions.extend(new_actions)
            
        # Update stage
        completed_count = sum(1 for a in plan.actions if a.completed)
        total_count = len(plan.actions)
        
        if completed_count == 0:
            plan.stage = InterventionStage.PLANNING
        elif completed_count < total_count * 0.3:
            plan.stage = InterventionStage.INTERVENTION
        elif completed_count < total_count * 0.7:
            plan.stage = InterventionStage.MONITORING
        elif completed_count < total_count:
            plan.stage = InterventionStage.REFLECTION
        else:
            plan.stage = InterventionStage.FOLLOW_UP
            
        # Update timestamps
        plan.updated_at = datetime.now()
        
        # Store success metrics
        plan.success_metrics = {
            "completion_rate": completed_count / total_count if total_count > 0 else 0,
            "average_effectiveness": avg_effectiveness,
            "engagement_score": self._calculate_engagement_score(plan)
        }
        
        return plan
        
    def _generate_alternative_actions(self, plan: InterventionPlan) -> List[AgentAction]:
        """Generate alternative actions when current plan isn't effective"""
        alternative_actions = []
        
        # Try different approach based on mood
        if plan.mood_state["primary_mood"] == "anxious":
            alternative_actions.append(AgentAction(
                action_type=ActionType.PROVIDE_TECHNIQUE,
                parameters={"technique": "grounding_54321"},
                rationale="Alternative anxiety management technique",
                timestamp=datetime.now(),
                expected_outcome="Reduced anxiety through grounding",
                priority=2
            ))
            
        # Add peer support suggestion
        alternative_actions.append(AgentAction(
            action_type=ActionType.SUGGEST_ACTIVITY,
            parameters={"type": "social_connection"},
            rationale="Social support can improve mood",
            timestamp=datetime.now() + timedelta(hours=1),
            expected_outcome="Increased social connection",
            priority=3
        ))
        
        return alternative_actions
        
    def _calculate_engagement_score(self, plan: InterventionPlan) -> float:
        """Calculate user engagement score based on actions"""
        if not plan.actions:
            return 0.0
            
        # Factors: completion rate, timeliness, effectiveness
        completed = [a for a in plan.actions if a.completed]
        
        if not completed:
            return 0.0
            
        completion_rate = len(completed) / len(plan.actions)
        
        # Check if actions were completed on time
        timely_completion = sum(
            1 for a in completed
            if a.timestamp and abs((a.timestamp - datetime.now()).total_seconds()) < 3600
        ) / len(completed)
        
        # Average effectiveness
        effectiveness_scores = [a.effectiveness for a in completed if a.effectiveness is not None]
        avg_effectiveness = sum(effectiveness_scores) / len(effectiveness_scores) if effectiveness_scores else 0.5
        
        # Weighted engagement score
        engagement = (
            completion_rate * 0.4 +
            timely_completion * 0.3 +
            avg_effectiveness * 0.3
        )
        
        return min(1.0, engagement)
        
    def get_intervention_summary(self, user_id: str) -> Dict[str, Any]:
        """Get summary of intervention for a user"""
        plan = self.active_plans.get(user_id)
        
        if not plan:
            return {"error": "No active intervention plan"}
            
        completed_actions = [a for a in plan.actions if a.completed]
        pending_actions = [a for a in plan.actions if not a.completed]
        
        return {
            "user_id": user_id,
            "mood_state": plan.mood_state,
            "goals": plan.goals,
            "stage": plan.stage.value,
            "progress": {
                "completed_actions": len(completed_actions),
                "pending_actions": len(pending_actions),
                "total_actions": len(plan.actions)
            },
            "metrics": plan.success_metrics,
            "created_at": plan.created_at.isoformat(),
            "updated_at": plan.updated_at.isoformat()
        }