import streamlit as st
import time
from dotenv import load_dotenv
from utilities.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
   # Line 14
    page_title="AI Video Assistant" ,
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Design System ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500;600&family=Inter:wght@400;500;600&display=swap');

:root {
    --bg: #071410;
    --surface: #0e2019;
    --surface-hover: #142a21;
    --surface-2: #17332a;
    --border: #234437;
    --border-soft: #17332a;
    --accent: #10b981;
    --accent-glow: #34d399;
    --accent-2: #f59e0b;
    --accent-pink: #fb923c;
    --text: #f3f4f6;
    --text-muted: #8fa89c;
    --text-dim: #567366;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --radius: 16px;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: var(--bg) !important; color: var(--text) !important; }

/* Ambient background glow */
.stApp::before {
    content: ''; position: fixed; top: -15%; left: -8%;
    width: 55vw; height: 55vh;
    background: radial-gradient(circle, rgba(16,185,129,0.10) 0%, transparent 70%);
    pointer-events: none; z-index: 0;
}
.stApp::after {
    content: ''; position: fixed; bottom: -15%; right: -8%;
    width: 55vw; height: 55vh;
    background: radial-gradient(circle, rgba(245,158,11,0.07) 0%, transparent 70%);
    pointer-events: none; z-index: 0;
}

/* Hide default streamlit chrome noise */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; max-width: 1200px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #05100c !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}

/* ── Typography ── */
h1, h2, h3, h4, h5, h6 { font-family: 'Syne', sans-serif !important; color: var(--text) !important; letter-spacing: -0.02em; }

.eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem; letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--accent-glow); font-weight: 600; margin-bottom: 0.35rem;
    display: flex; align-items: center; gap: 0.4rem;
}
.hero-title {
    font-family: 'Syne', sans-serif; font-size: clamp(1.7rem, 3vw, 2.5rem);
    font-weight: 800; line-height: 1.12; margin: 0;
    background: linear-gradient(135deg, #ffffff 0%, var(--accent-glow) 55%, var(--accent-2) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-sub { font-size: 0.88rem; color: var(--text-muted); margin-top: 0.5rem; max-width: 560px; line-height: 1.55; }

/* ── Stat pills (top metrics row) ── */
.stat-row { display: flex; gap: 0.75rem; flex-wrap: wrap; margin: 1.3rem 0 1.6rem 0; }
.stat-pill {
    flex: 1; min-width: 150px;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 14px; padding: 0.9rem 1.1rem;
    position: relative; overflow: hidden;
}
.stat-pill::before {
    content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 2.5px;
    background: linear-gradient(90deg, var(--accent), var(--accent-2));
}
.stat-label { font-size: 0.62rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-dim); font-weight: 600; }
.stat-value { font-family: 'Syne', sans-serif; font-size: 1.35rem; font-weight: 700; color: var(--text); margin-top: 0.15rem; }

/* ── Cards ── */
.card {
    background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
    padding: 1.3rem 1.4rem; margin-bottom: 1rem; position: relative; overflow: hidden;
    box-shadow: 0 10px 30px -12px rgba(0,0,0,0.55); transition: all 0.25s ease;
}
.card:hover { border-color: var(--accent); box-shadow: 0 14px 35px -10px rgba(139,92,246,0.18); }
.card::before {
    content: ''; position: absolute; top: 0; left: 0; width: 3px; height: 100%;
    background: linear-gradient(180deg, var(--accent), var(--accent-2));
}
.card-title {
    font-family: 'Syne', sans-serif; font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-muted);
    margin-bottom: 0.8rem; display: flex; align-items: center; justify-content: space-between; gap: 0.4rem;
}
.card-content { font-size: 0.87rem; line-height: 1.75; color: var(--text); }
.count-chip {
    font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; font-weight: 600;
    background: var(--surface-2); border: 1px solid var(--border); border-radius: 20px;
    padding: 0.1rem 0.55rem; color: var(--text-muted);
}

