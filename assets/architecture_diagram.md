# MoodSense AI System Architecture

## High-Level System Architecture

```mermaid
graph TB
    %% User Input Layer
    User[("👤 User")] -->|"Text/Journal Entry"| CLI["🖥️ CLI Interface"]
    User -->|"HTTP Request"| Web["🌐 Web Interface"]
    
    %% Input Processing
    CLI --> InputVal["🛡️ Input Validator"]
    Web --> InputVal
    
    %% Core Processing Pipeline
    InputVal --> MoodAnalyzer["🧠 Enhanced Mood Analyzer<br/>• Multi-dimensional emotions<br/>• Trigger detection<br/>• Crisis detection"]
    
    MoodAnalyzer -->|"Mood State"| Agent["🤖 Support Agent<br/>• Planning<br/>• Execution<br/>• Monitoring"]
    
    %% RAG System
    Agent -->|"Query"| RAG["📚 RAG System"]
    RAG --> VectorStore["🔍 Vector Store<br/>(ChromaDB)"]
    RAG --> KnowledgeBase["📖 Knowledge Base<br/>• CBT Techniques<br/>• Coping Strategies<br/>• Crisis Resources"]
    
    %% Agent Actions
    Agent --> ActionExecutor["⚡ Action Executor"]
    ActionExecutor --> Actions["📋 Actions<br/>• Provide Techniques<br/>• Suggest Activities<br/>• Journal Prompts<br/>• Check-ins"]
    
    %% Data Storage
    MoodAnalyzer -->|"Store Analysis"| DB[("💾 Database<br/>• User Profiles<br/>• Mood History<br/>• Journal Entries")]
    Agent -->|"Store Plans"| DB
    Actions -->|"Track Progress"| DB
    
    %% Monitoring & Feedback
    Actions --> Monitor["📊 Performance Monitor"]
    Monitor -->|"Metrics"| Evaluator["✅ Reliability Evaluator<br/>• Consistency Check<br/>• Bias Detection<br/>• Effectiveness Score"]
    
    %% Human Review
    Evaluator -->|"Flagged Issues"| HumanReview["👩‍⚕️ Human Review<br/>• Crisis Cases<br/>• Low Confidence<br/>• Bias Concerns"]
    
    %% Output Generation
    Actions --> ResponseGen["💬 Response Generator"]
    ResponseGen -->|"Personalized Support"| User
    
    %% Logging
    MoodAnalyzer -.->|"Log"| Logger["📝 Logger"]
    Agent -.->|"Log"| Logger
    Evaluator -.->|"Log"| Logger
    
    %% Testing Pipeline
    TestSuite["🧪 Test Suite"] -->|"Test Cases"| MoodAnalyzer
    TestSuite -->|"Test Cases"| RAG
    TestSuite -->|"Test Cases"| Agent
    
    style User fill:#e1f5fe
    style MoodAnalyzer fill:#fff9c4
    style Agent fill:#f3e5f5
    style RAG fill:#e8f5e9
    style DB fill:#fff3e0
    style HumanReview fill:#ffebee
    style Logger fill:#f5f5f5
```

## Detailed Component Flow

### 1. Input Processing Flow
```mermaid
sequenceDiagram
    participant User
    participant Interface
    participant Validator
    participant MoodAnalyzer
    participant CrisisDetector
    
    User->>Interface: Submit text/journal entry
    Interface->>Validator: Validate input
    Validator->>Validator: Check for malicious content
    Validator->>MoodAnalyzer: Process clean input
    MoodAnalyzer->>MoodAnalyzer: Tokenize & preprocess
    MoodAnalyzer->>MoodAnalyzer: Detect emotions (15 dimensions)
    MoodAnalyzer->>CrisisDetector: Check crisis indicators
    
    alt Crisis Detected
        CrisisDetector-->>Interface: URGENT: Escalate to crisis protocol
        Interface-->>User: Provide immediate resources
    else Normal Flow
        MoodAnalyzer-->>Interface: Return mood analysis
    end
```

### 2. RAG System Flow
```mermaid
graph LR
    subgraph "RAG Pipeline"
        Query["🔤 User Query"] --> Embed["🔢 Embedding<br/>(MiniLM-L6)"]
        Embed --> Search["🔍 Semantic Search"]
        Search --> ChromaDB["💾 ChromaDB<br/>Vector Store"]
        
        ChromaDB --> Retrieve["📚 Retrieve Top-K<br/>Resources"]
        Retrieve --> Rerank["🎯 Rerank by<br/>• Mood match<br/>• Trigger match<br/>• Effectiveness"]
        
        Rerank --> Context["📋 Build Context"]
        Context --> Generate["💬 Generate Response<br/>with Citations"]
    end
    
    subgraph "Knowledge Base"
        KB1["CBT Techniques"]
        KB2["Breathing Exercises"]
        KB3["Grounding Methods"]
        KB4["Crisis Resources"]
        KB5["Self-Compassion"]
    end
    
    KB1 --> ChromaDB
    KB2 --> ChromaDB
    KB3 --> ChromaDB
    KB4 --> ChromaDB
    KB5 --> ChromaDB
```

