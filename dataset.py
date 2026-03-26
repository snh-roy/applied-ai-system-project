"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
    "fire",
    "sick",
    "proud",
    "favorite",
    "🔥",
    "😊",
    "😂",
    "✨",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
    "failed",
    "exhausted",
    "💀",
    "🥲",
    "😒",
    "😭",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    "no cap this burger is fire 🔥",
    "I lowkey failed that test but it's fine 🥲",
    "waking up at 5am is my favorite thing ever",
    "The weather is just okay today",
    "highkey stressed for the final 💀",
    "manifesting a good grade today",
    "it is what it is",
    "I'm so over this week already",
    "This movie was sick!",
    "I love getting stuck in traffic",
    "I'm fine 🙂",
    "I'm exhausted but proud of myself",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    "positive",  # "no cap this burger is fire 🔥"
    "mixed",     # "I lowkey failed that test but it's fine 🥲"
    "negative",  # "waking up at 5am is my favorite thing ever" (sarcasm)
    "neutral",   # "The weather is just okay today"
    "negative",  # "highkey stressed for the final 💀"
    "positive",  # "manifesting a good grade today"
    "neutral",   # "it is what it is"
    "negative",  # "I'm so over this week already"
    "positive",  # "This movie was sick!" (slang)
    "negative",  # "I love getting stuck in traffic" (sarcasm)
    "neutral",   # "I'm fine 🙂"
    "mixed",     # "I'm exhausted but proud of myself"
]

# TODO: Add 5-10 more posts and labels.
#
# Requirements:
#   - For every new post you add to SAMPLE_POSTS, you must add one
#     matching label to TRUE_LABELS.
#   - SAMPLE_POSTS and TRUE_LABELS must always have the same length.
#   - Include a variety of language styles, such as:
#       * Slang ("lowkey", "highkey", "no cap")
#       * Emojis (":)", ":(", "🥲", "😂", "💀")
#       * Sarcasm ("I absolutely love getting stuck in traffic")
#       * Ambiguous or mixed feelings
#
# Tips:
#   - Try to create some examples that are hard to label even for you.
#   - Make a note of any examples that you and a friend might disagree on.
#     Those "edge cases" are interesting to inspect for both the rule based
#     and ML models.
#
# Example of how you might extend the lists:
#
# SAMPLE_POSTS.append("Lowkey stressed but kind of proud of myself")
# TRUE_LABELS.append("mixed")
#
# Remember to keep them aligned:
#   len(SAMPLE_POSTS) == len(TRUE_LABELS)
