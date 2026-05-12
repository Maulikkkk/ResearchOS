<div align="center">

# 🔬 ResearchOS

**An autonomous multi-agent AI research engine that searches, reads, writes, and critically reviews — so you don't have to.**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-green)](https://langchain.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?logo=streamlit)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Features](#-features) · [How It Works](#-how-it-works) · [Tech Stack](#-tech-stack) · [Installation](#-installation) · [Usage](#-usage) · [Roadmap](#-roadmap)

</div>

---

## 🧠 What Is ResearchOS?

ResearchOS is a fully autonomous research assistant built on a **multi-agent LangChain pipeline**. Give it any topic, and it autonomously searches the web, scrapes and reads relevant pages, writes a structured research report, and then critiques its own output — all in real time through a clean Streamlit interface.

No manual Googling. No copy-pasting. Just research, delivered.

---

## ✨ Features

- 🤖 **Multi-Agent Workflow** — Dedicated agents for searching, reading, writing, and reviewing
- 🌐 **Real-Time Web Intelligence** — Live search powered by Tavily API
- 📄 **Deep Web Scraping** — Full page content extraction via BeautifulSoup
- ✍️ **AI Report Generation** — Structured, coherent reports written by a dedicated writer agent
- 🧐 **Built-In AI Critic** — A separate critic agent reviews and scores the report for quality
- ⚡ **Live Workflow Execution** — Watch agents run step-by-step in real time
- 📥 **Export Options** — Download reports as Markdown or DOCX

---

## 🔄 How It Works

ResearchOS chains four specialized agents in sequence, each with a focused role:

```
 User Input
     │
     ▼
┌─────────────────┐
│  Search Agent   │  ← Queries Tavily for top relevant sources
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Reader Agent   │  ← Scrapes & extracts content from each source
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Writer Agent   │  ← Synthesizes findings into a structured report
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Critic Agent   │  ← Reviews the report for accuracy & completeness
└────────┬────────┘
         │
         ▼
  Final Research Report
```

Each agent is independently prompted and powered by Groq/Mistral, enabling fast, parallelizable inference.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Agent Framework | [LangChain](https://langchain.com) |
| LLM Inference | [Groq API](https://groq.com) + [Mistral AI](https://mistral.ai) |
| Web Search | [Tavily Search API](https://tavily.com) |
| Web Scraping | [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) |
| UI | [Streamlit](https://streamlit.io) |
| Language | Python 3.10+ |

---

## 📦 Installation

### Prerequisites

- Python 3.10+
- A [Groq API key](https://console.groq.com)
- A [Tavily API key](https://app.tavily.com)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/Maulikkkk/ResearchOS.git
cd ResearchOS

# 2. Create and activate a virtual environment
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

---

## ▶️ Usage

```bash
streamlit run app.py
```

Then open your browser at `http://localhost:8501`, enter a research topic, and watch the agents go to work.

---

## 📸 Screenshots

> _Screenshots coming soon — contributions welcome!_

---

## 🗺️ Roadmap

- [ ] Memory-enabled agents with conversation history
- [ ] Multi-source synthesis with citation tracking
- [ ] PDF export
- [ ] AI reasoning loops for deeper analysis
- [ ] Vector database integration for persistent knowledge
- [ ] Autonomous deep research mode (recursive sub-queries)
- [ ] Configurable agent personas and report formats

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to open an [issue](https://github.com/Maulikkkk/ResearchOS/issues) or submit a pull request.

---

## 👨‍💻 Author

**Maulik Gupta**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://www.linkedin.com/in/maulikg29)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?logo=github)](https://github.com/Maulikkkk)

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