/* ── Badges ── */
.badge { display: inline-block; padding: 0.22rem 0.6rem; border-radius: 6px; font-size: 0.62rem; font-weight: 600; letter-spacing: 0.07em; text-transform: uppercase; }
.badge-purple { background: rgba(139,92,246,0.15); color: var(--accent-glow); border: 1px solid rgba(139,92,246,0.35); }
.badge-cyan   { background: rgba(6,182,212,0.12);  color: var(--accent-2);    border: 1px solid rgba(6,182,212,0.3); }
.badge-green  { background: rgba(16,185,129,0.12); color: var(--success);    border: 1px solid rgba(16,185,129,0.3); }

/* ── Inputs & Buttons ── */
.stTextInput > div > div > input, .stSelectbox > div > div {
    background: var(--surface-2) !important; border: 1px solid var(--border) !important;
    border-radius: 10px !important; color: var(--text) !important; font-size: 0.85rem !important;
    padding: 0.55rem 0.8rem !important;
}
.stTextInput > div > div > input:focus { border-color: var(--accent) !important; box-shadow: 0 0 0 2px rgba(139,92,246,0.25) !important; }

.stButton > button {
    background: linear-gradient(135deg, var(--accent), #7c3aed) !important; color: white !important;
    border: none !important; border-radius: 10px !important; font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important; font-size: 0.8rem !important; letter-spacing: 0.04em !important;
    padding: 0.6rem 1.2rem !important; transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(139,92,246,0.3);
}
.stButton > button:hover { transform: translateY(-1.5px) !important; box-shadow: 0 8px 22px rgba(139,92,246,0.5) !important; }
.stButton > button[kind="secondary"] { background: var(--surface-2) !important; border: 1px solid var(--border) !important; box-shadow: none !important; }
.stDownloadButton > button {
    background: var(--surface-2) !important; color: var(--text) !important; border: 1px solid var(--border) !important;
    border-radius: 10px !important; font-size: 0.78rem !important; font-weight: 600 !important;
}

/* ── Chat (native st.chat_message wrapper polish) ── */
[data-testid="stChatMessage"] { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: 14px !important; }
.stChatInputContainer, [data-testid="stChatInput"] {
    background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: 14px !important;
}

/* Transcript box */
.transcript-box {
    background: var(--surface-2); border: 1px solid var(--border); border-radius: 12px;
    padding: 1.2rem; font-size: 0.82rem; line-height: 1.8; max-height: 480px; overflow-y: auto;
    color: var(--text-muted); white-space: pre-wrap; word-break: break-word;
    font-family: 'JetBrains Mono', monospace;
}

/* Scrollbars */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 6px; background-color: var(--surface); padding: 6px; border-radius: 12px; border: 1px solid var(--border); }
.stTabs [data-baseweb="tab"] { border-radius: 8px !important; color: var(--text-muted) !important; font-family: 'Syne', sans-serif !important; font-weight: 600 !important; font-size: 0.78rem !important; padding: 7px 16px !important; }
.stTabs [aria-selected="true"] { background-color: var(--surface-2) !important; color: var(--accent-glow) !important; border: 1px solid var(--border) !important; }

/* Divider */
hr { border-color: var(--border) !important; margin: 1.8rem 0 !important; }

