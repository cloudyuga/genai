🚫 What .co Files Can’t Do

They don’t teach the model or give it semantic generalization capabilities.

They don't support NLU (natural language understanding) out-of-the-box.

If your question isn't exactly or very closely worded as one of the user utterances in define user ask politics, the rule will be missed.

🚫 Nemo Guardrail

NeMo currently relies on pattern-based matching, not ML-based NLU (like intent classification in Rasa or Dialogflow).

However, semantic matching is on the roadmap, and some experimentation can be done using embedding-based classification, but not directly via .co files yet.
