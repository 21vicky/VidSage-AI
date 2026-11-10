import re
from urllib.parse import parse_qs, urlparse

import streamlit as st

from transcript import get_transcript
from summarizer import summarize_transcript


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="VidSage AI | Video Intelligence",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# SESSION STATE
# =========================================================

DEFAULT_STATE = {
    "summary": None,
    "transcript": None,
    "video_url": "",
    "video_id": None,
    "video_url_input": "",
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #080b16;
    --purple: #9575ff;
    --text: #f5f3ff;
    --muted: #9aa4bd;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 50% -15%, rgba(112, 74, 220, 0.22), transparent 45%),
        linear-gradient(145deg, #080b16, #101329 65%, #0b1020);
    color: var(--text);
}

.block-container {
    max-width: 1050px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* Header */
.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    padding: 10px 0 20px;
    border-bottom: 1px solid rgba(255,255,255,.08);
}

.brand {
    font-size: 20px;
    font-weight: 800;
    color: white;
    letter-spacing: -1px;
}

.brand span {
    color: #a78bfa;
}

.status {
    color: #c4b5fd;
    background: rgba(139,92,246,.12);
    border: 1px solid rgba(167,139,250,.25);
    border-radius: 30px;
    padding: 7px 14px;
    font-size: 11px;
    font-weight: 600;
}

/* Hero */
.hero {
    text-align: center;
    padding: 65px 10px 35px;
}

.hero-badge {
    display: inline-block;
    padding: 8px 16px;
    border-radius: 30px;
    background: rgba(139,92,246,.12);
    border: 1px solid rgba(167,139,250,.25);
    color: #c4b5fd;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 23px;
}

.hero h1 {
    font-size: clamp(38px, 6vw, 64px);
    font-weight: 800;
    letter-spacing: -3px;
    line-height: 1.12;
    margin: 0;
    color: #ffffff;
}

.gradient-text {
    background: linear-gradient(90deg, #a78bfa, #818cf8, #c4b5fd);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #a0a8c0;
    font-size: 16px;
    line-height: 1.8;
    margin-top: 20px;
}

/* Input form */
.input-heading {
    color: #f5f3ff;
    font-size: 20px;
    font-weight: 700;
    margin: 15px 0 7px;
}

.input-subheading {
    color: #929bb5;
    font-size: 13px;
    margin-bottom: 15px;
}

div[data-testid="stForm"] {
    background: linear-gradient(145deg, rgba(255,255,255,.055), rgba(255,255,255,.018));
    border: 1px solid rgba(167,139,250,.22);
    border-radius: 20px;
    padding: 22px;
    box-shadow: 0 20px 70px rgba(0,0,0,.20);
}

div[data-testid="stTextInput"] input {
    background: #0d1325;
    border: 1px solid #343d5b;
    border-radius: 12px;
    color: white;
    min-height: 48px;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #a78bfa;
    box-shadow: 0 0 0 1px #a78bfa;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button,
.stDownloadButton > button {
    border: 1px solid rgba(167,139,250,.25);
    border-radius: 12px;
    min-height: 46px;
    font-weight: 700;
    color: white;
    background: linear-gradient(100deg, #7655e9, #9b72f5);
    transition: all .2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover,
.stDownloadButton > button:hover {
    color: white;
    border-color: #c4b5fd;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(139,92,246,.25);
}

/* Metrics */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(167,139,250,.17);
    border-radius: 15px;
    padding: 18px;
}

div[data-testid="stMetricLabel"] {
    color: #a5afc5;
}

div[data-testid="stMetricValue"] {
    color: white;
    font-weight: 800;
}

/* Result and feature cards */
.result-heading {
    color: #e9e2ff;
    font-size: 22px;
    font-weight: 750;
    margin: 30px 0 15px;
}

.summary-box {
    background: rgba(255,255,255,.035);
    border: 1px solid rgba(167,139,250,.20);
    border-radius: 18px;
    padding: 22px 25px;
    line-height: 1.85;
}

.feature-card {
    background: rgba(255,255,255,.035);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 16px;
    padding: 19px;
    min-height: 125px;
}

.feature-card h4 {
    color: #eeeaff;
    margin: 0 0 8px 0;
    font-size: 15px;
}

.feature-card p {
    color: #939bb5;
    font-size: 12px;
    line-height: 1.7;
    margin: 0;
}

.helper-note {
    color: #8792ad;
    font-size: 12px;
    text-align: center;
    margin-top: 10px;
}

/* Footer */
.footer {
    text-align: center;
    color: #727d99;
    font-size: 12px;
    border-top: 1px solid rgba(255,255,255,.08);
    padding-top: 25px;
    margin-top: 65px;
}

/* Hide Streamlit chrome */
#MainMenu, footer, [data-testid="stDecoration"] {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

@media (max-width: 640px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .hero {
        padding-top: 42px;
    }
    .hero h1 {
        letter-spacing: -1.5px;
    }
    .status {
        font-size: 9px;
        padding: 6px 9px;
    }
    div[data-testid="stForm"] {
        padding: 15px;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def extract_youtube_video_id(url: str):
    """Return the 11-character YouTube video ID, or None."""
    try:
        parsed = urlparse(url.strip())
        host = (parsed.hostname or "").lower()

        allowed_hosts = {
            "youtube.com",
            "www.youtube.com",
            "m.youtube.com",
            "youtu.be",
            "www.youtu.be",
        }

        if host not in allowed_hosts:
            return None

        if host in {"youtu.be", "www.youtu.be"}:
            video_id = parsed.path.strip("/").split("/")[0]

        elif parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [""])[0]

        elif parsed.path.startswith("/shorts/"):
            parts = parsed.path.strip("/").split("/")
            video_id = parts[1] if len(parts) > 1 else ""

        elif parsed.path.startswith("/embed/"):
            parts = parsed.path.strip("/").split("/")
            video_id = parts[1] if len(parts) > 1 else ""

        else:
            return None

        return video_id if re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id) else None

    except (TypeError, ValueError):
        return None


def normalize_youtube_url(video_id: str) -> str:
    """Build a standard YouTube URL from a validated video ID."""
    return f"https://www.youtube.com/watch?v={video_id}"


def reset_results():
    st.session_state.summary = None
    st.session_state.transcript = None
    st.session_state.video_url = ""
    st.session_state.video_id = None
    st.session_state.video_url_input = ""


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
<div class="topbar">
    <div class="brand">🎬 VidSage<span> AI</span></div>
    <div class="status">✦ AI POWERED VIDEO INTELLIGENCE</div>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# HERO SECTION
# =========================================================

st.markdown(
    """
<div class="hero">
    <div class="hero-badge">✨ YOUR PERSONAL AI VIDEO ASSISTANT</div>
    <h1>
        Watch Less.<br>
        <span class="gradient-text">Understand More.</span>
    </h1>
    <p>
        Turn lengthy YouTube videos into clear, intelligent summaries.<br>
        Save time, capture insights and focus on what matters.
    </p>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# INPUT SECTION
# =========================================================

st.markdown(
    """
<div class="input-heading">🔗 Summarize any YouTube video</div>
<div class="input-subheading">
    Paste a public YouTube video link below to get started.
</div>
""",
    unsafe_allow_html=True,
)

with st.form("video_form", clear_on_submit=False):
    video_url_input = st.text_input(
        "YouTube Video URL",
        placeholder="https://www.youtube.com/watch?v=...",
        help="Supported formats: youtube.com/watch, youtu.be, YouTube Shorts and embed links.",
        key="video_url_input",
    )

    generate = st.form_submit_button(
        "✨ Generate AI Summary",
        use_container_width=True,
    )

st.markdown(
    '<div class="helper-note">🔒 Your video is processed for this summary. '
    'Only videos with an available transcript can be summarized.</div>',
    unsafe_allow_html=True,
)


# =========================================================
# GENERATE SUMMARY
# =========================================================

if generate:
    video_id = extract_youtube_video_id(video_url_input)

    if not video_url_input.strip():
        st.warning("Please paste a YouTube video URL first.")

    elif not video_id:
        st.error("That YouTube link doesn't look valid. Please check the URL and try again.")

    else:
        normalized_url = normalize_youtube_url(video_id)

        # Clear any previous result before processing a new video.
        st.session_state.summary = None
        st.session_state.transcript = None
        st.session_state.video_url = normalized_url
        st.session_state.video_id = video_id

        try:
            with st.status("🎧 Extracting video transcript...", expanded=True) as status:
                transcript = get_transcript(normalized_url)

                if not isinstance(transcript, str) or not transcript.strip():
                    raise ValueError("No transcript was returned for this video.")

                if (
                    transcript == "Invalid YouTube URL"
                    or transcript.startswith("Transcript extraction failed")
                ):
                    raise ValueError(transcript)

                status.update(
                    label="Transcript extracted successfully!",
                    state="complete",
                    expanded=False,
                )

            with st.status("🧠 AI is analyzing your video...", expanded=True) as status:
                summary = summarize_transcript(transcript)

                if not isinstance(summary, str) or not summary.strip():
                    raise ValueError("The AI returned an empty summary.")

                if summary.startswith("Gemini API Error"):
                    raise ValueError(summary)

                status.update(
                    label="AI analysis completed!",
                    state="complete",
                    expanded=False,
                )

            st.session_state.transcript = transcript
            st.session_state.summary = summary
            st.success("🎉 Your video summary is ready!")

        except Exception as error:
            st.error(f"Unable to generate the summary: {error}")


# =========================================================
# DISPLAY RESULTS
# =========================================================

if st.session_state.summary and st.session_state.transcript:
    transcript = st.session_state.transcript
    summary = st.session_state.summary
    current_url = st.session_state.video_url

    st.markdown(
        '<div class="result-heading">📊 Video Insights</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Transcript Characters", f"{len(transcript):,}")

    with col2:
        st.metric("Characters Analyzed", f"{min(len(transcript), 3000):,}")

    with col3:
        st.metric("Summary Characters", f"{len(summary):,}")

    if len(transcript) > 3000:
        st.info(
            "This version analyzes the first 3,000 transcript characters. "
            "We'll add full-video chunk processing in a later upgrade."
        )

    st.markdown(
        '<div class="result-heading">🎬 Video Preview</div>',
        unsafe_allow_html=True,
    )
    st.video(current_url)

    st.markdown(
        '<div class="result-heading">🧠 Your AI Summary</div>',
        unsafe_allow_html=True,
    )

    # Use a real Streamlit container so the summary content stays inside the card.
    with st.container(border=True):
        st.markdown(summary)

    st.markdown(
        '<div class="result-heading">📥 Export Your Summary</div>',
        unsafe_allow_html=True,
    )

    download_col1, download_col2 = st.columns(2)

    with download_col1:
        st.download_button(
            "⬇️ Download TXT",
            data=summary,
            file_name="VidSage_AI_Summary.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with download_col2:
        st.download_button(
            "⬇️ Download Markdown",
            data=summary,
            file_name="VidSage_AI_Summary.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with st.expander("📄 View Original Transcript"):
        st.text_area(
            "Extracted Transcript",
            value=transcript,
            height=300,
            disabled=True,
        )

    if st.button("🔄 Summarize Another Video", use_container_width=True):
        reset_results()
        st.rerun()


# =========================================================
# FEATURES
# =========================================================

if not st.session_state.summary:
    st.markdown(
        '<div class="result-heading" style="text-align:center;">'
        'Why VidSage AI?</div>',
        unsafe_allow_html=True,
    )

    feature1, feature2, feature3 = st.columns(3)

    with feature1:
        st.markdown(
            """
<div class="feature-card">
    <h4>⚡ Save Time</h4>
    <p>Get the important information without watching lengthy videos from beginning to end.</p>
</div>
""",
            unsafe_allow_html=True,
        )

    with feature2:
        st.markdown(
            """
<div class="feature-card">
    <h4>🧠 AI Intelligence</h4>
    <p>Transform video transcripts into structured, easy-to-understand insights.</p>
</div>
""",
            unsafe_allow_html=True,
        )

    with feature3:
        st.markdown(
            """
<div class="feature-card">
    <h4>📥 Easy Export</h4>
    <p>Download your summaries and keep useful knowledge accessible anytime.</p>
</div>
""",
            unsafe_allow_html=True,
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
<div class="footer">
    <p>Built with ❤️ using Python, Streamlit & Gemini AI</p>
    <p>VidSage AI · Understand More. Watch Less.</p>
    <p>© 2026 VidSage AI. All rights reserved.</p>
</div>
""",
    unsafe_allow_html=True,
)