/* Empty state */
.empty-hero {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    padding: 4.5rem 2rem; text-align: center; background: var(--surface); border: 1px dashed var(--border);
    border-radius: 20px; margin-top: 1rem;
}
.step-item { display: flex; align-items: flex-start; gap: 0.7rem; text-align: left; max-width: 320px; margin: 0 auto 0.8rem auto; }
.step-num {
    flex-shrink: 0; width: 22px; height: 22px; border-radius: 50%; background: var(--surface-2);
    border: 1px solid var(--border); color: var(--accent-glow); font-size: 0.68rem; font-weight: 700;
    display: flex; align-items: center; justify-content: center; font-family: 'JetBrains Mono', monospace;
}
</style>
""", unsafe_allow_html=True)

# ─── Session State Initialization ───────────────────────────────────────────────
for key, default in {
    "result": None,
    "chat_history": [],
    "pipeline_done": False,
    "run_count": 0,
    "show_deploy_panel": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ─── Sidebar Controls ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
    '<div class="hero-title" style="font-size:1.3rem">⚡ AI Video Assistant</div>',
    unsafe_allow_html=True)
                            
    st.markdown('<div class="eyebrow" style="margin-top:0.3rem">Video & Meeting Engine</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<span class="badge badge-purple">Source</span>', unsafe_allow_html=True)
    st.markdown("<div style='margin-top:0.5rem'></div>", unsafe_allow_html=True)
    source = st.text_input(
        "Input Source", placeholder="https://youtube.com/watch?v=... or file.mp4",
        label_visibility="collapsed",
    )

    st.markdown("<div style='margin-top:0.9rem'></div>", unsafe_allow_html=True)
    st.markdown('<span class="badge badge-cyan">Language</span>', unsafe_allow_html=True)
    st.markdown("<div style='margin-top:0.5rem'></div>", unsafe_allow_html=True)
    language = st.selectbox("Processing Language", ["english", "hinglish"], index=0, label_visibility="collapsed")

    st.markdown("<div style='margin-top:1.1rem'></div>", unsafe_allow_html=True)
    col_run, col_deploy = st.columns(2, gap="small")
    with col_run:
        run_btn = st.button("🚀 Run", use_container_width=True)
    with col_deploy:
        deploy_btn = st.button("🌐 Deploy", use_container_width=True, type="secondary")

    if deploy_btn:
        st.session_state.show_deploy_panel = True

    if st.session_state.get("show_deploy_panel"):
        st.markdown("""
        <div style="background:var(--surface-2);border:1px solid var(--border);border-radius:10px;
                    padding:0.8rem 0.9rem;margin-top:0.6rem;font-size:0.74rem;line-height:1.7;color:var(--text-muted)">
            <div style="color:var(--accent-glow);font-weight:700;margin-bottom:0.3rem">Deploy NexusAI</div>
            1. Push this repo to GitHub<br>
            2. Go to <strong>share.streamlit.io</strong> → New app<br>
            3. Point it at <code>app.py</code><br>
            4. Add your <code>.env</code> secrets in App Settings
        </div>
        """, unsafe_allow_html=True)
        st.link_button("Open Streamlit Cloud ↗", "https://share.streamlit.io", use_container_width=True)

    with st.expander("💡 Tips"):
        st.markdown(
            "<div style='font-size:0.75rem;color:var(--text-muted);line-height:1.7'>"
            "• Paste a full YouTube URL or a local file path.<br>"
            "• Hinglish mode helps with mixed-language meetings.<br>"
            "• Use the chat tab to query specifics — timestamps, names, numbers."
            "</div>", unsafe_allow_html=True,
        )

    if st.session_state.pipeline_done:
        st.markdown("---")
        st.markdown('<span class="badge badge-green">Engine Status</span>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:0.75rem;color:var(--text-muted);line-height:1.8;margin-top:0.5rem">
            ✅ Audio Processing<br>
            ✅ Deep Transcription<br>
            ✅ Title Synthesis<br>
            ✅ Smart Summarization<br>
            ✅ Extraction Matrix<br>
            ✅ RAG Neural Vector Index
        </div>
        """, unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="eyebrow">⚡ AI Video Assistant</div>',
    unsafe_allow_html=True
)
st.markdown('<div class="hero-title">Video Intelligence Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Deep-dive transcription, structured insights, and interactive context chat — all from a single link or file.</div>', unsafe_allow_html=True)

