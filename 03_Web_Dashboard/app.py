import os
import json
import numpy as np
import pandas as pd
import scipy.sparse as sp
import streamlit as st
import joblib

# -----------------------------------------------------------------------------
# 1. Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="arXiv Topic Explorer",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. Custom Stylesheet (Cinzel + Spectral + Fira Code + Gold/Parchment)
# -----------------------------------------------------------------------------
st.markdown("""
<!-- Google Fonts: Cinzel (Headings), Spectral (Body), Fira Code (Mono) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700;800&family=Fira+Code:wght@400;500;600;700&family=Spectral:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">

<style>
    /* Global Background & Typography */
    .stApp {
        background-color: #1A0F0A;
        color: #F5E6D3;
        font-family: 'Spectral', Georgia, serif;
        font-size: 16px;
        line-height: 1.7;
    }
    
    /* Headlines in Cinzel */
    h1, h2, h3, h4, h5, h6, .cinzel-font {
        font-family: 'Cinzel', serif !important;
        color: #F5E6D3 !important;
        letter-spacing: 0.5px;
    }
    
    /*  Cards */
    .quest-card {
        background-color: #2C1A10;
        border: 1px solid #5C3D2E;
        border-top: 2px solid #CA8A04;
        border-radius: 4px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 16px rgba(202, 138, 4, 0.15);
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    }
    
    .quest-card:hover {
        background-color: #3D2517;
        box-shadow: 0 4px 20px rgba(202, 138, 4, 0.28);
        border-color: #CA8A04;
    }
    
    /* Stat Metric Box () */
    .stat-card-quest {
        background-color: #2C1A10;
        border: 1px solid #5C3D2E;
        border-radius: 4px;
        padding: 18px 16px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(202, 138, 4, 0.12);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .stat-card-quest:hover {
        transform: translateY(-2px);
        border-color: #CA8A04;
    }
    
    .stat-number-quest {
        font-family: 'Fira Code', monospace;
        font-size: 26px;
        font-weight: 700;
        color: #CA8A04;
        margin-bottom: 4px;
    }
    
    .stat-label-quest {
        font-family: 'Cinzel', serif;
        font-size: 11.5px;
        font-weight: 600;
        color: #E5D5C3;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Chips & Badges */
    .quest-chip {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 2px;
        font-family: 'Cinzel', serif;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin: 3px 4px 3px 0;
    }
    
    .chip-gold {
        background-color: #CA8A04;
        color: #1A0F0A;
        font-weight: 700;
    }
    
    .chip-title-quest {
        background-color: #2C1A10;
        color: #CA8A04;
        border: 1px solid #5C3D2E;
    }
    
    .chip-abstract-quest {
        background-color: #2C1A10;
        color: #F5E6D3;
        border: 1px solid #5C3D2E;
    }
    
    .chip-purple {
        background-color: #581C87;
        color: #F5E6D3;
        border: 1px solid #9333EA;
    }
    
    .chip-red {
        background-color: #991B1B;
        color: #F5E6D3;
        border: 1px solid #DC2626;
    }
    
    .chip-green {
        background-color: rgba(34, 197, 94, 0.15);
        color: #22C55E;
        border: 1px solid #22C55E;
    }
    
    /* Pipeline Step Box */
    .step-box-quest {
        background-color: #2C1A10;
        border: 1px solid #5C3D2E;
        border-radius: 4px;
        padding: 16px;
        height: 100%;
    }
    
    .step-badge-quest {
        font-family: 'Cinzel', serif;
        font-size: 10.5px;
        font-weight: 700;
        letter-spacing: 1px;
        color: #1A0F0A;
        background-color: #CA8A04;
        padding: 2px 8px;
        border-radius: 2px;
        display: inline-block;
        margin-bottom: 8px;
    }
    
    /* Prediction Banner */
    .result-banner-quest {
        background-color: #3D2517;
        border: 1px solid #CA8A04;
        border-top: 3px solid #CA8A04;
        border-radius: 4px;
        padding: 20px;
        margin-top: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(202, 138, 4, 0.35);
    }
    
    .result-cluster-id-quest {
        font-family: 'Cinzel', serif;
        font-size: 12px;
        color: #CA8A04;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }
    
    .result-cluster-name-quest {
        font-family: 'Cinzel', serif;
        font-size: 22px;
        font-weight: 700;
        color: #F5E6D3;
        margin-top: 4px;
    }
    
    /* Intel Brief Callout */
    .intel-brief-quest {
        background-color: #2C1A10;
        border-left: 3px solid #CA8A04;
        border-right: 1px solid #5C3D2E;
        border-top: 1px solid #5C3D2E;
        border-bottom: 1px solid #5C3D2E;
        padding: 14px 18px;
        border-radius: 0 4px 4px 0;
        font-size: 14.5px;
        color: #F5E6D3;
        line-height: 1.6;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    
    .intel-brief-quest strong {
        color: #CA8A04;
        font-family: 'Cinzel', serif;
    }
    
    /* Streamlit Custom Element Overrides */
    .stButton>button {
        background-color: #CA8A04 !important;
        color: #1A0F0A !important;
        font-family: 'Cinzel', serif !important;
        font-weight: 700 !important;
        border: 1px solid #DAA520 !important;
        border-radius: 4px !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 2px 8px rgba(202, 138, 4, 0.25) !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton>button:hover {
        background-color: #B8780A !important;
        box-shadow: 0 4px 16px rgba(202, 138, 4, 0.45) !important;
        transform: translateY(-1px);
    }
    
    /* Text Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #2C1A10 !important;
        color: #F5E6D3 !important;
        border: 1px solid #5C3D2E !important;
        border-radius: 4px !important;
        font-family: 'Spectral', serif !important;
        font-size: 15px !important;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #CA8A04 !important;
        box-shadow: 0 0 10px rgba(202, 138, 4, 0.3) !important;
    }
    
    /* Selectboxes */
    .stSelectbox>div>div {
        background-color: #2C1A10 !important;
        color: #F5E6D3 !important;
        border: 1px solid #5C3D2E !important;
        border-radius: 4px !important;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: 1px solid #5C3D2E;
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Cinzel', serif !important;
        font-size: 13.5px !important;
        font-weight: 600 !important;
        color: #E5D5C3 !important;
        border-radius: 4px 4px 0 0 !important;
        padding: 8px 16px !important;
        letter-spacing: 0.5px !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #CA8A04 !important;
        background-color: #2C1A10 !important;
        border-top: 2px solid #CA8A04 !important;
        border-left: 1px solid #5C3D2E !important;
        border-right: 1px solid #5C3D2E !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: #CA8A04 !important;
    }
    
    /* -------------------------------------------------------------------------
       Sidebar  Custom Styling (Explicit High-Contrast Colors)
       ------------------------------------------------------------------------- */
    [data-testid="stSidebar"], section[data-testid="stSidebar"] {
        background-color: #21140D !important;
        border-right: 1px solid #5C3D2E !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4, 
    [data-testid="stSidebar"] h5, 
    [data-testid="stSidebar"] h6 {
        color: #CA8A04 !important;
        font-family: 'Cinzel', serif !important;
        letter-spacing: 0.5px !important;
    }
    
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] li, 
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] .stMarkdown {
        color: #F5E6D3 !important;
        font-family: 'Spectral', Georgia, serif !important;
    }
    
    [data-testid="stSidebar"] .stCaption, 
    [data-testid="stSidebar"] small, 
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #D4BFA7 !important;
        font-family: 'Spectral', Georgia, serif !important;
        font-size: 13.5px !important;
    }
    
    [data-testid="stSidebar"] a {
        color: #EAB308 !important;
        text-decoration: underline !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: #5C3D2E !important;
        margin: 16px 0 !important;
    }

    /* Universal High-Contrast Streamlit Overrides */
    .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown li, .stMarkdown div {
        color: #F5E6D3 !important;
    }
    
    .stCaption, [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p {
        color: #E5D5C3 !important;
        font-size: 14px !important;
    }
    
    label[data-testid="stWidgetLabel"], label[data-testid="stWidgetLabel"] p, label[data-testid="stWidgetLabel"] span {
        color: #F5E6D3 !important;
        font-family: 'Cinzel', serif !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
    }
    
    div[data-testid="stRadio"] label, div[data-testid="stRadio"] label p, div[data-testid="stRadio"] label span {
        color: #F5E6D3 !important;
        font-family: 'Spectral', Georgia, serif !important;
        font-size: 15px !important;
    }
    
    div[data-baseweb="select"] > div {
        background-color: #2C1A10 !important;
        color: #F5E6D3 !important;
        border-color: #5C3D2E !important;
    }
    
    div[data-baseweb="select"] span, div[data-baseweb="select"] div {
        color: #F5E6D3 !important;
    }
    
    ul[role="listbox"], div[data-baseweb="popover"], div[data-baseweb="menu"] {
        background-color: #2C1A10 !important;
        border: 1px solid #CA8A04 !important;
    }
    
    li[role="option"], li[role="option"] * {
        background-color: #2C1A10 !important;
        color: #F5E6D3 !important;
    }
    
    li[role="option"]:hover, li[role="option"][aria-selected="true"] {
        background-color: #3D2517 !important;
        color: #CA8A04 !important;
    }
    
    div[data-testid="stAlert"] {
        background-color: #2C1A10 !important;
        border: 1px solid #CA8A04 !important;
    }
    
    div[data-testid="stAlert"] * {
        color: #F5E6D3 !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #E5D5C3 !important;
    }

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. Cluster Metadata Dictionary (15 Clusters Ground Truth)
# -----------------------------------------------------------------------------
CLUSTERS_METADATA = {
    "0": {
        "id": "00",
        "name": "Gravitasi, Kosmologi & Fisika Energi Tinggi (General Relativity & Cosmology)",
        "velocity_status": "Stable / Foundational",
        "growth_pct": "+0.4%",
        "title_keywords": ["gravity", "black hole", "relativity", "gravitational", "cosmology", "inflationary", "cosmic", "einstein", "spacetime", "metric"],
        "abstract_keywords": ["gravity", "black", "hole", "relativity", "gravitational", "wave", "cosmology", "inflationary", "cosmic", "field", "horizon"],
        "categories": [
            {"name": "gr-qc (General Relativity & Quantum Cosmology)", "percent": 58.87},
            {"name": "hep-th (High Energy Physics - Theory)", "percent": 37.70},
            {"name": "astro-ph.HE (High Energy Astrophysical Phenomena)", "percent": 20.27}
        ]
    },
    "1": {
        "id": "01",
        "name": "Pemrosesan Bahasa Alami & AI Core (Natural Language Processing & Core AI)",
        "velocity_status": "High Growth / Frontier",
        "growth_pct": "+3.8%",
        "title_keywords": ["language", "translation", "semantic", "parser", "parsing", "corpus", "sentences", "word", "nlp", "text"],
        "abstract_keywords": ["language", "translation", "semantic", "parser", "parsing", "corpus", "sentences", "word", "nlp", "text", "machine"],
        "categories": [
            {"name": "cs.CL (Computation and Language)", "percent": 22.54},
            {"name": "cs.AI (Artificial Intelligence)", "percent": 21.94},
            {"name": "cs.LG (Machine Learning)", "percent": 21.48}
        ]
    },
    "2": {
        "id": "02",
        "name": "Sistem Kontrol, Optimasi & Sistem Dinamis (Control Systems & Optimization)",
        "velocity_status": "Stable / Active",
        "growth_pct": "+0.9%",
        "title_keywords": ["control", "optimal", "state", "optimization", "system", "feedback", "linear", "controller", "trajectory", "robust"],
        "abstract_keywords": ["control", "optimal", "state", "optimization", "system", "feedback", "linear", "controller", "trajectory", "robust", "lyapunov"],
        "categories": [
            {"name": "cs.LG (Machine Learning)", "percent": 9.73},
            {"name": "cs.CV (Computer Vision)", "percent": 9.51},
            {"name": "cs.AI (Artificial Intelligence)", "percent": 8.92}
        ]
    },
    "3": {
        "id": "03",
        "name": "Fisika Kuantum & Informasi Kuantum (Quantum Physics & Information)",
        "velocity_status": "High Growth / Emerging",
        "growth_pct": "+2.4%",
        "title_keywords": ["quantum", "spin", "entanglement", "qubit", "teleportation", "gate", "coherence", "superconducting", "cavity", "photon"],
        "abstract_keywords": ["quantum", "spin", "entanglement", "qubit", "teleportation", "gate", "coherence", "superconducting", "cavity", "photon", "state"],
        "categories": [
            {"name": "quant-ph (Quantum Physics)", "percent": 60.89},
            {"name": "cond-mat.mes-hall (Mesoscale Physics)", "percent": 14.28},
            {"name": "hep-th (High Energy Physics - Theory)", "percent": 10.38}
        ]
    },
    "4": {
        "id": "04",
        "name": "Fisika Energi Tinggi Teoretis (Theoretical High Energy Physics)",
        "velocity_status": "Mature / Theory-Heavy",
        "growth_pct": "-1.1%",
        "title_keywords": ["string", "supersymmetry", "conformal", "field", "branes", "dual", "duality", "holographic", "gravity", "dimensions"],
        "abstract_keywords": ["string", "supersymmetry", "conformal", "field", "branes", "dual", "duality", "holographic", "gravity", "dimensions", "gauge"],
        "categories": [
            {"name": "hep-th (High Energy Physics - Theory)", "percent": 27.48},
            {"name": "hep-ph (High Energy Physics - Phenomenology)", "percent": 11.16},
            {"name": "gr-qc (General Relativity & Quantum Cosmology)", "percent": 7.97}
        ]
    },
    "5": {
        "id": "05",
        "name": "Fisika Fenomenologi & Sistem Kompleks (Phenomenology & Complex Systems)",
        "velocity_status": "Stable",
        "growth_pct": "-0.3%",
        "title_keywords": ["model", "standard", "neutrino", "physics", "particles", "collider", "dark", "mass", "decay", "higgs"],
        "abstract_keywords": ["model", "standard", "neutrino", "physics", "particles", "collider", "dark", "mass", "decay", "higgs", "coupling"],
        "categories": [
            {"name": "hep-ph (High Energy Physics - Phenomenology)", "percent": 12.78},
            {"name": "cs.LG (Machine Learning)", "percent": 9.12},
            {"name": "cs.AI (Artificial Intelligence)", "percent": 7.76}
        ]
    },
    "6": {
        "id": "06",
        "name": "Fisika Benda Terkondensasi & Ilmu Bahan (Condensed Matter & Materials Science)",
        "velocity_status": "Active / High Potential",
        "growth_pct": "+1.3%",
        "title_keywords": ["superconducting", "materials", "crystal", "topological", "insulator", "transport", "magnetic", "electronic", "band", "structure"],
        "abstract_keywords": ["superconducting", "materials", "crystal", "topological", "insulator", "transport", "magnetic", "electronic", "band", "structure", "transition"],
        "categories": [
            {"name": "cond-mat.mes-hall (Mesoscale Physics)", "percent": 21.61},
            {"name": "cond-mat.str-el (Strongly Correlated Electrons)", "percent": 21.11},
            {"name": "cond-mat.mtrl-sci (Materials Science)", "percent": 17.66}
        ]
    },
    "7": {
        "id": "07",
        "name": "Pembelajaran Mesin & Deep Learning Utama (Machine Learning & Deep Learning)",
        "velocity_status": "High Growth / Frontier",
        "growth_pct": "+5.1%",
        "title_keywords": ["learning", "deep", "reinforcement", "machine", "supervised", "data", "training", "performance", "neural", "network"],
        "abstract_keywords": ["learning", "deep", "reinforcement", "machine", "supervised", "data", "training", "performance", "neural", "network", "models"],
        "categories": [
            {"name": "cs.LG (Machine Learning)", "percent": 54.37},
            {"name": "cs.AI (Artificial Intelligence)", "percent": 24.67},
            {"name": "cs.CV (Computer Vision)", "percent": 23.00}
        ]
    },
    "8": {
        "id": "08",
        "name": "Astrofisika & Astronomi (Astrophysics & Astronomy)",
        "velocity_status": "Stable / Foundational",
        "growth_pct": "+0.5%",
        "title_keywords": ["galaxy", "star", "ray", "mass", "emission", "stellar", "gas", "radio", "telescope", "cluster"],
        "abstract_keywords": ["galaxy", "star", "ray", "mass", "emission", "stellar", "gas", "radio", "telescope", "cluster", "observations"],
        "categories": [
            {"name": "astro-ph.GA (Astrophysics of Galaxies)", "percent": 30.06},
            {"name": "astro-ph (Astrophysics)", "percent": 29.17},
            {"name": "astro-ph.SR (Solar and Stellar Astrophysics)", "percent": 19.55}
        ]
    },
    "9": {
        "id": "09",
        "name": "Visi Komputer & Jaringan Saraf (Computer Vision & Neural Networks)",
        "velocity_status": "High Growth / Saturated Core",
        "growth_pct": "+2.9%",
        "title_keywords": ["neural", "network", "convolutional", "deep", "graph", "wireless", "detection", "layered", "hidden", "activation"],
        "abstract_keywords": ["neural", "network", "convolutional", "deep", "graph", "wireless", "detection", "layered", "hidden", "activation", "learning"],
        "categories": [
            {"name": "cs.LG (Machine Learning)", "percent": 35.61},
            {"name": "cs.CV (Computer Vision)", "percent": 16.95},
            {"name": "cs.AI (Artificial Intelligence)", "percent": 12.28}
        ]
    },
    "10": {
        "id": "10",
        "name": "Topik Multidisiplin & Umum (Multidisciplinary & General Science)",
        "velocity_status": "General / Broad",
        "growth_pct": "0.0%",
        "title_keywords": ["data", "analysis", "multi", "graphs", "dynamics", "dimensional", "functions", "high", "study", "field"],
        "abstract_keywords": ["data", "analysis", "multi", "graphs", "dynamics", "dimensional", "functions", "high", "study", "field", "results"],
        "categories": [
            {"name": "hep-ph (High Energy Physics - Phenomenology)", "percent": 7.03},
            {"name": "cs.LG (Machine Learning)", "percent": 6.50},
            {"name": "cs.CV (Computer Vision)", "percent": 6.02}
        ]
    },
    "11": {
        "id": "11",
        "name": "Aljabar, Teori Grup & Teori Representasi (Algebra & Group Theory)",
        "velocity_status": "Foundational / Theory",
        "growth_pct": "-0.6%",
        "title_keywords": ["group", "algebra", "lie", "finite", "representation", "subgroups", "abelian", "free", "compact", "ring"],
        "abstract_keywords": ["group", "algebra", "lie", "finite", "representation", "subgroups", "abelian", "free", "compact", "ring", "prove"],
        "categories": [
            {"name": "math.GR (Group Theory)", "percent": 25.40},
            {"name": "math.RT (Representation Theory)", "percent": 18.09},
            {"name": "math.RA (Rings and Algebras)", "percent": 15.16}
        ]
    },
    "12": {
        "id": "12",
        "name": "Persamaan Diferensial & Analisis Numerik (Differential Equations & Numerical Analysis)",
        "velocity_status": "Foundational / High-Reliability",
        "growth_pct": "-0.2%",
        "title_keywords": ["equation", "differential", "solution", "boundary", "value", "existence", "uniqueness", "nonlinear", "numerical", "method"],
        "abstract_keywords": ["equation", "differential", "solution", "boundary", "value", "existence", "uniqueness", "nonlinear", "numerical", "method", "paper"],
        "categories": [
            {"name": "math.AP (Analysis of PDEs)", "percent": 24.71},
            {"name": "math-ph (Mathematical Physics)", "percent": 9.04},
            {"name": "math.MP (Mathematical Physics)", "percent": 9.04}
        ]
    },
    "13": {
        "id": "13",
        "name": "AI Generatif, Difusi & Retrieval (Generative AI, Diffusion & Information Retrieval)",
        "velocity_status": "Peak High Growth",
        "growth_pct": "+6.4%",
        "title_keywords": ["image", "text", "generation", "diffusion", "retrieval", "augmented", "video", "generative", "gan", "style"],
        "abstract_keywords": ["image", "text", "generation", "diffusion", "retrieval", "augmented", "video", "generative", "gan", "style", "models"],
        "categories": [
            {"name": "cs.CV (Computer Vision)", "percent": 25.87},
            {"name": "cs.AI (Artificial Intelligence)", "percent": 20.72},
            {"name": "cs.CL (Computation and Language)", "percent": 17.90}
        ]
    },
    "14": {
        "id": "14",
        "name": "Kosmologi & Fenomenologi Partikel (Cosmology & Particle Physics Phenomenology)",
        "velocity_status": "Active Observation",
        "growth_pct": "+0.8%",
        "title_keywords": ["dark", "energy", "matter", "cosmic", "inflation", "gravitational", "lensing", "background", "cosmological", "acceleration"],
        "abstract_keywords": ["dark", "energy", "matter", "cosmic", "inflation", "gravitational", "lensing", "background", "cosmological", "acceleration", "hep-ph"],
        "categories": [
            {"name": "hep-ph (High Energy Physics - Phenomenology)", "percent": 34.22},
            {"name": "astro-ph.CO (Cosmology and Nongalactic Astrophysics)", "percent": 19.22},
            {"name": "gr-qc (General Relativity & Quantum Cosmology)", "percent": 13.14}
        ]
    }
}

# -----------------------------------------------------------------------------
# 4. Research Advisor Knowledge Base
# -----------------------------------------------------------------------------
RESEARCH_DOMAINS = {
    "cs": {
        "name": "Computer Science & Artificial Intelligence",
        "clusters": ["1", "2", "7", "9", "13"],
        "summary": "Fokus pada algoritma kecerdasan buatan, pemrosesan bahasa, visi komputer, dan sistem kontrol otonom."
    },
    "physics": {
        "name": "Physics, Quantum & Space Science",
        "clusters": ["0", "3", "4", "5", "6", "8", "14"],
        "summary": "Fokus pada komputasi kuantum, fisika benda terkondensasi, astrofisika, kosmologi, dan fisika partikel."
    },
    "math": {
        "name": "Mathematics & Numerical Analysis",
        "clusters": ["11", "12"],
        "summary": "Fokus pada persamaan diferensial non-linear, analisis numerik, teori grup, dan aljabar murni/terapan."
    },
    "cross": {
        "name": "Interdisciplinary & Cross-Domain Bridges",
        "clusters": ["cross"],
        "summary": "Celah riset di persimpangan dua disiplin ilmu yang memiliki potensi kebaruan (novelty) tertinggi saat ini."
    }
}

INTERDISCIPLINARY_BRIDGES = [
    {
        "title": "Quantum Machine Learning (QML)",
        "clusters": "Klaster 03 (Fisika Kuantum) + Klaster 07 (Deep Learning)",
        "desc": "Menggabungkan sirkuit kuantum tervariasi (VQC) dengan arsitektur neural network untuk mempercepat optimasi fungsi berdimensi sangat tinggi.",
        "starter_question": "Bagaimana memanfaatkan Variational Quantum Circuits (VQC) untuk mempercepat pelatihan model neural network pada data berdimensi sangat tinggi?",
        "sample_title": "Variational Quantum Circuit Optimization for High-Dimensional Supervised Classification"
    },
    {
        "title": "Physics-Informed Neural Networks (PINNs)",
        "clusters": "Klaster 12 (Persamaan Diferensial) + Klaster 09 (Jaringan Saraf)",
        "desc": "Menyematkan hukum fisika konservasi massa/energi (PDE) langsung ke dalam fungsi loss neural network agar prediksi selalu mematuhi hukum fisika.",
        "starter_question": "Bagaimana merancang loss function berbasis hukum konservasi fluida (Navier-Stokes) pada arsitektur PINNs agar konvergensi lebih stabil?",
        "sample_title": "Physics-Informed Neural Networks for Solving Non-Linear Fluid Dynamics with Conservation Constraints"
    },
    {
        "title": "AI for Astrophysics & Cosmic Web Discovery",
        "clusters": "Klaster 08 (Astrofisika) + Klaster 13 (AI Generatif & Diffusion)",
        "desc": "Menggunakan model difusi dan vision transformer untuk rekonstruksi gambar teleskopik resolusi tinggi dan deteksi halo materi gelap.",
        "starter_question": "Dapatkah Latent Diffusion Models merekonstruksi distorsi gravitational lensing pada citra galaksi teleskop radio dengan akurasi sub-pixel?",
        "sample_title": "High-Fidelity Gravitational Lensing Reconstruction via Latent Diffusion Models"
    },
    {
        "title": "AI-Driven Quantum Materials Discovery",
        "clusters": "Klaster 06 (Benda Terkondensasi) + Klaster 07 (Machine Learning)",
        "desc": "Memanfaatkan Graph Neural Networks (GNN) untuk memprediksi suhu kritis superkonduktivitas dan topologi pita elektronik material baru.",
        "starter_question": "Bagaimana arsitektur Graph Neural Network dapat memprediksi fase isolator topologis pada struktur kristal senyawa biner?",
        "sample_title": "Predicting Topological Insulator Phases in Crystal Structures via Equivariant Graph Networks"
    },
    {
        "title": "Safe Multi-Agent Reinforcement Learning for Control",
        "clusters": "Klaster 02 (Sistem Kontrol) + Klaster 07 (Reinforcement Learning)",
        "desc": "Mengintegrasikan Control Barrier Functions (CBF) dengan algoritma Actor-Critic untuk menjamin keselamatan robot otonom saat bernavigasi bersama.",
        "starter_question": "Bagaimana menjamin keamanan bebas tabrakan (zero-collision guarantee) pada kawanan drone otonom menggunakan Control Barrier Functions?",
        "sample_title": "Safe Multi-Agent Reinforcement Learning with Control Barrier Functions for Autonomous Drone Swarms"
    }
]

CLUSTER_STARTER_QUESTIONS = {
    "0": [
        "Bagaimana observasi gelombang gravitasi terbaru dapat membatasi model kosmologi inflasi non-standar?",
        "Simulasi numerik relativitas umum pada penggabungan lubang hitam biner bermassa asimetris."
    ],
    "1": [
        "Bagaimana memitigasi halusinasi pada Large Language Models (LLM) menggunakan ensemble constraint semantik?",
        "Transfer learning lintas bahasa berdaya komputasi rendah (low-resource cross-lingual PEFT)."
    ],
    "2": [
        "Bagaimana menjamin stabilitas Lyapunov pada controller berbasis neural network di lingkungan dinamis yang berubah-ubah?",
        "Distributed Model Predictive Control (MPC) untuk armada kendaraan otonom berskala besar."
    ],
    "3": [
        "Bagaimana meningkatkan waktu koherensi qubit superkonduktor di bawah gangguan dekoherensi termal?",
        "Algoritma kuantum mitigasi galat untuk perangkat Noisy Intermediate-Scale Quantum (NISQ)."
    ],
    "4": [
        "Pemeriksaan dualitas holografik (AdS/CFT) pada medan konformal berdimensi ganjil.",
        "Studi koreksi non-perturbatif pada teori medan kuantum supersimetris."
    ],
    "5": [
        "Kendala massa neutrino steril dari eksperimen collider energi tinggi dan observasi kosmologi.",
        "Pencarian partikel materi gelap ringan di bawah model standar yang diperluas (BSM physics)."
    ],
    "6": [
        "Eksplorasi transisi fase topologis pada material dua dimensi di bawah medan magnetik kuat.",
        "Mekanisme transpor termal dan elektronik pada superkonduktor suhu tinggi berstruktur kagome."
    ],
    "7": [
        "Bagaimana mencegah catastrophic forgetting pada continual learning menggunakan regularisasi gradien adaptif?",
        "Batas generalisasi teoritis pada arsitektur deep learning overparameterized."
    ],
    "8": [
        "Analisis spektroskopi emisi gas antarbintang untuk memetakan laju pembentukan bintang pada galaksi purba.",
        "Karakterisasi atmosfer eksoplanet mirip bumi menggunakan data transmisi teleskop generasi baru."
    ],
    "9": [
        "Graph Neural Networks untuk deteksi anomali pada topologi jaringan sensor nirkabel terdistribusi.",
        "Arsitektur vision transformer yang efisien komputasi untuk segmentasi citra medis 3D."
    ],
    "10": [
        "Metode dekomposisi dimensi tinggi untuk analisis klasterisasi data sains multi-variat yang sangat jarang (sparse).",
        "Pemodelan dinamis sistem stokastik multi-skala pada data empiris kompleks."
    ],
    "11": [
        "Struktur representasi tak tereduksi dari aljabar Lie berdimensi tak hingga pada bidang matematika murni.",
        "Invarian topologis pada klasifikasi grup abelian berhingga."
    ],
    "12": [
        "Eksistensi dan keunikan solusi lemah (weak solutions) untuk persamaan diferensial parsial non-linear orde tinggi.",
        "Metode numerik elemen hingga adaptif untuk persamaan gelombang elastis pada medium anisotropik."
    ],
    "13": [
        "Bagaimana mempercepat proses sampling pada Latent Diffusion Models tanpa mengorbankan keragaman generasi gambar?",
        "Retrieval-Augmented Generation (RAG) multimodal untuk sintesis jawaban ilmiah berbasis fakta terverifikasi."
    ],
    "14": [
        "Estimasi konstanta Hubble (H0) menggunakan data gravitational lensing quasar dan supernova tipe Ia.",
        "Kendala energi gelap dinamis dari survei struktur skala besar alam semesta terkini."
    ]
}

# -----------------------------------------------------------------------------
# 5. Scikit-Learn Model Loader with Cache
# -----------------------------------------------------------------------------
@st.cache_resource(show_spinner="Memuat Model Machine Learning Scikit-Learn...")
def load_trained_models():
    """Load Scikit-Learn trained KMeans and TF-IDF models from checkpoints directory."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ckpt_dir = os.path.join(base_dir, "..", "01_Clustering_and_Labelling", "checkpoints")
    
    kmeans_path = os.path.join(ckpt_dir, "kmeans_model.joblib")
    tfidf_t_path = os.path.join(ckpt_dir, "tfidf_title.joblib")
    tfidf_a_path = os.path.join(ckpt_dir, "tfidf_abstract.joblib")
    
    if os.path.exists(kmeans_path) and os.path.exists(tfidf_t_path) and os.path.exists(tfidf_a_path):
        try:
            kmeans = joblib.load(kmeans_path)
            tfidf_title = joblib.load(tfidf_t_path)
            tfidf_abstract = joblib.load(tfidf_a_path)
            return {
                "kmeans": kmeans,
                "tfidf_title": tfidf_title,
                "tfidf_abstract": tfidf_abstract,
                "status": "ready"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    return {"status": "not_found"}

models_bundle = load_trained_models()

# -----------------------------------------------------------------------------
# 6. Sidebar Navigation & Branding
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### arXiv Topic Explorer")
    st.caption("Scientific Intelligence & Analytics")
    
    # Model Status Badge
    if models_bundle.get("status") == "ready":
        st.markdown('<span class="quest-chip chip-green">[STATUS: ML ONLINE]</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="quest-chip chip-gold">[STATUS: HEURISTIC]</span>', unsafe_allow_html=True)
    
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown("#### Dashboard Modules")
    st.markdown("""
    - **Overview**: 3.15M Papers & Pipeline
    - **Topic Explorer**: 15 Academic Clusters
    - **Trend Radar**: 8 Temporal Evolutions
    - **AI Predictor**: Real-Time Neural Match
    - **Research Advisor**: Novelty & Gap Finder
    """)
    
    st.markdown("---")
    st.markdown("#### Repository Archives")
    st.markdown("**Cornell University arXiv Dataset**")
    st.caption("3,148,882 Scholarly Metadata (1993-2026)")
    st.markdown("[Open Kaggle Archives ->](https://www.kaggle.com/datasets/Cornell-University/arxiv)")

# -----------------------------------------------------------------------------
# 7. Main Tabs Interface (5 Tabs)
# -----------------------------------------------------------------------------
st.title("arXiv Topic Explorer Dashboard")
st.caption("Mining 3,148,882 Papers with Weighted K-Means & Temporal Intelligence.")

tab_overview, tab_explorer, tab_trends, tab_predictor, tab_advisor = st.tabs([
    "Overview & Pipeline",
    "Topic Explorer",
    "Trend Analysis",
    "AI Paper Predictor",
    "Research Topic Advisor"
])

# =============================================================================
# TAB 1: OVERVIEW & DATA PIPELINE
# =============================================================================
with tab_overview:
    # 4 Metric Cards Grid
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="stat-card-quest">
            <div class="stat-number-quest">3,148,882</div>
            <div class="stat-label-quest">Papers Indexed</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="stat-card-quest">
            <div class="stat-number-quest">15</div>
            <div class="stat-label-quest">Topic Clusters</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="stat-card-quest">
            <div class="stat-number-quest">100,000</div>
            <div class="stat-label-quest">Training Samples</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="stat-card-quest">
            <div class="stat-number-quest">O(1) RAM</div>
            <div class="stat-label-quest">Reservoir Pipeline</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    
    # Methodology & Architecture Cards
    st.markdown("### Data Architecture (Two-Stage Clustering Pipeline)")
    st.markdown("Sistem komputasi dirancang untuk memproses 5.4 GB berkas secara hemat memori tanpa Out-of-Memory (OOM):")
    
    step_col1, step_col2, step_col3, step_col4 = st.columns(4)
    with step_col1:
        st.markdown("""
        <div class="step-box-quest">
            <div class="step-badge-quest">STAGE I</div>
            <h4 style="margin-bottom: 6px;">Reservoir Sampling</h4>
            <p style="font-size: 14px; color: #E5D5C3; margin: 0;">
                Two-pass streaming generator mengambil 100k sampel terstratifikasi berdasarkan proporsi kategori utama arXiv.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with step_col2:
        st.markdown("""
        <div class="step-box-quest">
            <div class="step-badge-quest">STAGE II</div>
            <h4 style="margin-bottom: 6px;">Weighted TF-IDF</h4>
            <p style="font-size: 14px; color: #E5D5C3; margin: 0;">
                Ekstraksi fitur TF-IDF terpisah untuk Judul (bobot 2.0) dan Abstrak (bobot 1.0) lalu digabung dengan sparse hstack.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with step_col3:
        st.markdown("""
        <div class="step-box-quest">
            <div class="step-badge-quest">STAGE III</div>
            <h4 style="margin-bottom: 6px;">K-Means Model</h4>
            <p style="font-size: 14px; color: #E5D5C3; margin: 0;">
                Model K-Means (K=15) dilatih pada 100k sampel, disimpan ke format joblib sebagai checkpoint komputasi.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with step_col4:
        st.markdown("""
        <div class="step-box-quest">
            <div class="step-badge-quest">STAGE IV</div>
            <h4 style="margin-bottom: 6px;">Batch Inference</h4>
            <p style="font-size: 14px; color: #E5D5C3; margin: 0;">
                Prediksi klaster pada seluruh 3.15M paper sisa dijalankan bertahap (batch 100k) dengan dukungan resume otomatis.
            </p>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# TAB 2: TOPIC EXPLORER (15 CLUSTERS)
# =============================================================================
with tab_explorer:
    st.markdown("### 15 Academic Topic Clusters")
    st.markdown("Pilih klaster untuk membedah kata kunci representatif dan profil kategori ground-truth arXiv:")
    
    # Cluster Selector
    cluster_options = [f"Klaster {c['id']} - {c['name'].split(' (')[0]}" for c in CLUSTERS_METADATA.values()]
    selected_option = st.selectbox("Pilih Klaster untuk Ditinjau:", cluster_options, index=7)
    selected_key = str(int(selected_option.split(" - ")[0].replace("Klaster ", "")))
    
    cluster_info = CLUSTERS_METADATA[selected_key]
    
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    # Detail Container
    exp_col1, exp_col2 = st.columns([1.4, 1.0])
    
    with exp_col1:
        st.markdown(f"""
        <div class="quest-card">
            <div style="font-family: 'Cinzel', serif; font-size: 12px; color: #CA8A04; font-weight: 700; letter-spacing: 1px; margin-bottom: 4px;">
                KLASTER {cluster_info['id']} • {cluster_info.get('velocity_status', '')}
            </div>
            <h2 style="font-size: 22px; font-weight: 700; margin-bottom: 18px; color: #F5E6D3;">
                {cluster_info['name']}
            </h2>
            <div style="border-top: 1px solid #5C3D2E; padding-top: 14px; margin-bottom: 14px;">
                <div style="font-family: 'Cinzel', serif; font-size: 12px; font-weight: 700; color: #E5D5C3; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px;">
                    Kata Kunci Utama Judul (Bobot 2.0)
                </div>
                <div>
                    {"".join([f'<span class="quest-chip chip-title-quest">{w}</span>' for w in cluster_info['title_keywords']])}
                </div>
            </div>
            <div style="border-top: 1px solid #5C3D2E; padding-top: 14px;">
                <div style="font-family: 'Cinzel', serif; font-size: 12px; font-weight: 700; color: #E5D5C3; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px;">
                    Kata Kunci Utama Abstrak
                </div>
                <div>
                    {"".join([f'<span class="quest-chip chip-abstract-quest">{w}</span>' for w in cluster_info['abstract_keywords']])}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with exp_col2:
        st.markdown("""
        <div class="quest-card">
            <div style="font-family: 'Cinzel', serif; font-size: 12px; font-weight: 700; color: #CA8A04; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px;">
                Top 3 Kategori arXiv Asli Dominan
            </div>
        """, unsafe_allow_html=True)
        
        for cat in cluster_info["categories"]:
            st.markdown(f"**{cat['name']}** — `{cat['percent']}%`")
            st.progress(cat["percent"] / 100.0)
            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# TAB 3: TREND ANALYSIS (8 TEMPORAL PLOTS)
# =============================================================================
with tab_trends:
    st.markdown("### Temporal Trend Radar (1993 - 2026)")
    st.markdown("Evolusi pergeseran disiplin sains dari 3,14M+ nomor identitas unik arXiv yang diolah cepat menggunakan **Polars Engine**:")
    
    # Trend Filter Categories
    trend_view = st.radio(
        "Pilih Kategori Visualisasi Tren:",
        ["Semua 8 Grafik (Galeri Lengkap)", 
         "1. Evolusi Global (% Pangsa, Heatmap, Stacked Area)", 
         "2. Laju Momentum (Top 5 Tumbuh Cepat & Menurun)", 
         "3. Siklus Hidup & Dominasi (Linimasa #1, Distribusi Usia, Akumulasi)"],
        horizontal=True
    )
    
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    plots_base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "02_Trend_Analysis", "plots")
    
    def render_plot_card(filename, title, desc):
        p_path = os.path.join(plots_base, filename)
        if os.path.exists(p_path):
            st.image(p_path, use_container_width=True)
            st.markdown(f"""
            <div class="intel-brief-quest">
                <strong>{title}:</strong> {desc}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning(f"Berkas grafik `{filename}` belum ditemukan di `{plots_base}`. Jalankan notebook `02_Trend_Analysis/topic_trend_analysis.ipynb` untuk mengekspor.")

    # 1. Evolusi Global
    if "Semua" in trend_view or "Evolusi Global" in trend_view:
        st.markdown("#### 1. Evolusi Popularitas Global & Konsentrasi Sains")
        c1, c2 = st.columns(2)
        with c1:
            render_plot_card("trend_lineplot.png", "1. Garis Tren Popularitas Relatif (%)", "Menunjukkan lonjakan dramatis bidang AI & Deep Learning sejak 2012 menggeser dominasi fisika energi tinggi tradisional.")
        with c2:
            render_plot_card("trend_heatmap.png", "2. Heatmap Evolusi Topik Temporal", "Matriks 2D (Tahun vs Klaster) untuk memetakan periode 'ledakan' publikasi pada setiap sub-bidang sains secara sekilas.")
            
        render_plot_card("trend_stacked_area.png", "3. Komposisi Kumulatif Area Bertumpuk (100%)", "Menggambarkan pergeseran pangsa portofolio sains secara menyeluruh dari tahun ke tahun.")
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # 2. Laju Momentum
    if "Semua" in trend_view or "Laju Momentum" in trend_view:
        st.markdown("#### 2. Kecepatan Tren & Maturasi Bidang Riset (Velocity)")
        c3, c4 = st.columns(2)
        with c3:
            render_plot_card("top_growing_topics.png", "4. Top 5 Hottest Topics (Growth Velocity)", "Klaster dengan akselerasi kenaikan pangsa pasar terbesar dalam 5 tahun terakhir (AI Generatif & Deep Learning).")
        with c4:
            render_plot_card("top_declining_topics.png", "5. Top 5 Coolest Topics (Decline Velocity)", "Bidang yang mengalami penurunan pangsa relatif seiring perpindahan fokus riset ke ranah komputasi.")
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # 3. Siklus Hidup & Dominasi
    if "Semua" in trend_view or "Siklus Hidup" in trend_view:
        st.markdown("#### 3. Siklus Hidup, Usia Publikasi & Akumulasi Pengetahuan")
        c5, c6 = st.columns(2)
        with c5:
            render_plot_card("dominant_topic_timeline.png", "6. Linimasa Topik Nomor 1 Dominan", "Memetakan topik penyumbang volume terbanyak (#1) untuk setiap tahunnya di arXiv dari 1993 sampai 2026.")
        with c6:
            render_plot_card("cluster_year_distribution.png", "7. Sebaran Usia Publikasi per Klaster", "Box plot membedakan bidang mapan/klasik (merata sejak 1993) dengan bidang modern/emerging (sangat padat di tahun akhir).")
            
        render_plot_card("cumulative_growth.png", "8. Pertumbuhan Volume Kumulatif", "Menunjukkan total akumulasi basis pengetahuan sains yang diarsipkan di arXiv per topik.")

# =============================================================================
# TAB 4: AI PAPER PREDICTOR (LIVE MACHINE LEARNING INFERENCE)
# =============================================================================
with tab_predictor:
    st.markdown("### Live AI Paper Topic Classifier")
    st.markdown("Uji draf paper ilmiah Anda langsung pada model Scikit-Learn K-Means untuk memprediksi klaster topik secara real-time:")
    
    # Preset Quick Examples
    st.markdown("**Preset Examples (1-Click Test):**")
    ex_col1, ex_col2, ex_col3 = st.columns(3)
    
    default_title = ""
    default_abstract = ""
    
    if "pred_title" not in st.session_state:
        st.session_state.pred_title = "Attention Is All You Need"
        st.session_state.pred_abstract = "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely."
        
    with ex_col1:
        if st.button("Example 1: Deep Learning & NLP"):
            st.session_state.pred_title = "Attention Is All You Need"
            st.session_state.pred_abstract = "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely."
    with ex_col2:
        if st.button("Example 2: Quantum Information"):
            st.session_state.pred_title = "Experimental Quantum Teleportation of Qubits"
            st.session_state.pred_abstract = "Quantum teleportation is the transmission and reconstruction of an unknown quantum state using entanglement and classical communication. We demonstrate the teleportation of arbitrary polarization states of single photons across superconducting quantum circuits with high fidelity."
    with ex_col3:
        if st.button("Example 3: Astrophysics & Galaxies"):
            st.session_state.pred_title = "Observational Constraints on Dark Matter Distribution in Galaxies"
            st.session_state.pred_abstract = "We present high-resolution radio and optical observations of stellar kinematics and gas emission in nearby spiral galaxies. The rotation curves indicate substantial dark matter halos with gravitational lensing constraints."

    # Input Form
    pred_form_col, pred_res_col = st.columns([1.1, 1.0])
    
    with pred_form_col:
        input_title = st.text_input("Judul Paper (Title):", value=st.session_state.pred_title)
        input_abstract = st.text_area("Abstrak Paper (Abstract):", value=st.session_state.pred_abstract, height=160)
        btn_classify = st.button("Run Neural Classification", type="primary", use_container_width=True)
        
    with pred_res_col:
        if btn_classify or (input_title and input_abstract):
            if not input_title.strip() or not input_abstract.strip():
                st.warning("Mohon masukkan Judul dan Abstrak paper terlebih dahulu.")
            else:
                # -------------------------------------------------------------
                # True Scikit-Learn Inference or Heuristic Fallback
                # -------------------------------------------------------------
                if models_bundle.get("status") == "ready":
                    kmeans = models_bundle["kmeans"]
                    tfidf_title = models_bundle["tfidf_title"]
                    tfidf_abstract = models_bundle["tfidf_abstract"]
                    
                    # 1. Transform text
                    x_t = tfidf_title.transform([input_title]) * 2.0
                    x_a = tfidf_abstract.transform([input_abstract]) * 1.0
                    x_comb = sp.hstack([x_t, x_a])
                    
                    # 2. Predict primary cluster
                    primary_cluster_id = kmeans.predict(x_comb)[0]
                    
                    # 3. Calculate distance to all 15 cluster centers for similarity
                    centers = kmeans.cluster_centers_
                    x_dense = x_comb.toarray()
                    dists = np.linalg.norm(centers - x_dense, axis=1)
                    
                    # Invert distance to score
                    sims = 1.0 / (1.0 + dists)
                    sims_norm = (sims / np.sum(sims)) * 100.0
                    
                    top_indices = np.argsort(sims_norm)[::-1][:3]
                    
                else:
                    # Heuristic Keyword Fallback
                    scores = []
                    t_lower = input_title.lower()
                    a_lower = input_abstract.lower()
                    for k_idx, c_data in CLUSTERS_METADATA.items():
                        score = 0
                        for kw in c_data["title_keywords"]:
                            if kw in t_lower:
                                score += 2.0
                        for kw in c_data["abstract_keywords"]:
                            if kw in a_lower:
                                score += 1.0
                        scores.append(score)
                    scores = np.array(scores)
                    if np.sum(scores) == 0:
                        scores[10] = 1.0  # default general
                    sims_norm = (scores / np.sum(scores)) * 100.0
                    top_indices = np.argsort(sims_norm)[::-1][:3]
                    primary_cluster_id = top_indices[0]
                    
                primary_info = CLUSTERS_METADATA[str(primary_cluster_id)]
                
                # Render Primary Result Banner
                st.markdown(f"""
                <div class="result-banner-quest">
                    <div class="result-cluster-id-quest">PRIMARY CLASSIFICATION MATCH • KLASTER {primary_info['id']}</div>
                    <div class="result-cluster-name-quest">{primary_info['name']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Render Top 3 Match Breakdown
                st.markdown("#### Similarity Breakdown (Top 3):")
                for rank, idx in enumerate(top_indices, 1):
                    cand_info = CLUSTERS_METADATA[str(idx)]
                    pct = sims_norm[idx]
                    st.markdown(f"**#{rank} Klaster {cand_info['id']}** — {cand_info['name'].split(' (')[0]} (`{pct:.1f}%`)")
                    st.progress(float(pct) / 100.0)
                    
                # Feature Keyword Detection
                combined_text = (input_title + " " + input_abstract).lower()
                detected_words = [w for w in (primary_info['title_keywords'] + primary_info['abstract_keywords']) if w in combined_text]
                detected_words = list(dict.fromkeys(detected_words))[:8]
                
                if detected_words:
                    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                    st.markdown("**Detected Feature Keywords:**")
                    st.markdown(" ".join([f'<span class="quest-chip chip-gold">{w}</span>' for w in detected_words]), unsafe_allow_html=True)

# =============================================================================
# TAB 5: RESEARCH TOPIC ADVISOR & GAP FINDER
# =============================================================================
with tab_advisor:
    st.markdown("### Research Topic Advisor & Gap Finder")
    st.markdown("Solusi cerdas bagi peneliti untuk mengatasi *research block*, memilih topik riset berpotensi tinggi, dan menemukan celah riset (*novelty gaps*).")
    
    advisor_mode = st.radio(
        "Pilih Pendekatan Eksplorasi:",
        ["Mode A: Eksplorasi Domain & Celah Riset (Berdasarkan Minat)", 
         "Mode B: Brainstormer Ide & Analisis Kebaruan (Berdasarkan Kata Kunci Awal)"],
        horizontal=True
    )
    
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    # -------------------------------------------------------------------------
    # MODE A: DOMAIN EXPLORER & GAP FINDER
    # -------------------------------------------------------------------------
    if "Mode A" in advisor_mode:
        m_col1, m_col2 = st.columns([1.0, 1.2])
        
        with m_col1:
            st.markdown("#### 1. Tentukan Minat Bidang & Target:")
            domain_choice = st.selectbox(
                "Pilih Domain Keilmuan:",
                list(RESEARCH_DOMAINS.keys()),
                format_func=lambda x: RESEARCH_DOMAINS[x]["name"]
            )
            
            persona_choice = st.selectbox(
                "Pilih Sasaran Riset Anda:",
                [
                    ("hot", "High Velocity / Frontier (Topik Tumbuh Pesat untuk Publikasi Cepat)"),
                    ("gap", "Interdisciplinary Research Gap (Celah Riset Persilangan 2 Bidang)"),
                    ("foundational", "Foundational & Solid Theory (Bidang Mapan Teori Kuat)")
                ],
                format_func=lambda x: x[1]
            )[0]
            
            st.info(RESEARCH_DOMAINS[domain_choice]["summary"])
            
        with m_col2:
            st.markdown("#### 2. Rekomendasi Topik & Celah Riset Terpilih:")
            
            if domain_choice == "cross" or persona_choice == "gap":
                st.markdown("**Rekomendasi Jembatan Riset Antar-Disiplin (*Cross-Domain Bridges*):**")
                for bridge in INTERDISCIPLINARY_BRIDGES:
                    st.markdown(f"""
                    <div class="quest-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                            <span class="quest-chip chip-gold">INTERDISCIPLINARY GAP</span>
                            <span style="font-family: 'Fira Code', monospace; font-size: 12px; color: #E5D5C3;">High Novelty</span>
                        </div>
                        <h3 style="font-size: 18px; margin-bottom: 4px; color: #F5E6D3;">{bridge['title']}</h3>
                        <div style="font-family: 'Cinzel', serif; font-size: 12px; color: #CA8A04; font-weight: 600; margin-bottom: 8px;">
                            {bridge['clusters']}
                        </div>
                        <p style="font-size: 14.5px; color: #E5D5C3; margin-bottom: 10px;">{bridge['desc']}</p>
                        <div style="border-top: 1px solid #5C3D2E; padding-top: 8px; font-size: 14px; color: #F5E6D3;">
                            <strong>Contoh Ide Judul:</strong> <em>"{bridge['sample_title']}"</em>
                        </div>
                        <div style="margin-top: 6px; font-size: 13.5px; color: #E5D5C3;">
                            <strong>Starter Research Question:</strong> {bridge['starter_question']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                target_clusters = RESEARCH_DOMAINS[domain_choice]["clusters"]
                
                # Filter by persona
                if persona_choice == "hot":
                    selected_c_keys = [k for k in target_clusters if "High Growth" in CLUSTERS_METADATA.get(k, {}).get("velocity_status", "")]
                    if not selected_c_keys:
                        selected_c_keys = target_clusters[:2]
                else:
                    selected_c_keys = [k for k in target_clusters if "Foundational" in CLUSTERS_METADATA.get(k, {}).get("velocity_status", "") or "Stable" in CLUSTERS_METADATA.get(k, {}).get("velocity_status", "")]
                    if not selected_c_keys:
                        selected_c_keys = target_clusters[:2]
                        
                for c_key in selected_c_keys:
                    c_info = CLUSTERS_METADATA[c_key]
                    questions = CLUSTER_STARTER_QUESTIONS.get(c_key, ["Bagaimana merancang metodologi baru pada domain ini?"])
                    
                    status_badge = '<span class="quest-chip chip-gold">HIGH VELOCITY</span>' if "High Growth" in c_info.get("velocity_status", "") else '<span class="quest-chip chip-title-quest">FOUNDATIONAL</span>'
                    
                    st.markdown(f"""
                    <div class="quest-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                            {status_badge}
                            <span style="font-family: 'Fira Code', monospace; font-size: 12px; color: #CA8A04;">Growth: {c_info.get('growth_pct', 'N/A')}</span>
                        </div>
                        <h3 style="font-size: 18px; margin-bottom: 6px; color: #F5E6D3;">Klaster {c_info['id']} — {c_info['name']}</h3>
                        <div style="margin-bottom: 10px;">
                            {" ".join([f'<span class="quest-chip chip-abstract-quest">{w}</span>' for w in c_info['title_keywords'][:6]])}
                        </div>
                        <div style="border-top: 1px solid #5C3D2E; padding-top: 8px; font-size: 14px; color: #F5E6D3;">
                            <strong>Contoh Arah / Judul Riset:</strong>
                            <ul style="margin: 4px 0 0 18px; padding: 0;">
                                {"".join([f'<li>{q}</li>' for q in questions])}
                            </ul>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
    # -------------------------------------------------------------------------
    # MODE B: RESEARCH IDEA BRAINSTORMER
    # -------------------------------------------------------------------------
    else:
        st.markdown("#### Masukkan Ide Awal / Minat Topik Anda:")
        st.caption("Ketik beberapa kata kunci atau kalimat draf ide penelitian yang ada di benak Anda:")
        
        b_input = st.text_input(
            "Kata Kunci / Draf Ide Riset:",
            value="deep reinforcement learning for autonomous drone navigation in dynamic obstacles",
            placeholder="Contoh: quantum computing for drug discovery, graph neural networks in financial fraud, etc."
        )
        
        btn_analyze_idea = st.button("Analisis Celah Riset & Kebaruan Ide Ini", type="primary")
        
        if b_input.strip():
            # Analyze input keywords against cluster vocabulary
            text_tokens = b_input.lower().replace(",", " ").split()
            matched_scores = {}
            
            for c_id, c_data in CLUSTERS_METADATA.items():
                score = 0
                for w in c_data["title_keywords"]:
                    if w in b_input.lower():
                        score += 2.0
                for w in c_data["abstract_keywords"]:
                    if w in b_input.lower():
                        score += 1.0
                matched_scores[c_id] = score
                
            sorted_matches = sorted(matched_scores.items(), key=lambda x: x[1], reverse=True)
            top_cluster_id = sorted_matches[0][0] if sorted_matches[0][1] > 0 else "7"
            top_meta = CLUSTERS_METADATA[top_cluster_id]
            
            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            
            res_c1, res_c2 = st.columns([1.1, 1.0])
            
            with res_c1:
                st.markdown(f"""
                <div class="quest-card">
                    <div style="font-family: 'Cinzel', serif; font-size: 11.5px; color: #CA8A04; letter-spacing: 1px; margin-bottom: 4px;">
                        DIAGNOSIS DOMAIN RISET UTAMA
                    </div>
                    <h3 style="font-size: 20px; font-weight: 700; color: #F5E6D3; margin-bottom: 8px;">
                        Klaster {top_meta['id']} — {top_meta['name'].split(' (')[0]}
                    </h3>
                    <div style="margin-bottom: 12px;">
                        <span class="quest-chip chip-gold">STATUS: {top_meta.get('velocity_status', 'Active')}</span>
                        <span class="quest-chip chip-title-quest">Growth: {top_meta.get('growth_pct', 'N/A')}</span>
                    </div>
                    <p style="font-size: 14.5px; color: #E5D5C3; line-height: 1.6;">
                        Topik ini memiliki aktivitas publikasi yang aktif di arXiv. Agar paper Anda memiliki kebaruan (*novelty*) tinggi dan lolos peer-review di jurnal/konferensi top, hindari metodologi standar dan pertimbangkan saran persilangan di samping.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
            with res_c2:
                st.markdown("""
                <div class="quest-card">
                    <div style="font-family: 'Cinzel', serif; font-size: 12px; font-weight: 700; color: #CA8A04; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px;">
                        Saran Suntikan Kebaruan (Novelty Enhancers)
                    </div>
                """, unsafe_allow_html=True)
                
                if top_cluster_id in ["1", "7", "9", "13"]:
                    st.markdown("""
                    - **Saran 1 (Hybrid Constraints):** Gabungkan dengan *Physics-Informed Constraints (PINNs / Lyapunov)* untuk menjamin kepatuhan matematis/fisik model Anda.
                    - **Saran 2 (Controllability):** Jangan hanya gunakan model standar; uji pada skenario *few-shot generalization* atau lingkungan tak terlihat (*unseen environments*).
                    - **Saran 3 (Efficiency):** Pertimbangkan optimasi *parameter-efficient (LoRA/Quantization)* untuk membuktikan efisiensi komputasi.
                    """)
                elif top_cluster_id in ["0", "3", "4", "5", "6", "8", "14"]:
                    st.markdown("""
                    - **Saran 1 (AI for Science):** Terapkan *Graph Neural Networks (GNN)* atau *Diffusion Models* untuk merekonstruksi data eksperimen/observasi.
                    - **Saran 2 (Surrogate Modeling):** Bangun *Machine Learning Surrogate Model* untuk mempercepat komputasi simulasi numerik berorde jam menjadi milidetik.
                    """)
                else:
                    st.markdown("""
                    - **Saran 1 (Empirical Validation):** Padukan formulasi matematis teoritis dengan pengujian data empiris nyata dari domain data terbuka.
                    - **Saran 2 (Scalability):** Buktikan batas kekonvergenan teoritis pada matriks data berdimensi sangat besar.
                    """)
                    
                st.markdown("</div>", unsafe_allow_html=True)
                
            # Starter Outline Draft
            st.markdown("#### Draf Kerangka Usulan Penelitian (Starter Outline Draft):")
            st.markdown(f"""
            <div class="quest-card">
                <p style="margin-bottom: 8px;"><strong>1. Problem Statement:</strong> Mengatasi keterbatasan metode konvensional pada <em>{b_input}</em> dalam menangani ketidakpastian dan efisiensi komputasi.</p>
                <p style="margin-bottom: 8px;"><strong>2. Proposed Methodology:</strong> Mengintegrasikan pendekatan klaster <strong>{top_meta['name'].split(' (')[0]}</strong> dengan evaluasi kuantitatif komprehensif pada dataset benchmark terbuka.</p>
                <p style="margin: 0;"><strong>3. Expected Novelty:</strong> Menunjukkan peningkatan performa, ketahanan (*robustness*), dan efisiensi konvergensi dibandingkan *state-of-the-art* (SOTA) saat ini.</p>
            </div>
            """, unsafe_allow_html=True)
