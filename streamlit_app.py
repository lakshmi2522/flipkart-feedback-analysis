import re
from collections import Counter
import streamlit as st

st.set_page_config(
    page_title="Flipkart Feedback Insights",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: Inter, sans-serif; }
.stApp {
    background: linear-gradient(135deg, #f7f9ff 0%, #eef4ff 48%, #f8fbff 100%);
    color: #172033;
}
.block-container { max-width: 1180px; padding-top: 1.5rem; padding-bottom: 3rem; }
.hero {
    background: linear-gradient(120deg, #172554 0%, #1d4ed8 58%, #2563eb 100%);
    color: white; padding: 2.1rem 2.2rem; border-radius: 24px;
    box-shadow: 0 18px 45px rgba(37, 99, 235, .18); margin-bottom: 1.4rem;
}
.hero-kicker { color: #bfdbfe; text-transform: uppercase; letter-spacing: .15em; font-size: .75rem; font-weight: 800; }
.hero h1 { color: white; font-size: clamp(2rem, 4vw, 3.1rem); line-height: 1.1; margin: .5rem 0; }
.hero p { color: #dbeafe; font-size: 1rem; max-width: 720px; margin-bottom: 0; }
.pill {
    display: inline-block; background: rgba(255,255,255,.14); border: 1px solid rgba(255,255,255,.25);
    color: white; border-radius: 99px; padding: .35rem .75rem; font-size: .8rem; margin-top: 1rem;
}
.panel {
    background: white; border: 1px solid #e3eaf7; border-radius: 20px; padding: 1.25rem 1.4rem;
    box-shadow: 0 8px 28px rgba(31, 55, 100, .06); margin-bottom: 1rem;
}
.section-label { color: #2563eb; text-transform: uppercase; letter-spacing: .12em; font-size: .72rem; font-weight: 800; }
.panel h3 { margin-top: .25rem; color: #172033; }
.small-note { color: #64748b; font-size: .88rem; }
div[data-testid="stMetric"] {
    background: white; border: 1px solid #e3eaf7; padding: 1rem 1.1rem; border-radius: 16px;
    box-shadow: 0 6px 20px rgba(31, 55, 100, .05);
}
div[data-testid="stMetricLabel"] { color: #64748b; }
div[data-testid="stMetricValue"] { color: #1d4ed8; font-weight: 800; }
.stButton > button, .stFormSubmitButton > button {
    background: linear-gradient(90deg, #2563eb, #1d4ed8); color: white; border: 0;
    border-radius: 12px; min-height: 2.8rem; font-weight: 700; width: 100%;
}
.stButton > button:hover, .stFormSubmitButton > button:hover { color: white; border: 0; filter: brightness(1.06); }
div[data-baseweb="input"] > div, div[data-baseweb="textarea"] > div { border-radius: 10px; }
.footer { text-align: center; color: #64748b; font-size: .82rem; padding: 1.2rem 0 .2rem; }
</style>
""", unsafe_allow_html=True)

def analyze_feedback(name, feedback, keyword):
    words = re.findall(r"\b[\w']+\b", feedback, flags=re.UNICODE)
    char_count = len(feedback)
    word_count = len(words)
    occurrences = feedback.lower().count(keyword.strip().lower()) if keyword.strip() else 0
    return char_count, word_count, occurrences, words

if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""
if "feedback" not in st.session_state:
    st.session_state.feedback = ""
if "keyword" not in st.session_state:
    st.session_state.keyword = ""

st.markdown("""
<div class="hero">
  <div class="hero-kicker">Customer Experience · Feedback Toolkit</div>
  <h1>Flipkart Feedback Insights</h1>
  <p>Turn customer comments into simple, useful insights. Check feedback length, count words, and find how often a keyword appears — all in one clean workspace.</p>
  <div class="pill">⚡ Fast analysis &nbsp; · &nbsp; 🔒 Processed in this session</div>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1.12, .88], gap="large")

with left:
    st.markdown('<div class="panel"><div class="section-label">01 / Enter feedback</div><h3>Customer feedback</h3><p class="small-note">Enter a customer name, a feedback message (up to 500 characters), and an optional keyword to search.</p></div>', unsafe_allow_html=True)
    with st.form("feedback_form"):
        customer_name = st.text_input("Customer name", value=st.session_state.customer_name, placeholder="e.g., Rahul Sharma")
        feedback = st.text_area(
            "Feedback message",
            value=st.session_state.feedback,
            height=185,
            max_chars=500,
            placeholder="Write the customer's feedback here...",
            help="Feedback must contain 1–500 characters."
        )
        keyword = st.text_input("Keyword to search (optional)", value=st.session_state.keyword, placeholder="e.g., quality")
        submitted = st.form_submit_button("Analyze feedback  →", use_container_width=True)
    if submitted:
        if not customer_name.strip():
            st.error("Please enter the customer name.")
            st.session_state.analysis = None
        elif not feedback.strip():
            st.error("Please enter a feedback message.")
            st.session_state.analysis = None
        elif len(feedback) > 500:
            st.error("Feedback must be 500 characters or fewer.")
            st.session_state.analysis = None
        else:
            st.session_state.customer_name = customer_name.strip()
            st.session_state.feedback = feedback
            st.session_state.keyword = keyword
            result = analyze_feedback(customer_name, feedback, keyword)
            st.session_state.analysis = {
                "name": customer_name.strip(),
                "feedback": feedback,
                "keyword": keyword.strip(),
                "chars": result[0],
                "words": result[1],
                "occurrences": result[2],
            }

with right:
    st.markdown('<div class="panel"><div class="section-label">Quick start</div><h3>Try a sample</h3><p class="small-note">Fill the form with a ready-made example to see how the analyzer works.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="panel"><b>😊 Positive experience</b><p class="small-note">The product quality is excellent. The delivery was fast and the packaging was good. I am happy with the product quality and fast delivery.</p><b>Search keyword:</b> <code>quality</code></div>', unsafe_allow_html=True)
    if st.button("Use sample input", use_container_width=True):
        st.session_state.customer_name = "Rahul Sharma"
        st.session_state.feedback = "The product quality is excellent. The delivery was fast and the packaging was good. I am happy with the product quality and fast delivery."
        st.session_state.keyword = "quality"
        st.rerun()
    st.markdown('<div class="panel"><b>What this tool calculates</b><p class="small-note">Character count · Word count · Case-insensitive keyword matches · Feedback validation</p></div>', unsafe_allow_html=True)

analysis = st.session_state.analysis
if analysis:
    st.markdown("---")
    st.markdown('<div class="section-label">02 / Analysis report</div><h2 style="margin-top:.25rem;">Feedback analysis</h2>', unsafe_allow_html=True)
    st.markdown(f'<div class="panel"><div class="small-note">CUSTOMER</div><h3 style="margin:.2rem 0 .5rem;">{analysis["name"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")}</h3><div>{analysis["feedback"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")}</div></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Characters", analysis["chars"])
    c2.metric("Words", analysis["words"])
    c3.metric("Keyword matches", analysis["occurrences"])
    if analysis["keyword"]:
        st.success(f'Keyword **“{analysis["keyword"]}”** appeared **{analysis["occurrences"]}** time(s), ignoring uppercase/lowercase differences.')
    else:
        st.info("No keyword was entered, so keyword matching was skipped.")
    st.caption("Note: keyword matching counts substring occurrences, so a keyword can also match inside a longer word. Results are not saved to a database.")
else:
    st.markdown('<div class="panel"><div class="section-label">02 / Analysis report</div><h3>Your results will appear here</h3><p class="small-note">Submit the form to generate the customer feedback report with character count, word count, and keyword matches.</p></div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Student project demo · Not an official Flipkart service · Feedback is analyzed but not permanently stored</div>', unsafe_allow_html=True)