# ── Run Pipeline with Live Progress ──────────────────────────────────────────────
if run_btn:
    if not source.strip():
        st.error("Please supply a valid YouTube URL or local file path.")
    else:
        st.session_state.pipeline_done = False
        st.session_state.result = None
        st.session_state.chat_history = []

        steps = [
            ("🔊 Extracting & processing audio chunks...", "audio"),
            ("📝 Running speech transcription engine...", "transcript"),
            ("🏷️ Synthesizing session title...", "title"),
            ("📋 Compiling executive summary...", "summary"),
            ("🔍 Extracting action items, decisions & questions...", "extraction"),
            ("🧠 Vectorizing text & building RAG search space...", "rag"),
        ]
        progress = st.progress(0, text=steps[0][0])

        try:
            chunks = process_input(source)
            progress.progress(1 / 6, text=steps[1][0])

            transcript = transcribe_all(chunks, language)
            progress.progress(2 / 6, text=steps[2][0])

            title = generate_title(transcript)
            progress.progress(3 / 6, text=steps[3][0])

            summary = summarize(transcript)
            progress.progress(4 / 6, text=steps[4][0])

            action_items = extract_action_items(transcript)
            decisions = extract_key_decisions(transcript)
            questions = extract_questions(transcript)
            progress.progress(5 / 6, text=steps[5][0])

            rag_chain = build_rag_chain(transcript)
            progress.progress(1.0, text="✅ Pipeline execution completed!")

            st.session_state.result = {
                "title": title,
                "transcript": transcript,
                "summary": summary,
                "action_items": action_items,
                "key_decisions": decisions,
                "open_questions": questions,
                "rag_chain": rag_chain,
            }
            st.session_state.pipeline_done = True
            st.session_state.run_count += 1
            time.sleep(0.4)
            st.rerun()

        except Exception as e:
            progress.empty()
            st.error(f"❌ Pipeline execution failed — {e}")

