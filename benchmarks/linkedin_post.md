**Introducing Varity v0.1: A Novel Metric for LLM Hallucination Detection**

I'm thrilled to share Varity, an open-source Python library tackling LLMs confidently generating plausible but incorrect statements.

**The Problem**
Asking one LLM "Is this true?" causes confirmation bias, ratifying another model's hallucination. RAG helps but degrades when data goes stale.

**The Solution: Verdict Stability Score (VSS)**
Varity drops external retrieval and turns the LLM's latent space against itself. 
*Core Thesis*: True facts exist densely; lies exist sparsely. Under adversarial questioning (Depth-N Interrogation), hallucinatory claims mathematically collapse. Varity tracks these contradictory "flips." 
Low VSS = mathematical instability = hallucination.

**How It Works:**
1️⃣ Atomic Decomposition: Breaks responses into isolated claims.
2️⃣ Depth-N Interrogation: Recursive verification across isolated chambers.
3️⃣ Dual-Signal Gate: Combines Bayesian confidence + VSS.

**The Academic Foundation:**
📚 Built on findings that LLMs possess latent self-critique capabilities (Manakul et al. & Dhuliawala et al., 2023).
📚 Proves that fragile hallucinations structurally degrade under extended context lengths (Araujo et al., arXiv:2512.12775).
📚 Varity packages these theoretical limits into a deployable math equation.

**Benchmarks (gpt-4o-mini)**
✅ 100% Detection Accuracy
✅ 0% False Positives

Zero telemetry. Strictly BYOK.

Massive thanks to Dr. Shubhadeep for the motivation and belief in my research! Feedback appreciated! 

📦 `pip install varity`
🎮 charchitd.github.io/Varity-v0.1

#MachineLearning #LLMs #AI #Python #FactChecking
