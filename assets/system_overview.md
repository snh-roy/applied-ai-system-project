# MoodSense AI - System Overview

## 🏗️ System Architecture Overview

### Core Components & Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE LAYER                      │
├────────────────────┬──────────────────┬────────────────────────┤
│   CLI Interface    │   Web Interface   │    API Endpoints       │
└────────┬───────────┴──────────┬────────┴────────┬──────────────┘
         │                      │                  │
         └──────────────────────┼──────────────────┘
                                │
                    ┌───────────▼────────────┐
                    │   INPUT VALIDATION     │
                    │  • Sanitization        │
                    │  • Crisis Detection    │
                    └───────────┬────────────┘
                                │
                    ┌───────────▼────────────┐
                    │  ENHANCED MOOD ANALYZER│◄──┐
                    │  • 15 Emotion Dims     │   │
                    │  • Trigger Detection   │   │
                    │  • Intensity Scoring   │   │
                    └───────┬───────────────┘   │
                            │                     │
                  ┌─────────▼──────────┐         │ FEEDBACK
                  │   SUPPORT AGENT    │         │ LOOP
                  │  • Planning         │         │
                  │  • Execution        │         │
                  │  • Monitoring       ├─────────┘
                  └─────┬──────────────┘
                        │
            ┌───────────┼───────────┐
            │           │           │
    ┌───────▼──────┐   │   ┌───────▼──────┐
    │ RAG SYSTEM   │   │   │   DATABASE    │
    │              │   │   │               │
    │ • ChromaDB   │   │   │ • User Data   │
    │ • Knowledge  │   │   │ • History     │
    │   Base       │   │   │ • Journals    │
    └──────────────┘   │   └───────────────┘
                       │
              ┌────────▼────────┐
              │ ACTION EXECUTOR │
              │                 │
              │ • Techniques    │
              │ • Activities    │
              │ • Check-ins     │
              └────────┬────────┘
                       │
            ┌──────────▼──────────┐
            │  RESPONSE GENERATOR │
            └──────────┬──────────┘
                       │
                    USER
```

## 🔄 Key Data Flows

### 1. **Standard Support Flow**
```
User Input → Mood Analysis → Agent Planning → RAG Retrieval → 
Action Execution → Response Generation → User
```

### 2. **Crisis Detection Flow**
```
User Input → Crisis Detection → IMMEDIATE ESCALATION → 
Crisis Resources → Human Review Alert → Emergency Support
```

### 3. **Learning & Adaptation Flow**
```
User Feedback → Effectiveness Scoring → Plan Adjustment → 
Knowledge Base Update → Improved Future Responses
```

## 🧪 Testing & Reliability Checkpoints

### Automated Testing
- **Unit Tests**: Each component tested in isolation
- **Integration Tests**: End-to-end workflow validation
- **Regression Tests**: Consistency checks

### Human Review Triggers
1. **Crisis Cases** → Immediate human review
2. **Low Confidence** (<40%) → Expert validation
3. **Bias Detection** → Fairness review
4. **Poor Effectiveness** → Intervention adjustment

## 📊 System Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Response Time | <2s | Per request |
| Crisis Detection | 95% accuracy | Weekly audit |
| User Engagement | 70% completion | Monthly review |
| System Uptime | 99.9% | Continuous |

## 🔐 Safety Features

### Multi-Layer Protection
1. **Input Validation** - Filters harmful content
2. **Crisis Detection** - Immediate escalation
3. **Bias Monitoring** - Fairness checks
4. **Human Review** - Expert oversight
5. **Audit Logging** - Complete traceability

## 💡 Key Innovations

### 1. RAG-Enhanced Support
- Semantic search through mental health resources
- Context-aware resource matching
- Evidence-based recommendations

### 2. Autonomous Agent
- Plans multi-step interventions
- Monitors effectiveness
- Adapts based on progress

### 3. Multi-Dimensional Analysis
- 15 emotion dimensions
- Trigger identification
- Sarcasm detection

## 📈 Data Processing Pipeline

```
                 INPUT PROCESSING
                        │
    ┌───────────────────┼───────────────────┐
    │                   │                   │
Tokenization    Emotion Detection    Trigger Analysis
    │                   │                   │
    └───────────────────┼───────────────────┘
                        │
                 CONTEXT BUILDING
                        │
    ┌───────────────────┼───────────────────┐
    │                   │                   │
Historical Data   Current State    Environmental Factors
    │                   │                   │
    └───────────────────┼───────────────────┘
                        │
                INTERVENTION PLANNING
                        │
    ┌───────────────────┼───────────────────┐
    │                   │                   │
Resource Selection  Action Planning  Schedule Creation
    │                   │                   │
    └───────────────────┼───────────────────┘
                        │
                    EXECUTION
```

## 🔄 Continuous Improvement Loop

```
User Interaction → Data Collection → Performance Analysis → 
Model Refinement → Knowledge Base Update → Enhanced User Experience
```

---

### Quick Start for Developers

1. **Clone Repository**
   ```bash
   git clone https://github.com/snh-roy/applied-ai-system-project.git
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Tests**
   ```bash
   pytest tests/
   ```

4. **Start System**
   ```bash
   python main.py
   ```

### Architecture Benefits

- **Modular**: Easy to extend and maintain
- **Scalable**: Can handle increased load
- **Reliable**: Multiple safety checks
- **Transparent**: Clear audit trail
- **Adaptive**: Learns from interactions