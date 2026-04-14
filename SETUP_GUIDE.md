## Quick Start (No Installation Required!)

### Option 1: Run Simple Demo (Recommended for First-Time Users)
```bash
# Clone the repository
git clone https://github.com/snh-roy/applied-ai-system-project.git
cd applied-ai-system-project

# Run the demo - NO INSTALLATION NEEDED!
python demo_simple.py

# Or run demo with examples
python demo_simple.py --demo
```

That's it! The simple demo works with just Python 3.6+.

---

## Full Installation Guide

### Prerequisites
- **Python**: Version 3.7 or higher
- **pip**: Python package manager
- **Git**: For cloning the repository
- **Memory**: At least 2GB RAM recommended

### Step 1: Clone the Repository
```bash
git clone https://github.com/snh-roy/applied-ai-system-project.git
cd applied-ai-system-project
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

#### Option A: Minimal Installation (Basic Features)
```bash
# Just install core dependencies
pip install numpy scikit-learn
```

#### Option B: Full Installation (All Features)
```bash
# Install all dependencies
pip install -r requirements.txt
```

**Note**: Some packages like `torch` and `transformers` are large (1GB+). If you have limited space/bandwidth, use the minimal installation.

### Step 4: Common Installation Issues & Fixes

#### Issue: "No module named 'sentence_transformers'"
**Solution**: This is optional. The demo works without it:
```bash
# Either install it:
pip install sentence-transformers

# Or use the simple demo instead:
python demo_simple.py
```

#### Issue: "ChromaDB installation failed"
**Solution**: ChromaDB is optional for RAG features:
```bash
# Try installing without dependencies:
pip install chromadb --no-deps

# Or skip it and use basic mode
```

#### Issue: "torch installation is too large"
**Solution**: Use CPU-only version:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

---

## 📖 How to Use MoodSense AI

### 1. Simple Demo Mode (No Dependencies)
```bash
python demo_simple.py
```
Type any text about how you're feeling:
- "I'm feeling anxious about my exam"
- "I've been really sad lately"
- "Everything is going great!"

### 2. Original Mood Machine (Basic Dependencies)
```bash
# Run the original simple version
python main.py
```

### 3. Full MoodSense AI (All Dependencies)
```bash
# Run the complete system
python main_moodsense.py

# Or analyze specific text
python main_moodsense.py --analyze "I'm feeling stressed"

# Run test examples
python main_moodsense.py --test
```

### 4. Run Tests
```bash
# If pytest is installed:
python run_all_tests.py

# Or run individual test files:
python tests/test_mood_analyzer.py
```

---

## 🎮 Features by Installation Level

### Minimal Installation Features:
- ✅ Basic mood detection (positive/negative/neutral)
- ✅ Simple keyword-based analysis
- ✅ Crisis keyword detection
- ✅ Basic suggestions

### Full Installation Features:
- ✅ 15-dimensional emotion analysis
- ✅ RAG-based resource retrieval
- ✅ Semantic search through mental health resources
- ✅ Autonomous support planning
- ✅ Comprehensive logging
- ✅ Advanced NLP with transformers

---

## 📝 Example Usage Sessions

### Example 1: Anxiety Support
```
$ python demo_simple.py
🧠 MOODSENSE AI - Mental Health Support System
Type your message or 'quit' to exit

💭 You: I'm really anxious about my presentation tomorrow

📊 MOOD ANALYSIS RESULTS
🎭 Primary Mood: ANXIOUS
🎯 Confidence: 50%

💡 RECOMMENDED SUPPORT
📚 4-7-8 Breathing Technique
The 4-7-8 breathing technique helps calm your nervous system...
```

### Example 2: Crisis Detection
```
💭 You: I don't want to live anymore

⚠️ CRISIS DETECTED - IMMEDIATE SUPPORT NEEDED ⚠️
Your safety is the top priority. Please reach out now:
• National Suicide Prevention Lifeline: 988
• Crisis Text Line: Text HOME to 741741
```

---

## 🔧 Troubleshooting

### Python Version Issues
Check your Python version:
```bash
python --version
# Should be 3.7 or higher

# If not, try:
python3 --version
# Then use python3 instead of python
```

### Import Errors
If you get import errors:
1. Make sure you're in the project directory
2. Check if virtual environment is activated
3. Try the simple demo first: `python demo_simple.py`

### Memory Issues
If installation fails due to memory:
```bash
# Install packages one by one:
pip install numpy
pip install scikit-learn
pip install nltk
# etc...
```

---

## 📁 Project Structure Explanation

```
applied-ai-system-project/
│
├── demo_simple.py          # ← START HERE! No dependencies needed
├── main.py                 # Original mood machine (basic deps)
├── main_moodsense.py       # Full system (all deps needed)
│
├── src/                    # Advanced implementation
│   ├── core/              # Enhanced mood analyzer
│   ├── rag/               # RAG system
│   ├── agents/            # Autonomous agents
│   └── utils/             # Logging and utilities
│
├── tests/                  # Test files (need pytest)
├── assets/                 # Diagrams and images
├── README.md              # Main documentation
└── requirements.txt        # Full dependency list
```

---

## 💡 Tips for Success

1. **Start Simple**: Run `demo_simple.py` first to see what the system does
2. **Gradual Installation**: Install dependencies as needed, not all at once
3. **Check Examples**: The demo includes several example inputs to try
4. **Read Error Messages**: They usually tell you exactly what's missing
5. **Use Virtual Environment**: Keeps your system Python clean

---

## 🆘 Getting Help

If you're stuck:
1. Try the simple demo first: `python demo_simple.py`
2. Check this guide's troubleshooting section
3. Look at error messages carefully
4. Create an issue on GitHub with:
   - Your Python version
   - The command you ran
   - The full error message

---

## ✅ Quick Verification

To verify everything is working, run these commands in order:

```bash
# 1. Test simple demo (should always work)
python demo_simple.py --demo

# 2. Test original mood machine (needs basic deps)
python main.py

# 3. Test full system (needs all deps)
python main_moodsense.py --test

# 4. Run tests (needs pytest)
python run_all_tests.py
```

If step 1 works, the core project is functional!

---

## 📊 Expected Output

When running correctly, you should see:
- Mood analysis with confidence scores
- Emotion detection across multiple dimensions
- Personalized coping strategies
- Crisis detection when appropriate
- Evidence-based resource recommendations

---

*Remember: The simple demo (`demo_simple.py`) ALWAYS works with just Python. Start there!*