### 3. Agentic Workflow
```mermaid
stateDiagram-v2
    [*] --> Assessment
    Assessment --> Planning: Mood Analyzed
    Planning --> Intervention: Plan Created
    Intervention --> Monitoring: Actions Executed
    Monitoring --> Reflection: Progress Tracked
    Reflection --> FollowUp: Insights Generated
    
    Monitoring --> Adjustment: Low Effectiveness
    Adjustment --> Intervention: New Actions
    
    FollowUp --> [*]: Complete
    
    Assessment --> Escalation: Crisis Detected
    Escalation --> [*]: Emergency Protocol
    
    note right of Assessment
        • Analyze mood state
        • Identify triggers
        • Detect crisis indicators
    end note
    
    note right of Planning
        • Set intervention goals
        • Select appropriate resources
        • Schedule actions
    end note
    
    note right of Intervention
        • Execute planned actions
        • Provide techniques
        • Deliver resources
    end note
    
    note right of Monitoring
        • Track completion
        • Measure effectiveness
        • Gather feedback
    end note
```

### 4. Testing & Reliability Pipeline
```mermaid
graph TB
    subgraph "Testing Framework"
        UT["Unit Tests"] --> CI["Continuous Integration"]
        IT["Integration Tests"] --> CI
        RT["Reliability Tests"] --> CI
        
        CI --> Results["Test Results"]
    end
    
    subgraph "Reliability Checks"
        Input2["User Input"] --> ConsistencyCheck["Consistency Check<br/>• Same input → Similar output<br/>• Confidence thresholds"]
        Input2 --> BiasDetection["Bias Detection<br/>• Gender bias<br/>• Cultural sensitivity<br/>• Age appropriateness"]
        Input2 --> SafetyCheck["Safety Check<br/>• Crisis detection accuracy<br/>• Harmful content filter<br/>• Escalation triggers"]
    end
    
    subgraph "Human Review"
        Flagged["Flagged Cases"] --> HumanExpert["Human Expert"]
        HumanExpert --> Feedback["Feedback Loop"]
        Feedback --> ModelUpdate["Model/KB Update"]
    end
    
    ConsistencyCheck --> Flagged
    BiasDetection --> Flagged
    SafetyCheck --> Flagged
    
    Results --> Dashboard["📊 Metrics Dashboard<br/>• Accuracy: 85%<br/>• Crisis Detection: 95%<br/>• User Satisfaction: 4.2/5"]
```

## Data Flow Summary

### Input → Process → Output

1. **Input Stage**
   - User provides text through CLI or Web interface
   - Input validation and sanitization
   - Crisis keyword scanning

2. **Analysis Stage**
   - Multi-dimensional emotion detection
   - Context and trigger identification
   - Intensity and confidence scoring

3. **Planning Stage**
   - Agent creates intervention plan
   - RAG retrieves relevant resources
   - Actions prioritized by urgency

4. **Execution Stage**
   - Techniques provided
   - Activities suggested
   - Journal prompts generated

5. **Monitoring Stage**
   - Progress tracked
   - Effectiveness measured
   - Adjustments made

6. **Output Stage**
   - Personalized response generated
   - Resources cited
   - Follow-up scheduled

## Human-in-the-Loop Checkpoints

| Checkpoint | Purpose | Trigger Conditions |
|------------|---------|-------------------|
| **Crisis Review** | Immediate safety assessment | Crisis keywords detected |
| **Low Confidence Review** | Verify uncertain analyses | Confidence < 40% |
| **Bias Review** | Check for harmful stereotypes | Sensitive demographic mentions |
| **Effectiveness Review** | Assess intervention success | Effectiveness < 50% after 3 attempts |
| **Escalation Review** | Professional referral decision | Persistent severe symptoms |

## Testing Integration Points

```mermaid
graph LR
    subgraph "Automated Testing"
        T1["Mood Analysis Tests<br/>100+ test cases"] --> Auto["✅ Automated"]
        T2["RAG Retrieval Tests<br/>50+ queries"] --> Auto
        T3["Agent Planning Tests<br/>20 scenarios"] --> Auto
    end
    
    subgraph "Manual Testing"
        T4["Crisis Response Tests"] --> Manual["👤 Manual Review"]
        T5["Edge Case Tests"] --> Manual
        T6["User Experience Tests"] --> Manual
    end
    
    Auto --> Report["📊 Test Report"]
    Manual --> Report
    Report --> Deploy{Deploy?}
    Deploy -->|Pass| Prod["🚀 Production"]
    Deploy -->|Fail| Fix["🔧 Fix Issues"]
```

## Performance Metrics

- **Response Time**: < 2 seconds for mood analysis
- **RAG Retrieval**: < 1 second for top-5 resources
- **Crisis Detection**: 95% accuracy, 0% false negatives tolerated
- **User Engagement**: 70% action completion rate
- **System Uptime**: 99.9% availability target