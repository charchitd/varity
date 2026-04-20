Here is the final draft for your LinkedIn post. It strikes the perfect balance between serious AI research, nerdy humor, and engaging formatting!

***

🚀 **If an LLM hallucinates in a server forest, and no one is around to fact-check it, is it still "highly confident"?** 

Spoiler: Yes. Yes it is. 🤦‍♂️

As AI researchers, we've all been there. You ask an LLM for historical facts, and it confidently tells you that Abraham Lincoln invented the iPhone in 1864. 

This happens because modern LLMs are statistical parrots—they prioritize token likelihood over factual truth. Sure, Retrieval-Augmented Generation (RAG) is great... until your vector database goes stale.

That’s why I’m incredibly excited to finally open-source **Varity v0.1**! 🔍

Varity is a zero-dependency Python library that uses the LLM’s own latent space against itself to mathematically filter out hallucinations using what we call the **Verdict Stability Score (VSS)**.

**🧠 How it works (The nerdy stuff):**
Recent literature (Manakul et al. & Dhuliawala et al., 2023) has shown that LLMs possess a hidden, latent ability for self-critique. Varity weaponizes this by forcing the LLM into a rigorous "Recursive Verification Loop." 

1️⃣ First, Varity slices a long-winded response into atomic claims.
2️⃣ Then, it cross-examines the LLM on each claim in isolated, recursive passes (Depth-N interrogation). 
3️⃣ Hallucinatory claims are chemically unstable—under pressure, the LLM will contradict itself and "flip." True facts remain rock solid.
4️⃣ Varity tracks these algorithmic flips to calculate the VSS. High VSS = stable fact. Low VSS = confident hallucination.

Basically, Varity acts like a strict math teacher making the LLM "show its work." 🧐

**📊 The Benchmark Results:**
Against a rigorous test dataset of common AI misconceptions (`gpt-4o-mini` via OpenRouter), Varity achieved:
✅ **100% Detection Accuracy** (Caught every single hallucination)
✅ **0% False Positive Rate** 
✅ **Average VSS on Facts: 100%**

Whether you are building high-stakes autonomous agents, medical AI writers, or automated academic fact-checkers, Varity serves as the ultimate "sanity middleware." And it supports OpenAI, Google Gemini, and Anthropic Claude right out of the box (with zero telemetry—your keys are totally safe). 🔒

Check out the interactive demo below, and let's make our AIs a little less confidently wrong. 👇

📦 **PyPI**: `pip install varity`  
🎮 **Interactive BYOK Demo**: https://charchitd.github.io/Varity-v0.1/  
📄 **Academic Whitepaper**: Check out `docs/CONCEPTS.md` in the repo 

Part of our ongoing research at Aston University on GenAI reliability. If you're tackling LLM evaluations, I’d love to hear your thoughts! Drop a comment below. 👇

#MachineLearning #LLMs #AI #Python #Hallucination #Research #NLP #OpenSource #GenAI #AstonUniversity
