# BrandFlow-Studio-agent
An autonomous multi-agent creative system for generating brand identities and producing high-quality, SEO-optimized content at scale.
BrandFlow Studio blends creative intelligence with system engineering to automate brand creation, content drafting, editing, SEO optimization, and visual asset generation — all powered by a coordinated suite of LLM-driven agents and custom tools.

This project was built as a capstone for the Google x Kaggle 5-Day AI Agent Certification, demonstrating multi-agent orchestration, long-term memory, observability, tool integration, and evaluation in a real-world workflow.

BrandFlow Studio automates:

* Market Research
* Brand Identity Generation
* Blog Drafting
* Editing + Evaluation Loops
* SEO Optimization
* Visual Asset Creation (logos, thumbnails)
* Final Packaging & Report Generation

Powered by:

* **Google AI Studio (Gemini models)**
* **Multi‑Agent Architecture** (Research, Brand, Draft, Editor, SEO, Visual, Evaluator)
* **Custom Tools** (Search, Image Generation, Code Execution)
* **Sessions & Memory**
* **Observability Logging**
* **Long‑Running Editing Loops**

---

## 📁 Repository Structure

```
BrandFlowStudio/
│
├── agents/
│   ├── __init__.py
│   ├── research_agent.py
│   ├── brand_design_agent.py
│   ├── draft_agent.py
│   ├── editor_agent.py
│   ├── seo_agent.py
│   ├── visual_agent.py
│   └── evaluator_agent.py
│
├── tools/
│   ├── google_llm.py
│   ├── search.py
│   ├── image.py
│   ├── code_execution.py
│   └── tool_client.py
│
├── orchestrator/
│   ├── pipeline.py
│   ├── session.py
│   └── controller.py
│
├── notebooks/
│   └── brandflow_demo.ipynb  (Kaggle notebook placeholder)
│
├── main.py
├── README.md 
├── requirements.txt
└── .gitignore
```

---

## 🛠 Installation

### 1. Clone the repo

```bash
git clone https://github.com/yourname/BrandFlowStudio.git
cd BrandFlowStudio
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your Google AI Studio API key

```bash
export GOOGLE_API_KEY="your-key-here"
```

## 📬 Contact

If you want to collaborate, reach out anytime!
