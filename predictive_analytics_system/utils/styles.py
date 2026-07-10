"""
utils/styles.py

Reusable CSS and UI components for
Google Maps Business Analytics Dashboard.
"""

import streamlit as st

# LOAD GLOBAL CSS

def load_css():

    st.markdown(
        """
        <style>

        /* ===============================
            MAIN APP
        ================================ */

        .stApp{
            background:white;
        }

        header{
            visibility:hidden;
        }

        footer{
            visibility:hidden;
        }

        /* ===============================
            SIDEBAR
        ================================ */

        section[data-testid="stSidebar"]{
            background:#F7F7F7;
        }

        section[data-testid="stSidebar"] *{
            color:black !important;
        }

        /* ===============================
            HEADINGS
        ================================ */
        h1,h2,h3,h4,h5,h6{
            color:#000000 !important;
            font-weight:700;
        }

        /* Streamlit Markdown */
        .stMarkdown h1,
        .stMarkdown h2,
        .stMarkdown h3,
        .stMarkdown h4,
        .stMarkdown h5,
        .stMarkdown h6{
            color:#000000 !important;
        }

        /* Streamlit Markdown Container */

        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3,
        [data-testid="stMarkdownContainer"] h4,
        [data-testid="stMarkdownContainer"] h5,
        [data-testid="stMarkdownContainer"] h6{
            color:#000000 !important;
        }

        p{
            color:black !important;
        }

        label{
            color:black !important;
        }

        /* ===============================
            METRICS
        ================================ */

        [data-testid="stMetricLabel"]{
            color:black !important;
            font-weight:600;
        }

        [data-testid="stMetricValue"]{
            color:black !important;
        }

        /* ===============================
            BUTTONS
        ================================ */

        .stButton > button{

            width:100%;

            border-radius:10px;

            background:#0F62FE;

            color:red !important;

            border:none;

            font-weight:600;

            height:45px;

        }

        .stButton > button:hover{

            background:#0043CE;

            color:white;

        }

        /* ===============================
            DATAFRAME
        ================================ */

        .stDataFrame{

            border-radius:10px;

        }

        /* ===============================
            TABS
        ================================ */

        button[data-baseweb="tab"]{

            color:black !important;

            font-weight:600;

        }

        /* ===============================
            HERO
        ================================ */

        .hero{

            background:#0F62FE;

            padding:30px;

            border-radius:15px;

            color:white;

            margin-bottom:20px;

        }

        .hero h1{

            color:white !important;

        }

        .hero p{

            color:white !important;

        }

        /* ===============================
            CARD
        ================================ */

        .card{

            background:white;

            border-radius:12px;

            padding:18px;

            border:1px solid #EEEEEE;

            box-shadow:0 2px 8px rgba(0,0,0,0.08);

            margin-bottom:15px;

        }

        /* ===============================
            SUCCESS
        ================================ */

        .success-card{

            background:#16A34A;

            color:white;

            padding:18px;

            border-radius:12px;

        }

        .success-card h3,
        .success-card h4,
        .success-card p{

            color:white !important;

        }

        /* ===============================
            WARNING
        ================================ */

        .warning-card{

            background:#EA580C;

            color:white;

            padding:18px;

            border-radius:12px;

        }

        .warning-card h3,
        .warning-card h4,
        .warning-card p{

            color:white !important;

        }

        /* ===============================
            ERROR
        ================================ */

        .error-card{

            background:#DC2626;

            color:white;

            padding:18px;

            border-radius:12px;

        }

        .error-card h3,
        .error-card h4,
        .error-card p{

            color:white !important;

        }

        </style>
        """,
        unsafe_allow_html=True,
    )


# HERO SECTION

def hero_section(title, subtitle):

    st.markdown(
        f"""
<div class="hero">

<h1 style="color:white; margin-bottom:10px;">
{title}
</h1>

<p style="font-size:18px; color:white;">
{subtitle}
</p>

</div>
""",
        unsafe_allow_html=True,
    )


# SIMPLE CARD

def card(title, body):

    st.markdown(
        f"""
        <div class="card">

        <h4>{title}</h4>

        <p>{body}</p>

        </div>
        """,
        unsafe_allow_html=True,
    )


# SUCCESS CARD

def success_card(title, body):

    st.markdown(
        f"""
<div class="success-card">

<h3 style="color:white;">
{title}
</h3>

<p style="color:white;">
{body}
</p>

</div>
""",
        unsafe_allow_html=True,
    )


# WARNING CARD

def warning_card(title, body):

    st.markdown(
        f"""
<div class="warning-card">

<h3 style="color:white;">
{title}
</h3>

<p style="color:white;">
{body}
</p>

</div>
""",
        unsafe_allow_html=True,
    )


# ERROR CARD

def error_card(title, body):

    st.markdown(
        f"""
<div class="error-card">

<h3 style="color:white;">
{title}
</h3>

<p style="color:white;">
{body}
</p>

</div>
""",
        unsafe_allow_html=True,
    )


# SECTION TITLE

def section_title(title):

    st.markdown(
        f"""
        <h2 style="
        color:black;
        font-weight:700;
        margin-top:15px;
        ">
        {title}
        </h2>
        """,
        unsafe_allow_html=True,
    )