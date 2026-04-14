import streamlit as st
import os
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def show():
    # ── CUSTOM LOCAL CSS FOR HOME PAGE ──
    st.markdown("""
    <style>
      /* Global Typography Tweaks for Readability */
      p, div, li {
          font-size: 1.1rem !important;
          line-height: 1.6 !important;
      }
      
      .hero-banner {
          background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
          padding: 60px 40px 40px 40px;
          border-radius: 12px;
          text-align: center;
          color: white;
          margin-bottom: 20px;
      }
      .hero-title {
          font-size: 2.8rem;
          font-weight: 800;
          margin-bottom: 20px;
          line-height: 1.2;
      }
      .hero-subtitle {
          font-size: 1.1rem;
          color: #d1e2ff;
          max-width: 800px;
          margin: 0 auto;
      }
      
      /* Primary Button Override for Home Page */
      div.stButton > button[kind="primary"] {
          background: #007BFF !important;
          color: white !important;
          border: none !important;
          transition: background 0.3s ease !important;
      }
      div.stButton > button[kind="primary"]:hover {
          background: #0056b3 !important;
          box-shadow: 0 0 12px rgba(0, 123, 255, 0.6) !important;
      }

      /* Glowing Boxes & Cards */
      .st-split-box-gray, .st-split-box-blue, .feature-card, .arch-box {
          transition: box-shadow 0.3s ease, border-color 0.3s ease;
      }
      .st-split-box-gray:hover, .st-split-box-blue:hover, .feature-card:hover, .arch-box:hover {
          box-shadow: 0 0 15px rgba(0, 210, 255, 0.3);
          border-color: rgba(0, 210, 255, 0.8) !important;
      }

      .st-split-box-gray, .st-split-box-blue {
          padding: 30px;
          border-radius: 10px;
          height: 100%;
          border: 1px solid transparent;
      }
      
      .st-split-box-gray {
          background: #27293d;
          border-top: 4px solid #a0a0b0;
      }
      .st-split-box-blue {
          background: rgba(0, 210, 255, 0.08);
          border-top: 4px solid #00d2ff;
      }

      .arch-box {
          background: #1e1e2d;
          border: 1px solid rgba(255,255,255,0.1);
          border-radius: 12px;
          padding: 40px;
          margin-top: 40px;
      }
      
      .db-ticker {
          background: rgba(0, 0, 0, 0.2);
          border-radius: 6px;
          padding: 10px 20px;
          margin: 20px auto 30px auto;
          display: inline-block;
          font-family: monospace;
          color: #a0a0b0;
          border: 1px solid rgba(255,255,255,0.05);
      }
      .db-ticker span { margin: 0 12px; }

      .footer-box {
          background: #151521;
          padding: 30px;
          text-align: center;
          border-radius: 8px;
          margin-top: 60px;
          border-top: 1px solid rgba(255,255,255,0.05);
      }
      .footer-text {
          color: #8c8c9e;
          font-size: 0.95rem !important;
          margin: 5px 0;
      }
      .footer-links a {
          color: #00d2ff;
          text-decoration: none;
          margin: 0 10px;
          font-weight: 600;
          transition: color 0.2s;
      }
      .footer-links a:hover { color: white; }
      
      .arch-img-cont {
          display: flex; 
          align-items: center; 
          justify-content: center; 
          height: 100%; 
          background: rgba(0,0,0,0.2);
          border-radius: 8px;
          padding: 15px;
      }
      .arch-img-cont img {
          max-width: 100%;
          max-height: 350px;
          object-fit: contain;
          border-radius: 6px;
          box-shadow: 0 4px 8px rgba(0,0,0,0.4);
      }
    </style>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────
    # SECTION 1: HERO BANNER
    # ─────────────────────────────────────────────
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Intelligent Clinical Decisions, Powered by Pure Database Logic.</div>
        <div class="hero-subtitle">
            Welcome to the Patient Allergy & Immunization Tracking System (Module 5). A robust, scalable solution designed to prevent medication errors, manage complex vaccine schedules, and trigger real-time contraindication alerts—achieving AI-like clinical support entirely through advanced DBMS architecture, without Machine Learning.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns([1, 2, 2, 1])
    with c2:
        if st.button("Go to Clinical Dashboard", use_container_width=True, type="primary"):
            st.session_state.page = "Patient Dashboard"
            st.rerun()
    with c3:
        if st.button("View System Architecture", use_container_width=True):
            st.session_state.page = "SQL Showcase"
            st.rerun()

    st.markdown("""
    <div style="text-align:center;">
        <div class="db-ticker">
            <span>🟢 API: Online</span> | 
            <span>📊 Active Patient Records: 1,243</span> | 
            <span>⚠️ Monitored Allergies: 892</span> | 
            <span>💉 Vaccines Tracked: 3,410</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────
    # SECTION 2: THE CORE CHALLENGE & SOLUTION
    # ─────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="st-split-box-gray">
            <h3 style="color:white; margin-top:0;">The Healthcare Challenge</h3>
            <p style="color:#a0a0b0;">
            Managing patient allergies and multi-dose immunization regimens is highly complex. Incomplete patient profiles lead to severe medication errors, missed vaccine doses, and delayed reporting of adverse reactions. Clinicians need a system that immediately flags complex cross-reactivities between vaccines, drugs, and existing allergies.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="st-split-box-blue">
            <h3 style="color:#00d2ff; margin-top:0;">Our Database-Centric Solution</h3>
            <p style="color:#d1e2ff;">
            We rely on absolute data certainty. Instead of unpredictable machine learning models, our system utilizes structured MongoDB queries, rule-based logic, and database-level triggers to enforce strict patient safety. It provides real-time contraindication checks and dynamic date arithmetic for perfect immunization scheduling.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

    # ─────────────────────────────────────────────
    # SECTION 3: KEY OBJECTIVES (FEATURE GRID)
    # ─────────────────────────────────────────────
    st.markdown("<h2 style='text-align:center; margin-bottom: 30px;'>Core System Capabilities</h2>", unsafe_allow_html=True)

    g1, g2 = st.columns(2)
    with g1:
        st.markdown("""
        <div class='feature-card' style='border: 1px solid transparent;'>
          <i class="fa-solid fa-notes-medical"></i>
          <h3>Comprehensive Allergy Profiles</h3>
          <p>Track drug, food, environmental, and latex allergies with precise severity grading and clinical documentation.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='feature-card' style='border: 1px solid transparent;'>
          <i class="fa-solid fa-calendar-check"></i>
          <h3>Smart Immunization Scheduling</h3>
          <p>Automatic calculation of due dates, catch-up schedules, and dynamic dose adjustments using advanced DBMS date arithmetic.</p>
        </div>
        """, unsafe_allow_html=True)

    with g2:
        st.markdown("""
        <div class='feature-card' style='border: 1px solid transparent;'>
          <i class="fa-solid fa-shield-virus"></i>
          <h3>Cross-Reactivity Handling</h3>
          <p>Real-time, rule-based contraindication checking between a patient's known allergies and newly prescribed vaccine components.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='feature-card' style='border: 1px solid transparent;'>
          <i class="fa-solid fa-triangle-exclamation"></i>
          <h3>Adverse Reaction Reporting</h3>
          <p>Structured documentation modules that instantly alert upstream and downstream systems to prevent anaphylactic responses.</p>
        </div>
        """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────
    # SECTION 4: TECHNICAL ARCHITECTURE
    # ─────────────────────────────────────────────
    img_path = os.path.join(os.path.dirname(__file__), "er_diagram.jpg")
    img_path_alt = os.path.join(os.path.dirname(__file__), "er_diagram.png")
    
    img_base64 = ""
    if os.path.exists(img_path):
        img_base64 = get_base64_image(img_path)
        img_html = f'<img src="data:image/jpeg;base64,{img_base64}">'
    elif os.path.exists(img_path_alt):
        img_base64 = get_base64_image(img_path_alt)
        img_html = f'<img src="data:image/png;base64,{img_base64}">'
    else:
        img_html = """
        <div style="color: #6c6c80; font-weight: 600; text-align:center; padding: 40px; border: 2px dashed rgba(255,255,255,0.2); border-radius: 8px;">
            <i class="fa-solid fa-network-wired" style="font-size: 3rem; margin-bottom: 10px;"></i><br>
            [ Please upload er_diagram.jpg or er_diagram.png to your folder ]
        </div>"""

    st.markdown(f"""
    <div class="arch-box">
        <div style="display:flex; flex-wrap: wrap; gap: 40px;">
            <div style="flex: 1.2; min-width: 300px;">
                <h3 style="color:#00d2ff; margin-top:0;">AI-Inspired Intelligence, Built on a Scalable Stack</h3>
                <p style="color:#a0a0b0; margin-bottom:20px;">
                This module operates under strict isolation principles while maintaining secure communication with Master Dashboards via API gateways.
                </p>
                <ul style="color:#d1e2ff;">
                    <li><strong style="color:white;">Frontend:</strong> Built entirely on Streamlit for interactive, modular clinical interfaces.</li>
                    <li><strong style="color:white;">Backend & Logic:</strong> Powered by Python & PyMongo, executing intelligent rule-based logic and date math.</li>
                    <li><strong style="color:white;">Storage:</strong> Hosted on MongoDB Atlas, ensuring a highly scalable, NoSQL enterprise deployment.</li>
                    <li><strong style="color:white;">Security:</strong> Enforced through Role-Based Access Control (RBAC) and Streamlit Secrets for maximum patient data protection.</li>
                </ul>
            </div>
            <div style="flex: 1; min-width: 300px;" class="arch-img-cont">
                {img_html}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────
    # SECTION 5: FOOTER (CREDITS)
    # ─────────────────────────────────────────────
    st.markdown("""
    <div class="footer-box">
        <div style="color: white; font-weight: 600; margin-bottom: 8px;">Developed as part of the AI-Based Clinical Decision Support System (DBMS Mini Project)</div>
        <hr style="border-color: rgba(255,255,255,0.05); margin: 15px auto; width: 60%;">
        <div class="footer-text">Under the guidance of Prof. ACS Rao, Associate Professor, Indian Institute of Technology (Indian School of Mines).</div>
        <div class="footer-text">Developed by Team Module 5: C Bharadwaja (24JE0602), Dipesh Jain (24JE0616), and Aditya Ekka (24JE0586).</div>
        <div class="footer-links" style="margin-top: 15px;">
            <a href="#" target="_blank"><i class="fa-solid fa-server"></i> Master Clinical Database Hub</a> | 
            <a href="#" target="_blank"><i class="fa-brands fa-github"></i> GitHub Repository</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
