import html
import os

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()

st.set_page_config(
    page_title="Reply Studio | Customer Support",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --ink: #172b3a;
        --muted: #687b88;
        --line: #e4ecec;
        --teal: #0c8477;
        --teal-dark: #07665d;
        --mint: #e9f6f2;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: var(--ink);
    }
    .stApp {
        background:
            radial-gradient(ellipse at 87% 1%, rgba(207, 239, 228, .42), transparent 28rem),
            #f6f8f7;
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] > div:first-child { padding-top: 1.5rem; }
    .block-container {
        max-width: 1200px;
        padding-top: 1.8rem;
        padding-bottom: 3.5rem;
    }
    h1, h2, h3 { font-family: 'Manrope', sans-serif; color: var(--ink); }
    .brand {
        display: flex;
        align-items: center;
        gap: .65rem;
        margin-bottom: 1.7rem;
        color: var(--ink);
        font-family: 'Manrope', sans-serif;
        font-size: 1.05rem;
        font-weight: 800;
        letter-spacing: -.04em;
    }
    .brand-mark {
        display: grid;
        width: 2rem;
        height: 2rem;
        place-items: center;
        border-radius: .7rem;
        background: var(--mint);
        color: var(--teal);
        font-size: 1.2rem;
    }
    .hero {
        position: relative;
        overflow: hidden;
        padding: 2.3rem 2.4rem;
        border: 1px solid rgba(255, 255, 255, .12);
        border-radius: 1.4rem;
        background: linear-gradient(115deg, #142e3c 0%, #174a4d 68%, #17645a 100%);
        box-shadow: 0 22px 55px rgba(24, 55, 64, .14);
        color: #fff;
    }
    .hero:after {
        position: absolute;
        top: -8rem;
        right: -4rem;
        width: 20rem;
        height: 20rem;
        border: 1px solid rgba(255,255,255,.11);
        border-radius: 50%;
        box-shadow: 0 0 0 2.5rem rgba(255,255,255,.025), 0 0 0 5rem rgba(255,255,255,.02);
        content: "";
    }
    .eyebrow {
        margin-bottom: .6rem;
        color: #9edfd0;
        font-size: .72rem;
        font-weight: 700;
        letter-spacing: .15em;
        text-transform: uppercase;
    }
    .hero h3 {
        position: relative;
        z-index: 1;
        margin: 0;
        color: #fff;
        font-size: clamp(1.7rem, 3vw, 2.4rem);
        letter-spacing: -.055em;
    }
    .hero p {
        position: relative;
        z-index: 1;
        max-width: 39rem;
        margin: .65rem 0 0;
        color: #d0e0e0;
        font-size: .98rem;
        line-height: 1.65;
    }
    .section-heading {
        margin: 0 0 .45rem;
        color: var(--ink);
        font-family: 'Manrope', sans-serif;
        font-size: 1.05rem;
        font-weight: 800;
        letter-spacing: -.035em;
    }
    .section-hint {
        margin-top: 0;
        margin-bottom: 1.15rem;
        color: var(--muted);
        font-size: .88rem;
        line-height: 1.55;
    }
    .panel-kicker {
        margin-bottom: .45rem;
        color: var(--teal);
        font-size: .68rem;
        font-weight: 800;
        letter-spacing: .14em;
        text-transform: uppercase;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid var(--line);
        border-radius: 1.1rem;
        background: rgba(255, 255, 255, .86);
        box-shadow: 0 12px 32px rgba(24, 55, 64, .045);
    }
    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        padding: 1.25rem 1.35rem;
    }
    [data-testid="stTextArea"] textarea,
    [data-testid="stTextInput"] input,
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
        border-color: var(--line);
        border-radius: .7rem;
        background: #fff;
    }
    [data-testid="stTextArea"] textarea:focus,
    [data-testid="stTextInput"] input:focus {
        border-color: #75bdb0;
        box-shadow: 0 0 0 3px rgba(12, 132, 119, .1);
    }
    [data-testid="stTextArea"] textarea {
        min-height: 12rem;
        line-height: 1.65;
    }
    [data-testid="stButton"] button[kind="primary"] {
        min-height: 3rem;
        border: 0;
        border-radius: .72rem;
        background: var(--teal);
        color: #fff;
        font-weight: 700;
        transition: background .18s ease, transform .18s ease;
    }
    [data-testid="stButton"] button[kind="primary"]:hover {
        background: var(--teal-dark);
        transform: translateY(-1px);
    }
    .result-label {
        display: inline-flex;
        align-items: center;
        gap: .45rem;
        margin-bottom: .9rem;
        color: var(--teal-dark);
        font-size: .78rem;
        font-weight: 700;
        letter-spacing: .08em;
        text-transform: uppercase;
    }
    .reply-card {
        min-height: 15rem;
        padding: 1.35rem 1.5rem;
        border: 1px solid var(--line);
        border-radius: .85rem;
        background: linear-gradient(145deg, #fff 0%, #fbfdfc 100%);
        box-shadow: 0 8px 24px rgba(24, 55, 64, .045);
        color: #314653;
        font-size: .96rem;
        line-height: 1.8;
        white-space: pre-wrap;
    }
    .empty-state {
        display: grid;
        min-height: 15rem;
        place-items: center;
        padding: 1.5rem;
        border: 1px dashed #cbd9d8;
        border-radius: .9rem;
        background: rgba(255,255,255,.55);
        color: var(--muted);
        text-align: center;
    }
    .empty-icon {
        display: grid;
        width: 2.6rem;
        height: 2.6rem;
        margin: 0 auto .7rem;
        place-items: center;
        border-radius: .85rem;
        background: var(--mint);
        color: var(--teal);
        font-size: 1.2rem;
    }
    .sidebar-note {
        padding: .9rem 1rem;
        border: 1px solid var(--line);
        border-radius: .8rem;
        background: #f8fbfa;
        color: var(--muted);
        font-size: .82rem;
        line-height: 1.55;
    }
    .footer {
        margin-top: 1.75rem;
        color: #8a999f;
        font-size: .78rem;
        text-align: center;
    }
    @media (max-width: 700px) {
        .block-container { padding: 1.2rem 1rem 2rem; }
        .hero { padding: 1.7rem 1.35rem; }
        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            padding: 1rem;
        }
        .reply-card, .empty-state { min-height: 12rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        '<div class="brand"><span class="brand-mark">✦</span> Reply Studio</div>',
        unsafe_allow_html=True,
    )
    st.markdown("#### Reply preferences")
    tone = st.selectbox(
        "Tone",
        ["Empathetic & reassuring", "Warm & conversational", "Professional & concise"],
        help="Choose how the response should sound.",
    )
    company_name = st.text_input(
        "Company name",
        placeholder="e.g. Northstar",
        help="Optional. Used to personalize the sign-off.",
    )
    st.markdown("---")

    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        st.success("AI connection ready", icon=":material/check_circle:")
    else:
        api_key = st.text_input(
            "Groq API key",
            type="password",
            placeholder="Enter your API key",
            help="Your key is used for this session only and is not saved.",
        )
        st.caption("Or add `GROQ_API_KEY` to your local `.env` file.")

    st.markdown(
        '<div class="sidebar-note">Your message is used only to draft a reply. '
        "Always review the response before sending it to a customer.</div>",
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <section class="hero">
      <div class="eyebrow">Customer care, made thoughtful</div>
      <h3>Tell us your problem we'll here to solve it</h3>
      <p>Turn a tough customer moment into a thoughtful, helpful response — ready for your team to review and send.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

input_col, reply_col = st.columns([1, 1], gap="large")

with input_col:
    with st.container(border=True):
        st.markdown('<div class="panel-kicker">01 &nbsp; / &nbsp; Incoming message</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">Customer message</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-hint">Paste the message you received. We’ll shape a reply that acknowledges the issue and moves things forward.</div>',
            unsafe_allow_html=True,
        )

        customer_message = st.text_area(
            "AI assistant",
            placeholder=(
                "For example: I've been waiting for my express delivery for two hours "
                "and it still hasn't arrived. I would like a refund."
            ),
            height=190,
            label_visibility="collapsed",
            key="AI assistant",
        )

        generate_col, helper_col = st.columns([1, 1.5], vertical_alignment="center")
        with generate_col:
            generate = st.button("✦  Write a reply", type="primary", use_container_width=True)
        with helper_col:
            st.caption("Thoughtful, clear, and ready for your review.")

        if generate:
            st.session_state.pop("generated_reply", None)
            if not customer_message.strip():
                st.warning("Add the customer’s message before generating a reply.")
            elif not api_key:
                st.error("Add a Groq API key in the sidebar or configure `GROQ_API_KEY` in your `.env` file.")
            else:
                prompt = f"""
You are an AI Disaster Early Warning Assistant.

Your job is to analyze the provided environmental data and
the user's question and identify possible disaster risks.

IMPORTANT:
- Analyze the user's actual question.
- Do not assume the disaster is a flood.
- If the user asks about strong wind, analyze wind-related risks.
- If the user asks about heavy rain, analyze flood/heavy-rain risks.
- If the available data is insufficient to make a prediction, clearly say so.
- Do not invent weather data.
- Do not claim that an official warning has been issued.
- Give a prediction based only on the provided data.

Location:
Mumbai, Maharashtra

Current Environmental Data:
- Rainfall: 92 mm in the last 24 hours
- Rainfall forecast: 120 mm in the next 24 hours
- Humidity: 91%
- Temperature: 26°C
- Wind speed: 28 km/h
- River/Water level: 4.1 meters
- Water level trend: Rising
- Soil moisture: 88%
- Weather condition: Heavy rain
- Visibility: 2.5 km

Historical Information:
- Heavy rainfall has previously caused flooding in this area.
- Low-lying areas are more vulnerable to water accumulation.

User's question:
{customer_message.strip()}

Give your answer in this format:

Disaster/Risk:
Risk Level:
Prediction:
Main Risk Factors:
Early Warning:
What to Monitor:

Do not make up information that is not present in the data.
"""
                try:
                    with st.spinner("Crafting a thoughtful response..."):
                        llm = ChatGroq(
                            model="openai/gpt-oss-20b",
                            temperature=0.2,
                            api_key=api_key,
                        )
                        result = llm.invoke(prompt)
                        st.session_state["generated_reply"] = str(result.content).strip()
                except Exception as exc:
                    st.error("The reply couldn’t be generated. Check your Groq connection and try again.")
                    st.caption(f"Details: {exc}")

with reply_col:
    with st.container(border=True):
        st.markdown('<div class="panel-kicker">02 &nbsp; / &nbsp; Your draft</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">Response draft</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-hint">Review the suggested reply and make it your own before sending.</div>',
            unsafe_allow_html=True,
        )

        reply = st.session_state.get("generated_reply", "")
        if reply:
            st.markdown(
                f'<div class="reply-card">{html.escape(reply)}</div>',
                unsafe_allow_html=True,
            )
            escaped_reply = html.escape(reply, quote=True)
            components.html(
                f"""
        <div style="display:flex;justify-content:flex-end;padding-top:10px;">
          <button id="copy-reply" type="button" style="
            border:1px solid #d8e4e1;border-radius:9px;background:#fff;
            color:#176c62;padding:9px 14px;font:600 13px 'DM Sans',sans-serif;
            cursor:pointer;transition:background .15s ease;">
            Copy response
          </button>
        </div>
        <textarea id="reply-text" aria-hidden="true" style="
          position:absolute;left:-9999px;top:0;">{escaped_reply}</textarea>
        <script>
          const button = document.getElementById("copy-reply");
          const text = document.getElementById("reply-text");
          button.addEventListener("click", async () => {{
            try {{
              await navigator.clipboard.writeText(text.value);
            }} catch (error) {{
              text.focus();
              text.select();
              document.execCommand("copy");
            }}
            button.textContent = "Copied!";
            button.style.background = "#e9f6f2";
            window.setTimeout(() => {{
              button.textContent = "Copy response";
              button.style.background = "#fff";
            }}, 1800);
          }});
        </script>
        """,
                height=52,
                scrolling=False,
            )
        else:
            st.markdown(
                """
        <div class="empty-state">
          <div>
            <div class="empty-icon">✦</div>
            <strong>Your polished reply will appear here</strong><br>
            <span>Enter a customer message and select <em>Write a reply</em> to get started.</span>
          </div>
        </div>
        """,
                unsafe_allow_html=True,
            )

st.markdown(
    '<div class="footer">Thoughtful support is good business. Review every draft before sending.</div>',
    unsafe_allow_html=True,
)