# ── Dashboard Results View ──────────────────────────────────────────────────────
if st.session_state.result:
    r = st.session_state.result

    def _count(text_block):
        return len(str(text_block).split())

    def _bullet_count(text_block):
        lines = [ln for ln in str(text_block).splitlines() if ln.strip()]
        return max(len(lines), 1)

    st.markdown("<div style='margin-top:0.5rem'></div>", unsafe_allow_html=True)

    # Stat row
    word_count = _count(r["transcript"])
    read_minutes = max(round(word_count / 140), 1)
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-pill">
            <div class="stat-label">Transcript Length</div>
            <div class="stat-value">{word_count:,} words</div>
        </div>
        <div class="stat-pill">
            <div class="stat-label">Est. Read Time</div>
            <div class="stat-value">{read_minutes} min</div>
        </div>
        <div class="stat-pill">
            <div class="stat-label">Action Items</div>
            <div class="stat-value">{_bullet_count(r['action_items'])}</div>
        </div>
        <div class="stat-pill">
            <div class="stat-label">Key Decisions</div>
            <div class="stat-value">{_bullet_count(r['key_decisions'])}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Title Card Banner
    st.markdown(f"""
    <div class="card">
        <div class="card-title">📌 Session Title</div>
        <div style="font-family:'Syne',sans-serif;font-size:1.25rem;font-weight:700;color:var(--text);letter-spacing:-0.01em;">
            {r['title']}
        </div>
    </div>""", unsafe_allow_html=True)

    # Core Content Layout
    tab_summary, tab_matrix, tab_transcript, tab_chat = st.tabs(
        ["📋 Summary", "⚡ Extraction Matrix", "📜 Transcript", "💬 Chat"]
    )

    with tab_summary:
        st.markdown("<div style='margin-top:0.8rem'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="card" style="border-left:none;">
            <div class="card-title">✨ Key Takeaways & Overview</div>
            <div class="card-content">{r['summary']}</div>
        </div>""", unsafe_allow_html=True)
        st.download_button("⬇ Download Summary (.txt)", r["summary"], file_name="summary.txt", use_container_width=False)

    with tab_matrix:
        st.markdown("<div style='margin-top:0.8rem'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3, gap="medium")
        with col1:
            st.markdown(f"""
            <div class="card">
                <div class="card-title" style="color:var(--success);">✅ Action Items <span class="count-chip">{_bullet_count(r['action_items'])}</span></div>
                <div class="card-content">{r['action_items']}</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="card">
                <div class="card-title" style="color:var(--accent-glow);">🔑 Key Decisions <span class="count-chip">{_bullet_count(r['key_decisions'])}</span></div>
                <div class="card-content">{r['key_decisions']}</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="card">
                <div class="card-title" style="color:var(--warning);">❓ Open Questions <span class="count-chip">{_bullet_count(r['open_questions'])}</span></div>
                <div class="card-content">{r['open_questions']}</div>
            </div>""", unsafe_allow_html=True)

    with tab_transcript:
        st.markdown("<div style='margin-top:0.8rem'></div>", unsafe_allow_html=True)
        st.markdown(f'<div class="transcript-box">{r["transcript"]}</div>', unsafe_allow_html=True)
        st.download_button("⬇ Download Transcript (.txt)", r["transcript"], file_name="transcript.txt")

    with tab_chat:
        st.markdown("<div style='margin-top:0.8rem'></div>", unsafe_allow_html=True)
        st.markdown(
            '<div style="font-size:0.8rem;color:var(--text-muted);margin-bottom:1rem">'
            'Query directly against your meeting transcript using embedded context vectors.</div>',
            unsafe_allow_html=True,
        )

        chat_container = st.container(height=420, border=True)
        with chat_container:
            if not st.session_state.chat_history:
                st.markdown("""
                <div style="text-align:center;padding:3rem 1rem;color:var(--text-muted);">
                    <div style="font-size:2rem;margin-bottom:0.4rem">🧠</div>
                    <div style="font-size:0.82rem">Ask something like "What are the core deliverables?" or "Summarize the timeline discussed."</div>
                </div>""", unsafe_allow_html=True)
            else:
                for msg in st.session_state.chat_history:
                    avatar = "🧑" if msg["role"] == "user" else "⚡"
                    with st.chat_message(msg["role"], avatar=avatar):
                        st.markdown(msg["content"])

        user_input = st.chat_input("Ask a question about the video…")
        c_clear = st.columns([5, 1])[1]
        with c_clear:
            if st.button("Clear chat", type="secondary", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()

        if user_input and user_input.strip():
            st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
            with st.spinner("Analyzing context vectors..."):
                answer = ask_question(r["rag_chain"], user_input.strip())
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.rerun()

else:
    # Empty state
    st.markdown("""
    <div class="empty-hero">
        <div style="font-size:2.8rem;margin-bottom:0.75rem">⚡</div>
        <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:700;color:var(--text);margin-bottom:0.5rem">
            Awaiting Source Input
        </div>
        <div style="color:var(--text-muted);font-size:0.8rem;max-width:400px;line-height:1.65;margin-bottom:1.6rem">
            Drop a YouTube URL or local file path into the sidebar, pick a language, and hit <strong>Run Pipeline</strong>.
        </div>
        <div style="margin-bottom:1.5rem">
            <div class="step-item"><div class="step-num">1</div><div>Paste your video source in the sidebar</div></div>
            <div class="step-item"><div class="step-num">2</div><div>Choose the processing language</div></div>
            <div class="step-item"><div class="step-num">3</div><div>Click Run Pipeline and explore the dashboard</div></div>
        </div>
        <div style="display:flex;gap:0.6rem;flex-wrap:wrap;justify-content:center">
            <span class="badge badge-purple">Speech-to-Text</span>
            <span class="badge badge-cyan">Structured Extraction</span>
            <span class="badge badge-green">RAG Vector Retrieval</span>
        </div>
    </div>""", unsafe_allow_html=True)