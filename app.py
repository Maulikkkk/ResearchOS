import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchOS · AI Research Engine",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=IBM+Plex+Mono:wght@300;400;500&family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    color: #dde6f0;
}

.stApp {
    background: #080e18;
    background-image:
        radial-gradient(ellipse 70% 55% at 5% 15%, rgba(32,180,170,0.09) 0%, transparent 60%),
        radial-gradient(ellipse 55% 45% at 95% 85%, rgba(60,100,200,0.08) 0%, transparent 55%),
        url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%231a2a40' fill-opacity='0.35'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.hero-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #20b4aa;
    margin-bottom: 1.2rem;
    opacity: 0.85;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 700;
    font-style: italic;
    line-height: 1.05;
    letter-spacing: -0.01em;
    color: #eef3fa;
    margin: 0 0 1rem;
}
.hero h1 span {
    color: #20b4aa;
    font-style: normal;
    font-weight: 600;
}
.hero-sub {
    font-size: 1rem;
    font-weight: 300;
    color: #7a92ab;
    width: 100%;
    max-width: 580px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.85;
    text-align: center;
    display: block;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(32,180,170,0.25), rgba(60,100,200,0.2), transparent);
    margin: 2rem 0;
}

/* ── Input card ── */
.input-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(32,180,170,0.12);
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 1px 40px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.04);
}

/* ── Streamlit input overrides ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(32,180,170,0.2) !important;
    border-radius: 8px !important;
    color: #eef3fa !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 0.98rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #20b4aa !important;
    box-shadow: 0 0 0 3px rgba(32,180,170,0.1) !important;
}
.stTextInput > label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: #20b4aa !important;
    font-weight: 500 !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #1a9e96 0%, #157a8a 100%) !important;
    color: #f0f8ff !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.75rem 2.2rem !important;
    cursor: pointer !important;
    transition: transform 0.15s, box-shadow 0.15s, opacity 0.15s !important;
    box-shadow: 0 4px 20px rgba(32,180,170,0.25), inset 0 1px 0 rgba(255,255,255,0.1) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(32,180,170,0.35) !important;
    opacity: 0.92 !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Pipeline step cards ── */
