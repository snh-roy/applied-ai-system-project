# Model Card: Mood Machine

This model card is for the Mood Machine project, which includes **two** versions of a mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn

## 1. Model Overview

**Model type:**  
I compared both the rule-based model and the ML model.

**Intended purpose:**  
The model classifies short text snippets (social media style) into four mood categories: **positive**, **negative**, **neutral**, and **mixed**.

**How it works (brief):**  
- **Rule-based:** Uses keyword matching against `POSITIVE_WORDS` and `NEGATIVE_WORDS`. It includes simple negation handling (e.g., "not happy" counts as negative).
- **ML version:** Uses a CountVectorizer to turn text into word counts (bag-of-words) and a Logistic Regression classifier trained on the `SAMPLE_POSTS` and `TRUE_LABELS`.

## 2. Data

**Dataset description:**  
The dataset consists of 18 `SAMPLE_POSTS` with corresponding `TRUE_LABELS`. I expanded the starter set with 12 new posts.

**Labeling process:**  
I manually labeled new posts based on common sentiment. Posts like "I lowkey failed that test but it's fine 🥲" were labeled as **mixed** because they combine a negative event with a neutral/positive coping sentiment.

**Important characteristics of your dataset:**  
- **Slang:** Includes "no cap", "fire", "highkey", "lowkey", and "sick".
- **Emojis:** Uses 🔥, 🥲, 💀, and 🙂.
- **Sarcasm:** "waking up at 5am is my favorite thing ever" and "I love getting stuck in traffic".

**Possible issues with the dataset:**  
The dataset is very small (18 examples), which leads to overfitting in the ML model and poor generalization for the rule-based model when it encounters words not in its lists.

## 3. How the Rule Based Model Works (if used)

**Your scoring rules:**  
- **Preprocessing:** Lowercases text and uses regex to split words and emojis into tokens.
- **Scoring:** Starts at 0. Positive words add 1, negative words subtract 1.
- **Negation:** If a negation word ("not", "never", etc.) precedes a sentiment word, the score is flipped (e.g., "not happy" = -1).
- **Slang/Emojis:** Terms like "fire", "sick", and 🔥 are explicitly added to `POSITIVE_WORDS`.

**Strengths of this approach:**  
Very predictable and easy to debug. You can see exactly which word caused a score change.

**Weaknesses of this approach:**  
Fails completely on sarcasm. For example, "I love getting stuck in traffic" is predicted as **positive** because "love" is a high-weight positive word, and the model doesn't understand the context of "traffic".

## 4. How the ML Model Works (if used)

**Features used:**  
Bag-of-words using `CountVectorizer`.

**Training data:**  
Trained on the 18 labeled examples in `dataset.py`.

**Training behavior:**  
The model achieved 100% accuracy on its own training data. It "learned" that "traffic" + "love" = negative because I labeled it that way.

**Strengths and weaknesses:**  
- **Strengths:** Can capture complex patterns (like specific sarcastic phrases) if they are in the training data.
- **Weaknesses:** Highly prone to overfitting. If I type a new sarcastic sentence it hasn't seen, it will likely fail just like the rule-based model.

## 5. Evaluation

**How you evaluated the model:**  
I ran both `main.py` and `ml_experiments.py` to compare predictions against `TRUE_LABELS`.

**Accuracy:**
- **Rule-based:** 67%
- **ML Model:** 100% (on training data)

**Examples of correct predictions:**  
- "no cap this burger is fire 🔥" -> **positive** (Correctly identified slang and emoji).
- "I am not happy about this" -> **negative** (Corrected by negation logic).

**Examples of incorrect predictions:**  
- "I love getting stuck in traffic" -> Predicted **positive**, True **negative** (Rule-based failed on sarcasm).
- "I lowkey failed that test but it's fine 🥲" -> Predicted **negative**, True **mixed** (Rule-based didn't weigh "fine" enough to offset "failed").

## 6. Limitations

- **Sarcasm Blindness:** The rule-based model cannot detect irony. "waking up at 5am is my favorite thing ever" is seen as positive because of "favorite".
- **Vocabulary Limit:** If a user uses a synonym not in the list (e.g., "superb" instead of "great"), the rule-based model treats it as neutral.
- **Small Context Window:** Negation only looks at the immediately preceding word.

## 7. Ethical Considerations

- **Cultural Bias:** The model is optimized for Gen-Z/Internet slang ("no cap", "fire"). It might misinterpret more formal language or different dialects.
- **Over-simplification:** Reducing human emotion to four labels can be reductive and might miss signs of genuine distress if the user uses "neutral" sounding language.

## 8. Ideas for Improvement

- **Intensity Weighting:** Make "hate" subtract 2 points while "dislike" only subtracts 1.
- **Expanded Negation:** Handle phrases like "not only... but also...".
- **Emoji Sentiment Library:** Integrate a full list of emoji sentiments.
- **Bigger Dataset:** Train the ML model on thousands of tweets for better generalization.
