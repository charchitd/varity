# Varity: Core Concepts & Architecture Strategy

This document outlines the foundational research concepts, mathematical models, and architectural decisions that govern the Varity library. Varity was built to address the critical failure state of Large Language Models (LLMs): the generation of highly plausible, yet factually incorrect statements with absolute semantic confidence (hallucinations).

---

## 1. The Core Problem: The Illusion of Certainty
Standard Next-Token-Prediction models do not inherently possess a mechanism for "doubt." Because they optimize for linguistic probability rather than factual groundings, they synthesize falsehoods utilizing the exact same syntactic certainty as factual truths. 

Traditional evaluation frameworks attempt to solve this via **Single-Pass Evaluation**: asking a secondary LLM "Is this true?". However, this is fundamentally flawed. A single-pass prompt is highly susceptible to confirmation bias and often blindly ratifies the first model's hallucination.

## 2. Foundation I: Atomic Claim Decomposition
You cannot evaluate a paragraph simultaneously. If 95% of a paragraph is true, and 5% is a hallucinated statistic, a single-pass evaluator will often label the entire paragraph as "True" due to holistic semantic masking.

**The Varity Approach:**
Before any verification occurs, the generation is forced through a strict **Decomposition Pipeline**.
1. The text is stripped of rhetorical fluff.
2. The core semantic nodes are isolated into a `list[Claim]`.
3. Claims are strictly categorized into typings (e.g., `numerical`, `factual`, `temporal`, `causal`) to inform how they should be tested.

This ensures the "poisoned" node cannot hide behind the surrounding structural truth.

## 3. Foundation II: Depth-N Recursive Interrogation
To break the LLM's confirmation bias, Varity abandons single-pass evaluation for **Recursive Interrogation**.

Instead of asking whether something is true once, Varity forces the model into an isolated, iterative verification chamber. For $N$ depth cycles, the claim is passed structurally to the model from varying adversarial perspectives.
If an LLM has hallucinated a fact, its latent space connection to that fact is mathematically weak. When pressured repeatedly across varying contexts (Depth-N), the LLM will struggle to maintain the lie and will eventually contradict its previous verification.

## 4. Foundation III: The Verdict Stability Score (VSS)
How do we mathematically quantify a hallucination? Through **Boolean Flips**.

Varity introduces the **Verdict Stability Score (VSS)** model. 
* A verified fact exists densely within the LLM's latent space. No matter how many times it is questioned, the LLM will consistently return `VERIFIED`.
* A hallucination exists sparsely. During Depth-N interrogation, the LLM will return `VERIFIED` on pass 1, `CONTRADICTED` on pass 2, and `UNCERTAIN` on pass 3.

**VSS Calculation:**
We track `flip_count` across the recursive chain. A claim that violently oscillates between True and False is heavily penalized by the VSS algorithm. A low VSS strictly indicates hallucination or mathematical instability.

## 5. Foundation IV: Dual-Signal Flagging Matrix
Varity refuses to rely on a single threshold for safety. It implements a **Dual-Signal** gate:
1. **Confidence Threshold:** A purely Bayesian weighted calculation of the semantic certainty of the claims.
2. **VSS Threshold:** The measurement of algorithmic flipping.

A claim is flagged and excised from the final output if it fails **either** the confidence check OR the VSS check. This dual-matrix guarantees that "Confidently Wrong" hallucinations (High Confidence, Low VSS) are caught before reaching the end user.

## 6. Execution Strategy: Raw HTTP / BYOK
The software architecture of Varity is built strictly against the trend of bloated AI toolchains.
* **No Vendor SDKs:** We utilize raw asynchronous `httpx` to interface directly with Anthropic, OpenAI, and Google Gemini REST endpoints. This mitigates dependency hell, removes thousands of bloatware sub-dependencies from the user's ultimate Docker images, and ensures the package is phenomenally lightweight.
* **Strict BYOK (Bring Your Own Key):** Enterprise clients cannot risk third-party routing. Varity does not use middle-man telemetry servers. The API key is stored securely in the local environment and passed strictly to the host provider. Zero proprietary data ever touches our systems.