.step-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 1.4rem 1.7rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, background 0.3s;
}
.step-card.active {
    border-color: rgba(32,180,170,0.35);
    background: rgba(32,180,170,0.04);
}
.step-card.done {
    border-color: rgba(90,180,255,0.25);
    background: rgba(90,180,255,0.03);
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 10px 0 0 10px;
    background: rgba(255,255,255,0.04);
    transition: background 0.3s;
}
.step-card.active::before { background: #20b4aa; }
.step-card.done::before   { background: #5ab4ff; }

.step-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 0.3rem;
}
.step-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.66rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    color: #20b4aa;
    opacity: 0.65;
}
.step-title {
    font-family: 'Playfair Display', serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: #dde6f0;
}
.step-status {
    margin-left: auto;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.status-waiting  { color: #3a4a5c; }
.status-running  { color: #20b4aa; }
.status-done     { color: #5ab4ff; }

/* ── Result panels ── */
.result-panel {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 1.8rem 2rem;
    margin-top: 1rem;
    margin-bottom: 1.5rem;
}
.result-panel-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #20b4aa;
    margin-bottom: 1rem;
    padding-bottom: 0.7rem;
    border-bottom: 1px solid rgba(32,180,170,0.12);
}
.result-content {
    font-size: 0.9rem;
    line-height: 1.85;
    color: #8aa4bc;
    white-space: pre-wrap;
    font-family: 'IBM Plex Sans', sans-serif;
}

/* ── Report & feedback panels ── */
.report-panel {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(32,180,170,0.18);
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-top: 1rem;
    box-shadow: 0 2px 40px rgba(0,0,0,0.2);
}
.feedback-panel {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(90,180,255,0.18);
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-top: 1rem;
    box-shadow: 0 2px 40px rgba(0,0,0,0.2);
}
.panel-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    padding-bottom: 0.7rem;
}
.panel-label.teal {
    color: #20b4aa;
    border-bottom: 1px solid rgba(32,180,170,0.15);
}
.panel-label.blue {
    color: #5ab4ff;
    border-bottom: 1px solid rgba(90,180,255,0.15);
}

/* ── Progress text ── */
.stSpinner > div { color: #20b4aa !important; }

/* ── Expander ── */
details summary {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #7a92ab !important;
    letter-spacing: 0.1em !important;
    cursor: pointer;
}

/* ── Section heading ── */
.section-heading {
    font-family: 'Playfair Display', serif;
    font-size: 1.35rem;
    font-weight: 600;
    font-style: italic;
    color: #eef3fa;
    margin: 2rem 0 1rem;
}

/* ── Toast-style notice ── */
.notice {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #2a3a4c;
    text-align: center;
    margin-top: 3rem;
    letter-spacing: 0.1em;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",   "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div style='font-size:0.8rem;color:#4a6070;margin-top:0.3rem;'>"+desc+"</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">An Autonomous AI Research Engine</div>
    <h1><em>Research</em><span>OS</span></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate for searching, scraping, writing,
        and critiquing to deliver a polished research report on any topic.
    </p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Example chips
    st.markdown("""
    <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1.5rem;">
        <span style="font-family:'IBM Plex Mono',monospace;font-size:0.66rem;color:#3a4a5c;letter-spacing:0.12em;">TRY →</span>
    """, unsafe_allow_html=True)
    examples = ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]
    for ex in examples:
        st.markdown(f"""
        <span style="
            background:rgba(32,180,170,0.06);
            border:1px solid rgba(32,180,170,0.12);
            border-radius:5px;
            padding:0.25rem 0.7rem;
            font-size:0.73rem;
            color:#7a92ab;
            font-family:'IBM Plex Sans',sans-serif;
            cursor:default;
        ">{ex}</span>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)

    r = st.session_state.results
    done = st.session_state.done

    def s(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        idx = steps.index(step)
        completed = list(r.keys())
        # figure out which steps are done
        if step in r:
            return "done"
        # which step is running now (first not in r)
        if st.session_state.running:
            for i, k in enumerate(steps):
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Research Scout",  s("search"), "Discovers relevant real-time information")
    step_card("02", "Insight Extractor",  s("reader"), "Scrapes and extracts deep insights")
    step_card("03", "Research Composer",  s("writer"), "Builds structured research reports")
    step_card("04", "Quality Reviewer",  s("critic"), "Evaluates accuracy and report quality")


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ──
    with st.spinner("🔍  Search Agent is working…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)
    st.rerun() if False else None   # keep inline for now

    # ── Step 2: Reader ──
    with st.spinner("📄  Reader Agent is scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 3: Writer ──
    with st.spinner("✍️  Writer is drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    # ── Step 4: Critic ──
    with st.spinner("🧐  Critic is reviewing the report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    # Raw outputs in expanders
    if "search" in r:
        with st.expander("🔍 Search Results (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Search Agent Output</div>'
                        f'<div class="result-content">{r["search"]}</div></div>', unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("📄 Scraped Content (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Reader Agent Output</div>'
                        f'<div class="result-content">{r["reader"]}</div></div>', unsafe_allow_html=True)

    # Final report
    if "writer" in r:
        st.markdown("""
        <div class="report-panel">
            <div class="panel-label teal">📝 Final Research Report</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])   # render markdown natively
        st.markdown("</div>", unsafe_allow_html=True)

        # Download
        st.download_button(
            label="⬇  Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic feedback
    if "critic" in r:
        st.markdown("""
        <div class="feedback-panel">
            <div class="panel-label blue">🧐 Critic Feedback</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    ResearchOS · Powered by LangChain · Multi-Agent Pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)