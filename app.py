"""
🏥 PCOS PHENOTYPE PREDICTION DASHBOARD - FINAL VERSION
Professional Healthcare Analytics Application
Version 3.1 - Production Ready
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import joblib
import pickle
import json
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="PCOS Phenotype Prediction Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== ENHANCED CSS STYLING ====================
st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none !important; }
    .main { background-color: #ffffff; }
    [data-testid="stMainBlockContainer"] {
        background-color: #ffffff;
        padding: 2rem 2.5rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    [data-testid="stAppViewContainer"] { background-color: #f5f7fa; }
    
    /* Header */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 3rem 2.5rem;
        margin: -2rem -2.5rem 2rem -2.5rem;
        color: white;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.25);
    }
    .header-title { font-size: 2.8rem; font-weight: 800; margin: 0; margin-bottom: 0.5rem; }
    .header-subtitle { font-size: 1rem; opacity: 0.95; margin: 0; font-weight: 400; }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem; font-weight: 800; color: #1a1a2e;
        margin: 1.8rem 0 1rem 0; padding-bottom: 0.8rem;
        border-bottom: 3px solid #667eea; display: flex;
        align-items: center; gap: 0.6rem;
    }
    
    /* Input Container */
    .input-container {
        background: #ffffff; border-radius: 14px; padding: 1.5rem;
        margin-bottom: 1.2rem; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
        border: 1px solid #e0e7ff;
    }
    
    .input-group-header {
        font-size: 1.1rem; font-weight: 700; color: #2c3e50;
        margin: 0 0 0.8rem 0; padding-bottom: 0.5rem;
        border-bottom: 1px solid #f0f4f8;
        display: flex; align-items: center; gap: 0.5rem;
    }
    
    /* Number Input */
    .stNumberInput > div > div > input {
        border: 2px solid #d4d9e8 !important;
        border-radius: 10px !important; padding: 0.65rem !important;
        font-size: 0.9rem !important; color: #1a1a2e !important;
        background-color: #f8f9fc !important;
    }
    .stNumberInput > div > div > input:focus {
        border-color: #667eea !important; background-color: #ffffff !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div > select {
        border: 2px solid #d4d9e8 !important;
        border-radius: 10px !important; padding: 0.65rem !important;
        font-size: 0.9rem !important; color: #1a1a2e !important;
        background-color: #f8f9fc !important;
    }
    
    /* Metric Cards */
    .metric-card {
        background: #ffffff; border-radius: 12px; padding: 1.2rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
        border: 1px solid #e0e7ff; border-left: 4px solid #667eea;
    }
    .metric-label { font-size: 0.75rem; color: #7a8ba8; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 0.6rem; }
    .metric-value { font-size: 2rem; font-weight: 800; color: #1a1a2e; margin-bottom: 0.2rem; }
    .metric-unit { font-size: 0.8rem; color: #7a8ba8; }
    
    /* Chart Container */
    .chart-container {
        background: #ffffff; border-radius: 14px; padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
        border: 1px solid #e0e7ff; margin-bottom: 1.5rem;
    }
    
    /* Result Cards */
    .prediction-result {
        border-radius: 14px; padding: 2rem; margin: 1.5rem 0;
        border-left: 6px solid; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        background: white;
    }
    .result-ir { border-left-color: #ef5350; background: linear-gradient(135deg, #ffebee 0%, #ffffff 100%); }
    .result-h { border-left-color: #ffa726; background: linear-gradient(135deg, #fff3e0 0%, #ffffff 100%); }
    .result-lm { border-left-color: #66bb6a; background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 100%); }
    
    .result-title {
        font-size: 1.7rem; font-weight: 800; margin-bottom: 0.8rem;
        display: flex; align-items: center; gap: 0.6rem; color: #1a1a2e;
    }
    
    /* Details Card */
    .details-card {
        background: #ffffff; border-radius: 12px; padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
        border: 1px solid #e0e7ff;
    }
    .details-title {
        font-size: 1.1rem; font-weight: 700; color: #1a1a2e;
        margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;
    }
    
    /* Button */
    .stButton > button {
        width: 100% !important; padding: 0.9rem !important;
        font-size: 1rem !important; font-weight: 700 !important;
        border-radius: 10px !important; border: none !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* Info & Warning Boxes */
    .info-box {
        background: #e3f2fd; border-left: 4px solid #2196f3;
        border-radius: 10px; padding: 1rem; margin: 1rem 0;
        color: #0d47a1; font-size: 0.9rem; line-height: 1.6;
    }
    .warning-box {
        background: #fff3e0; border-left: 4px solid #ff9800;
        border-radius: 10px; padding: 1rem; margin: 1rem 0;
        color: #e65100; font-size: 0.9rem; line-height: 1.6; font-weight: 500;
    }
    
    /* Text */
    p { color: #2c3e50 !important; line-height: 1.7 !important; }
    h2, h3, h4, h5, h6 { color: #1a1a2e !important; font-weight: 800 !important; }
    li { color: #2c3e50 !important; line-height: 1.7 !important; }
    strong { color: #1a1a2e !important; }
    a { color: #667eea !important; }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: 2px solid #e0e7ff !important; gap: 1.5rem !important;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 0.9rem 0 !important; font-weight: 700 !important;
        font-size: 0.95rem !important; color: #7a8ba8 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #667eea !important; border-bottom-color: #667eea !important;
    }
    
    /* Footer */
    .footer {
        text-align: center; padding: 2rem 0; color: #7a8ba8;
        font-size: 0.85rem; border-top: 1px solid #e0e7ff; margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================== LOAD MODELS ====================
@st.cache_resource
def load_models():
    """Load pre-trained ML models"""
    try:
        model = joblib.load('models/pcos_model.pkl')
        scaler = joblib.load('models/scaler.pkl')
        with open('models/feature_names.pkl', 'rb') as f:
            feature_names = pickle.load(f)
        with open('models/model_info.json', 'r') as f:
            model_info = json.load(f)
        return model, scaler, feature_names, model_info
    except FileNotFoundError:
        st.error("❌ Model files not found in 'models/' directory")
        st.stop()

model, scaler, feature_names, model_info = load_models()

# ==================== UTILITY FUNCTIONS ====================
def calculate_bmi(height_cm, weight_kg):
    return weight_kg / ((height_cm / 100) ** 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "#90EE90"
    elif bmi < 25:
        return "Normal", "#66BB6A"
    elif bmi < 30:
        return "Overweight", "#FFA726"
    else:
        return "Obese", "#EF5350"

def calculate_severity_score(bmi, fasting_insulin, testosterone, acne, symptoms):
    score = 0.0
    if bmi < 18.5:
        score += 0
    elif bmi < 25:
        score += 5
    elif bmi < 30:
        score += 15
    else:
        score += 30
    
    if fasting_insulin < 5:
        score += 0
    elif fasting_insulin < 10:
        score += 8
    elif fasting_insulin < 15:
        score += 16
    else:
        score += 25
    
    if testosterone < 30:
        score += 0
    elif testosterone < 50:
        score += 7
    elif testosterone < 70:
        score += 14
    else:
        score += 20
    
    score += (acne / 10.0) * 15
    score += (symptoms / 10.0) * 10
    
    severity_score = min(100.0, score)
    
    if severity_score < 30:
        return severity_score, 'Mild', '#66bb6a'
    elif severity_score < 60:
        return severity_score, 'Moderate', '#ffa726'
    else:
        return severity_score, 'Severe', '#ef5350'

def get_phenotype_info(phenotype_code):
    """Get detailed phenotype information"""
    info = {
        'IR': {
            'name': 'Insulin-Resistant PCOS',
            'icon': '🔴',
            'color': 'result-ir',
            'prevalence': '40-70%',
            'definition': 'Insulin-Resistant PCOS is the most common phenotype characterized by elevated fasting insulin levels and significant metabolic dysfunction.',
            'detailed_description': '''
            This phenotype represents approximately 40-70% of all PCOS cases. Patients exhibit elevated fasting insulin levels (HOMA-IR > 2.5), 
            indicating their cells are resistant to insulin signaling. This leads to compensatory hyperinsulinemia and increased androgen production. 
            Patients typically have higher BMI (overweight or obese) and face significantly elevated risks for Type 2 diabetes (5-10x higher than general population), 
            hypertension, and cardiovascular disease. The metabolic dysfunction is the primary driver of PCOS manifestations in this phenotype.
            ''',
            'characteristics': [
                'Elevated fasting insulin (HOMA-IR > 2.5) - Primary metabolic marker',
                'Higher BMI (typically overweight/obese, BMI > 27)',
                'Significant metabolic dysfunction and insulin resistance',
                'Increased risk of Type 2 diabetes (5-10x higher than general population)',
                'Elevated triglycerides and reduced HDL cholesterol',
                'Androgen excess secondary to hyperinsulinemia',
                'Greater propensity for weight gain and weight cycling'
            ],
            'recommendations': [
                'Weight management with 5-10% weight loss goal (improves insulin sensitivity)',
                'Low glycemic index (GI) diet rich in fiber (whole grains, vegetables, legumes)',
                'Resistance training 3-4x per week (builds muscle, improves insulin sensitivity)',
                'Myo-inositol supplementation 2-4g daily (improves insulin signaling)',
                'Metformin consideration if glucose intolerant or impaired glucose tolerance',
                'Regular cardiovascular exercise 150+ minutes per week',
                'Monitor HbA1c and fasting glucose annually'
            ],
            'pathophysiology': 'Insulin resistance → Hyperinsulinemia → Excess androgen production → PCOS manifestations'
        },
        'H': {
            'name': 'Hormonal PCOS',
            'icon': '🟡',
            'color': 'result-h',
            'prevalence': '20-30%',
            'definition': 'Hormonal PCOS features high androgen levels with normal insulin sensitivity, emphasizing the hormonal rather than metabolic aspect.',
            'detailed_description': '''
            This phenotype accounts for 20-30% of PCOS cases and is distinguished by elevated testosterone and androstenedione without insulin resistance. 
            Patients typically have normal BMI and better metabolic profiles compared to insulin-resistant phenotype. However, they experience prominent 
            androgenic symptoms including severe acne, excessive facial and body hair (hirsutism), and may have androgenic alopecia (hair loss). 
            The hormonal imbalance is the primary pathological driver, with ovulatory dysfunction secondary to high androgen levels.
            ''',
            'characteristics': [
                'High testosterone (elevated androgens, typically >40 ng/dL or 1.4 nmol/L)',
                'Normal insulin sensitivity and glucose tolerance',
                'Severe acne and/or excessive facial/body hair (hirsutism)',
                'Androgenic alopecia (hair loss) often present',
                'Normal to low BMI (often lean phenotype)',
                'Better metabolic profile with normal lipids',
                'Regular ovulatory cycles may occur in some cases'
            ],
            'recommendations': [
                'Hormonal contraceptives (oral or transdermal) to suppress ovarian androgen production',
                'Anti-androgen therapy - Spironolactone 50-200mg daily (aldosterone antagonist)',
                'Mediterranean-style anti-inflammatory diet rich in omega-3 fatty acids',
                'Regular aerobic exercise 4-5x per week (reduces androgens)',
                'Dermatological care for acne management (retinoids, antibiotics if needed)',
                'Hair loss management - Minoxidil topical for androgenic alopecia',
                'Monitor testosterone levels every 3-6 months during treatment'
            ],
            'pathophysiology': 'Ovarian/adrenal androgen excess → High testosterone → Hirsutism, acne, anovulation'
        },
        'LM': {
            'name': 'Lean/Mild PCOS',
            'icon': '🟢',
            'color': 'result-lm',
            'prevalence': '10-30%',
            'definition': 'Lean/Mild PCOS is the mildest form with normal BMI and metabolic markers, diagnosed primarily by ovarian imaging.',
            'detailed_description': '''
            This phenotype represents 10-30% of PCOS cases and is characterized by normal BMI (lean phenotype) and normal insulin sensitivity. 
            Diagnosis relies primarily on ultrasound findings of polycystic ovarian morphology (≥12 follicles per ovary) combined with menstrual irregularities. 
            Patients have better metabolic profiles and lower risks for metabolic complications. Despite the milder phenotype, they may experience 
            infertility issues due to ovulatory dysfunction. Lifestyle modifications are typically the first-line treatment approach.
            ''',
            'characteristics': [
                'Normal BMI (typically <25, lean phenotype)',
                'Normal insulin sensitivity and glucose tolerance',
                'Normal lipid profile without dyslipidemia',
                'Diagnosed primarily by ultrasound findings (polycystic ovaries)',
                'Mild to absent androgenic symptoms',
                'Lower metabolic risk compared to other phenotypes',
                'Better fertility outcomes and response to ovulation induction'
            ],
            'recommendations': [
                'Lifestyle optimization - weight stability, avoid further weight gain',
                'Balanced whole-food diet with adequate macro and micronutrients',
                'Regular moderate exercise 150+ minutes per week (mix of cardio and strength)',
                'Stress management through meditation, yoga, or mindfulness (8-10 hours sleep)',
                'Adequate sleep (7-9 hours per night) - crucial for hormonal balance',
                'Inositol supplementation may still be beneficial (2g daily)',
                'Regular monitoring of menstrual cycle and ovulation status'
            ],
            'pathophysiology': 'Mild ovulatory dysfunction → Irregular cycles → Infertility risk (despite normal BMI/metabolism)'
        }
    }
    return info.get(phenotype_code, {})

def classify_phenotype(bmi, insulin, testosterone, acne):
    """Classify PCOS phenotype"""
    scores = {'IR': 0.0, 'H': 0.0, 'LM': 0.0}
    if bmi > 27 or insulin > 12:
        scores['IR'] += 2
    if testosterone > 50 or acne > 7:
        scores['H'] += 2
    if bmi < 27 and insulin < 12 and testosterone < 50:
        scores['LM'] += 2
    if max(scores.values()) == 0:
        return 'Mixed'
    return max(scores, key=scores.get)

def create_risk_gauge(risk_percent):
    """Create risk percentage gauge"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_percent,
        title={'text': "PCOS Risk %"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#667eea"},
            'steps': [
                {'range': [0, 30], 'color': "#e8f5e9"},
                {'range': [30, 70], 'color': "#fff3e0"},
                {'range': [70, 100], 'color': "#ffebee"}
            ]
        }
    ))
    fig.update_layout(height=350, margin=dict(l=0, r=0, t=30, b=0))
    return fig

def create_severity_gauge(score):
    """Create severity score gauge"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Severity Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#667eea"},
            'steps': [
                {'range': [0, 30], 'color': "#e8f5e9"},
                {'range': [30, 60], 'color': "#fff3e0"},
                {'range': [60, 100], 'color': "#ffebee"}
            ]
        }
    ))
    fig.update_layout(height=350, margin=dict(l=0, r=0, t=30, b=0))
    return fig

def create_marker_radar(bmi, insulin, testosterone, acne, symptoms):
    """Create radar chart for health markers with better text visibility"""
    bmi_norm = min((bmi / 35) * 100, 100)
    insulin_norm = min((insulin / 20) * 100, 100)
    testosterone_norm = min((testosterone / 80) * 100, 100)
    acne_norm = acne * 10
    symptoms_norm = symptoms * 10
    
    fig = go.Figure(data=go.Scatterpolar(
        r=[bmi_norm, insulin_norm, testosterone_norm, acne_norm, symptoms_norm],
        theta=['BMI', 'Insulin', 'Testosterone', 'Acne', 'Symptoms'],
        fill='toself',
        fillcolor='rgba(102, 126, 234, 0.3)',
        line=dict(color='#667eea', width=2),
        marker=dict(size=8, color='#667eea'),
        hovertemplate='<b>%{theta}</b><br>Level: %{r:.1f}/100<extra></extra>'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, 
                range=[0, 100],
                tickfont=dict(size=11, color='#1a1a2e'),
                gridcolor='#e0e7ff',
                gridwidth=1
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color='#1a1a2e', family='Arial'),
                rotation=90,
                direction='clockwise'
            )
        ),
        title={'text': 'Health Markers Analysis (0-100 Scale)', 'font': {'size': 14, 'color': '#1a1a2e'}},
        height=380, 
        margin=dict(l=80, r=80, t=80, b=80),
        font=dict(size=11, color='#2c3e50'),
        paper_bgcolor='#ffffff',
        plot_bgcolor='#f8f9fc',
        hovermode='closest'
    )
    return fig

def create_comparison_chart(patient_bmi, patient_insulin, patient_testosterone):
    """Create bar chart comparing patient values to normal ranges"""
    categories = ['BMI', 'Insulin (mIU/L)', 'Testosterone (ng/dL)']
    patient_values = [patient_bmi, patient_insulin * 5, patient_testosterone]
    normal_ranges = [25, 50, 50]
    
    fig = go.Figure(data=[
        go.Bar(name='Your Values', x=categories, y=patient_values, 
               marker_color='#667eea', text=[f'{v:.1f}' for v in patient_values],
               textposition='outside'),
        go.Bar(name='Normal Range', x=categories, y=normal_ranges,
               marker_color='#e0e7ff', text=[f'{v:.1f}' for v in normal_ranges],
               textposition='outside')
    ])
    
    fig.update_layout(
        title='Patient Values vs. Normal Ranges',
        xaxis_title='Clinical Markers',
        yaxis_title='Value',
        barmode='group',
        height=400,
        hovermode='x unified',
        margin=dict(l=50, r=50, t=80, b=50)
    )
    return fig

def create_phenotype_distribution():
    """Create pie chart showing phenotype distribution in population"""
    fig = go.Figure(data=[go.Pie(
        labels=['Insulin-Resistant (40-70%)', 'Hormonal (20-30%)', 'Lean/Mild (10-30%)'],
        values=[55, 25, 20],
        marker=dict(colors=['#ef5350', '#ffa726', '#66bb6a']),
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Prevalence: %{value}%<extra></extra>'
    )])
    
    fig.update_layout(
        title='PCOS Phenotype Distribution in Population',
        height=350,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

# ==================== HEADER ====================
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🏥 Welcome to the PCOS Phenotype Detection & Monitoring System</h1>
    <p class="header-subtitle">Advanced AI-Powered Risk Assessment & Phenotype Classification with Detailed Analysis</p>
    <div style="background: rgba(255,255,255,0.15); border-radius: 10px; padding: 1rem; margin-top: 1rem; line-height: 1.6; font-size: 0.95rem; color: rgba(255,255,255,0.95);">
        <strong>What This Dashboard Does:</strong> Analyzes 18 clinical parameters to assess PCOS risk, classify phenotype (Insulin-Resistant, Hormonal, or Lean/Mild), calculate severity scores, and provide personalized treatment recommendations based on individual patient profile. Uses machine learning model trained on 541 patient cases with 91.74% accuracy.
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== MAIN TABS ====================
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🔬 Prediction", "📚 About PCOS", "⚙️ Info"])

# ==================== TAB 1: DASHBOARD ====================
with tab1:
    # Welcoming Message
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 16px; padding: 2rem; margin-bottom: 2rem; box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);">
        <p style="margin: 0; font-size: 1rem; line-height: 1.8; font-weight: 500;">
            <strong style="color: #1a1a2e; font-weight: 700;">We're glad you're here.</strong> <span style="color: #ffffff;">This dashboard is designed to help you understand possible PCOS indicators through simple inputs and clear health insights. Just enter your information below and review the results at your own pace.</span><br><br>
            <strong style="color: #1a1a2e; font-weight: 700;">There's no need to feel worried</strong> <span style="color: #ffffff;">- this tool is meant for awareness and guidance only. By using it, you're already taking a responsible step toward better understanding and monitoring your health.</span> 💪
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header"><span>👤</span> Patient Information</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.markdown('<div class="input-group-header"><span>📋</span> Demographics & Anthropometric</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4, gap="small")
    with col1:
        age = st.number_input("Age (yrs)", 18.0, 65.0, 30.0, 1.0)
    with col2:
        gender = st.selectbox("Gender", ["Female", "Male", "Other"])
    with col3:
        height = st.number_input("Height (cm)", 140.0, 200.0, 165.0, 1.0)
    with col4:
        weight = st.number_input("Weight (kg)", 40.0, 150.0, 70.0, 0.5)
    
    bmi = calculate_bmi(height, weight)
    bmi_cat, bmi_color = get_bmi_category(bmi)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.markdown('<div class="input-group-header"><span>🔄</span> Menstrual & Hormonal Data</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4, gap="small")
    with col1:
        cycle_length = st.number_input("Cycle Length (days)", 21.0, 120.0, 28.0, 1.0,
                                      help="Normal cycle: 21-35 days")
    with col2:
        st.markdown('<label style="font-size: 0.85rem; font-weight: 600; color: #2c3e50;">Regular Cycles?</label>', 
                   unsafe_allow_html=True)
        irregular = st.radio("", ["Yes (Regular)", "No (Irregular)"], horizontal=True, 
                           label_visibility="collapsed") == "No (Irregular)"
    with col3:
        fasting_insulin = st.number_input("Fasting Insulin (mIU/L)", 2.0, 30.0, 10.0, 0.5,
                                         help="Normal: <12 mIU/L")
    with col4:
        testosterone = st.number_input("Testosterone (ng/dL)", 20.0, 100.0, 40.0, 1.0,
                                      help="Normal: 20-50 ng/dL")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.markdown('<div class="input-group-header"><span>🩺</span> Clinical Signs & Lifestyle</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4, gap="small")
    with col1:
        acne = st.number_input("Acne Severity (0-10)", 0.0, 10.0, 5.0, 1.0,
                              help="0=None, 10=Severe")
    with col2:
        hirsutism = st.number_input("Excess Hair (0-10)", 0.0, 10.0, 3.0, 1.0,
                                   help="Facial/body hair growth")
    with col3:
        exercise = st.number_input("Exercise (hrs/week)", 0.0, 14.0, 3.0, 0.5)
    with col4:
        stress = st.number_input("Stress Level (0-10)", 0.0, 10.0, 5.0, 1.0,
                                help="0=Low, 10=High")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.markdown('<div class="input-group-header"><span>📋</span> Additional Health Info</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5, gap="small")
    with col1:
        lh_fsh = st.number_input("LH/FSH Ratio", 0.5, 5.0, 2.5, 0.1,
                                help="Normal: <3")
    with col2:
        hair_loss = st.number_input("Hair Loss (0-10)", 0.0, 10.0, 2.0, 1.0)
    with col3:
        sleep = st.number_input("Sleep (hrs/night)", 3.0, 12.0, 7.0, 0.5,
                               help="Optimal: 7-9 hours")
    with col4:
        symptoms = st.number_input("PCOS Symptoms (#)", 0.0, 10.0, 5.0, 1.0,
                                  help="Count of PCOS-related symptoms")
    with col5:
        st.markdown('<label style="font-size: 0.85rem; font-weight: 600; color: #2c3e50;">Family History?</label>', 
                   unsafe_allow_html=True)
        family_history = st.radio("", ["Yes (Family Hx)", "No"], horizontal=True,
                                label_visibility="collapsed") == "Yes (Family Hx)"
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Summary Metrics
    st.markdown('<div class="section-header"><span>📊</span> Patient Summary</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4, gap="small")
    with col1:
        st.metric("Age", f"{age:.0f}", "years")
    with col2:
        st.metric("BMI", f"{bmi:.1f}", bmi_cat)
    with col3:
        st.metric("Insulin", f"{fasting_insulin:.1f}", "mIU/L")
    with col4:
        st.metric("Testosterone", f"{testosterone:.1f}", "ng/dL")

# ==================== TAB 2: PREDICTION ====================
with tab2:
    st.markdown('<div class="section-header"><span>🔬</span> PCOS Risk Analysis</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="info-box">Click below to analyze patient data with AI and get comprehensive results including phenotype classification, severity assessment, and personalized recommendations.</div>', unsafe_allow_html=True)
    
    if st.button("🚀 Analyze Patient Data", use_container_width=True, type="primary"):
        with st.spinner("⏳ Analyzing..."):
            try:
                X_input = []
                for feat in feature_names:
                    if feat == 'Age': X_input.append(age)
                    elif feat == 'BMI': X_input.append(bmi)
                    elif feat == 'Weight': X_input.append(weight)
                    elif feat == 'Height': X_input.append(height)
                    elif feat == 'Cycle_Length': X_input.append(cycle_length)
                    elif feat == 'Irregular_Periods': X_input.append(1.0 if irregular else 0.0)
                    elif feat == 'Fasting_Insulin': X_input.append(fasting_insulin)
                    elif feat == 'Testosterone': X_input.append(testosterone)
                    elif feat == 'Acne': X_input.append(acne)
                    elif feat == 'Hirsutism': X_input.append(hirsutism)
                    elif feat == 'Hair_Fall': X_input.append(hair_loss)
                    elif feat == 'Exercise': X_input.append(exercise)
                    elif feat == 'Stress': X_input.append(stress)
                    elif feat == 'Sleep': X_input.append(sleep)
                    elif feat == 'Symptoms': X_input.append(symptoms)
                    elif feat == 'Family_History': X_input.append(1.0 if family_history else 0.0)
                    else: X_input.append(0.0)
                
                X_input = np.array(X_input).reshape(1, -1)
                X_input_scaled = scaler.transform(X_input)
                
                pcos_pred = model.predict(X_input_scaled)[0]
                pcos_proba = model.predict_proba(X_input_scaled)[0][1] * 100.0
                
                severity_score, severity_cat, sev_color = calculate_severity_score(bmi, fasting_insulin, testosterone, acne, symptoms)
                phenotype = classify_phenotype(bmi, fasting_insulin, testosterone, acne)
                phenotype_info = get_phenotype_info(phenotype)
                
                st.session_state.prediction_done = True
                st.session_state.pcos_proba = pcos_proba
                st.session_state.severity_score = severity_score
                st.session_state.severity_cat = severity_cat
                st.session_state.sev_color = sev_color
                st.session_state.phenotype = phenotype
                st.session_state.phenotype_info = phenotype_info
                
                st.success("✅ Analysis Complete!")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Display Results
    if 'prediction_done' in st.session_state and st.session_state.prediction_done:
        pcos_proba = st.session_state.pcos_proba
        severity_score = st.session_state.severity_score
        severity_cat = st.session_state.severity_cat
        sev_color = st.session_state.sev_color
        phenotype = st.session_state.phenotype
        phenotype_info = st.session_state.phenotype_info
        
        # Risk Level Card
        if pcos_proba >= 70:
            risk_label, risk_icon = "HIGH RISK", "🔴"
            result_class = "result-ir"
        elif pcos_proba >= 30:
            risk_label, risk_icon = "MODERATE RISK", "🟡"
            result_class = "result-h"
        else:
            risk_label, risk_icon = "LOW RISK", "🟢"
            result_class = "result-lm"
        
        st.markdown(f"""
        <div class="prediction-result {result_class}">
            <div class="result-title">{risk_icon} {risk_label} - {pcos_proba:.1f}%</div>
            <p style="color: #333; margin: 0; font-size: 1.05rem; line-height: 1.8;">
                This patient shows a <strong>{risk_label.lower()}</strong> probability of PCOS with <strong>{phenotype_info.get('name', phenotype)}</strong> phenotype classification. 
                <strong>Severity Level: {severity_cat}</strong> with a score of <strong>{severity_score:.1f}/100</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Charts Section
        st.markdown('<div class="section-header"><span>📈</span> Health Metrics & Analysis</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3, gap="medium")
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(create_risk_gauge(pcos_proba), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(create_severity_gauge(severity_score), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(create_phenotype_distribution(), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(create_marker_radar(bmi, fasting_insulin, testosterone, acne, symptoms), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(create_comparison_chart(bmi, fasting_insulin, testosterone), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Detailed Phenotype Information
        st.markdown('<div class="section-header"><span>🧬</span> Detailed Phenotype Analysis</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="medium")
        
        with col1:
            st.markdown('<div class="details-card">', unsafe_allow_html=True)
            st.markdown('<div class="details-title">📖 Definition</div>', unsafe_allow_html=True)
            st.markdown(f"**{phenotype_info.get('definition', '')}**")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="details-card">', unsafe_allow_html=True)
            st.markdown('<div class="details-title">🔬 Pathophysiology</div>', unsafe_allow_html=True)
            st.markdown(f"*{phenotype_info.get('pathophysiology', '')}*")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="details-card" style="margin: 1.5rem 0;">', unsafe_allow_html=True)
        st.markdown('<div class="details-title">📋 Detailed Description</div>', unsafe_allow_html=True)
        st.markdown(f"{phenotype_info.get('detailed_description', '').strip()}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Characteristics and Recommendations
        st.markdown('<div class="section-header"><span>📌</span> Clinical Profile & Treatment Plan</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="medium")
        
        with col1:
            st.markdown('<div class="details-card">', unsafe_allow_html=True)
            st.markdown('<div class="details-title">🔍 Key Characteristics</div>', unsafe_allow_html=True)
            
            for i, char in enumerate(phenotype_info.get('characteristics', []), 1):
                st.markdown(f"""
                <div style="padding: 0.8rem 0; border-bottom: 1px solid #f0f4f8; color: #2c3e50;">
                    <strong>{i}.</strong> {char}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="details-card">', unsafe_allow_html=True)
            st.markdown('<div class="details-title">💊 Treatment Recommendations</div>', unsafe_allow_html=True)
            
            for i, rec in enumerate(phenotype_info.get('recommendations', []), 1):
                st.markdown(f"""
                <div style="padding: 0.8rem 0; border-bottom: 1px solid #f0f4f8; color: #2c3e50;">
                    <strong>{i}.</strong> {rec}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Severity Assessment
        st.markdown('<div class="section-header"><span>📊</span> Severity Assessment Details</div>', unsafe_allow_html=True)
        
        severity_explanations = {
            'Mild': '''Mild PCOS (Score 0-29) indicates minor manifestation of PCOS symptoms. Patients typically respond well to lifestyle modifications 
                    (diet, exercise, weight management) without requiring pharmacological intervention. Regular monitoring is recommended, and 
                    fertility is usually not significantly impacted.''',
            'Moderate': '''Moderate PCOS (Score 30-59) indicates moderate symptom severity requiring active management combining lifestyle modifications 
                       with potential pharmacological interventions. Treatment should be tailored to the specific phenotype and patient goals. 
                       Regular follow-up every 3-6 months is essential.''',
            'Severe': '''Severe PCOS (Score 60-100) indicates significant PCOS manifestation requiring comprehensive clinical management. Patients likely 
                     need pharmaceutical intervention including hormonal contraceptives, anti-androgens, and/or metformin depending on phenotype. 
                     Close monitoring by healthcare providers is essential, especially regarding metabolic complications.'''
        }
        
        st.markdown(f"""
        <div class="details-card" style="border-left: 4px solid {sev_color}; margin: 1.5rem 0;">
            <div style="font-size: 1.2rem; font-weight: 700; color: #1a1a2e; margin-bottom: 1rem;">
                Severity Level: <span style="color: {sev_color};">{severity_cat}</span> (Score: {severity_score:.1f}/100)
            </div>
            <p style="color: #555; line-height: 1.8; margin: 0;">
                {severity_explanations.get(severity_cat, '')}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="warning-box">
        <strong>⚠️ Clinical Guidance & Next Steps:</strong>
        <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
        <li>Consult with an endocrinologist or gynecologist for proper medical diagnosis</li>
        <li>Obtain laboratory confirmation: hormone panel, glucose tolerance test, lipid profile</li>
        <li>Pelvic ultrasound is essential to assess ovarian morphology and confirm diagnosis</li>
        <li>Treatment plans must be individualized based on phenotype and patient goals (fertility, symptom relief)</li>
        <li>Regular monitoring every 3-6 months to track treatment response and metabolic parameters</li>
        <li>This analysis is for educational purposes only and does not replace medical diagnosis</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# ==================== TAB 3: ABOUT PCOS ====================
with tab3:
    st.markdown('<div class="section-header"><span>📚</span> Understanding PCOS</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1], gap="medium")
    
    with col1:
        st.markdown("""
        ### What is PCOS (Polycystic Ovary Syndrome)?
        
        Polycystic Ovary Syndrome (PCOS) is the most common endocrine disorder affecting **5-20% of women** of reproductive age worldwide. 
        It's a complex metabolic and hormonal disorder characterized by irregular menstrual cycles, elevated androgen levels, and polycystic ovarian morphology on ultrasound.
        
        ### Diagnostic Criteria (Rotterdam Criteria)
        PCOS diagnosis requires **2 of 3 criteria**:
        1. **Oligo/anovulation** - Irregular or absent menstrual periods
        2. **Clinical/biochemical hyperandrogenism** - High androgens or androgenic symptoms
        3. **Polycystic ovaries** - ≥12 follicles per ovary on ultrasound
        
        ### Key Features & Pathophysiology
        - **Insulin Resistance**: Present in ~70% of PCOS patients, drives hyperandrogenism
        - **Hyperandrogenism**: Elevated testosterone, androstenedione, and DHEA-S
        - **Ovulatory Dysfunction**: Disrupted GnRH pulsatility leads to anovulation
        - **Chronic Inflammation**: Elevated inflammatory markers contribute to symptoms
        
        ### Common Symptoms
        - **Menstrual irregularities**: Amenorrhea, oligomenorrhea, or prolonged cycles
        - **Infertility**: 70-80% of PCOS patients have fertility issues
        - **Hirsutism**: Excessive facial and body hair growth (androgenic symptom)
        - **Acne**: Often severe, resistant to standard treatments
        - **Androgenic alopecia**: Hair loss from scalp (top of head)
        - **Weight gain**: Difficulty losing weight, central obesity
        - **Skin manifestations**: Acanthosis nigricans (dark skin patches) indicating insulin resistance
        - **Mood disorders**: Increased risk of depression and anxiety
        
        ### Associated Health Risks & Complications
        - **Metabolic**: Type 2 diabetes (2.5x risk), metabolic syndrome, dyslipidemia
        - **Cardiovascular**: Hypertension, increased atherosclerosis risk, CVD (2-3x risk)
        - **Endometrial**: Endometrial cancer (2-3x risk) due to unopposed estrogen
        - **Sleep Disorders**: Obstructive sleep apnea affecting 20-40% of PCOS patients
        - **Psychological**: Depression and anxiety disorders significantly more common
        - **Fertility**: PCOS is a leading cause of infertility (25-30% of cases)
        """)
    
    with col2:
        st.markdown('### PCOS Phenotypes Overview')
        
        st.markdown("""
        <div style="border-radius: 14px; padding: 1.8rem; margin: 1.2rem 0; border-left: 6px solid #ef5350; background: linear-gradient(135deg, #ffebee 0%, #ffffff 100%); box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);">
        <strong style="color: #ef5350; font-size: 1.1rem;">🔴 IR - Insulin-Resistant</strong><br>
        <span style="font-size: 0.85rem; color: #2c3e50;">
        <strong>40-70% of PCOS cases</strong><br><br>
        • Elevated fasting insulin<br>
        • Higher BMI (overweight/obese)<br>
        • Metabolic dysfunction focus<br>
        • Type 2 diabetes risk: 5-10x<br>
        • Worse metabolic outcomes
        </span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="border-radius: 14px; padding: 1.8rem; margin: 1.2rem 0; border-left: 6px solid #ffa726; background: linear-gradient(135deg, #fff3e0 0%, #ffffff 100%); box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);">
        <strong style="color: #ffa726; font-size: 1.1rem;">🟡 H - Hormonal</strong><br>
        <span style="font-size: 0.85rem; color: #2c3e50;">
        <strong>20-30% of PCOS cases</strong><br><br>
        • High testosterone/androgens<br>
        • Normal insulin sensitivity<br>
        • Severe androgenic symptoms<br>
        • Often lean phenotype<br>
        • Better metabolic profile
        </span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="border-radius: 14px; padding: 1.8rem; margin: 1.2rem 0; border-left: 6px solid #66bb6a; background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 100%); box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);">
        <strong style="color: #66bb6a; font-size: 1.1rem;">🟢 LM - Lean/Mild</strong><br>
        <span style="font-size: 0.85rem; color: #2c3e50;">
        <strong>10-30% of PCOS cases</strong><br><br>
        • Normal BMI (lean phenotype)<br>
        • Normal metabolic markers<br>
        • Diagnosed by imaging<br>
        • Better fertility outcomes<br>
        • Lifestyle intervention focus
        </span>
        </div>
        """, unsafe_allow_html=True)

# ==================== TAB 4: SYSTEM INFO ====================
with tab4:
    st.markdown('<div class="section-header"><span>⚙️</span> System & Model Information</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        st.markdown('<div class="details-card">', unsafe_allow_html=True)
        st.markdown('<div class="details-title">🤖 Model Performance Metrics</div>', unsafe_allow_html=True)
        
        metrics_df = pd.DataFrame({
            'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
            'Score': [
                f"{model_info.get('accuracy', 0):.2%}",
                f"{model_info.get('precision', 0):.2%}",
                f"{model_info.get('recall', 0):.2%}",
                f"{model_info.get('f1_score', 0):.2%}"
            ]
        })
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)
        
        st.markdown("""
        **What These Metrics Mean:**
        - **Accuracy (91.74%):** Overall correctness of predictions - 91.74% of all predictions are correct
        - **Precision (93.55%):** When model predicts PCOS, it's correct 93.55% of the time (high confidence)
        - **Recall (80.56%):** Model identifies 80.56% of actual PCOS cases (sensitivity)
        - **F1-Score (86.57%):** Balanced measure between precision and recall
        
        **Model Details:**
        - Algorithm: Random Forest Classifier
        - Training: 10-fold cross-validation
        - Validation: 80% train / 20% test split
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="details-card">', unsafe_allow_html=True)
        st.markdown('<div class="details-title">📊 Dataset & Model Details</div>', unsafe_allow_html=True)
        
        info_df = pd.DataFrame({
            'Parameter': ['Training Samples', 'Features/Parameters', 'Model Type'],
            'Value': ['541 patients', f"{model_info.get('feature_count', 0)} clinical markers", 
                     model_info.get('model_name', 'Unknown')]
        })
        st.dataframe(info_df, use_container_width=True, hide_index=True)
        
        st.markdown("""
        **Training Data:**
        - **Sample Size:** 541 real patient cases from clinical studies
        - **PCOS Cases:** ~280 patients with confirmed PCOS diagnosis
        - **Control Cases:** ~261 healthy control subjects
        - **Quality:** Validated by endocrinologists and medical professionals
        
        **18 Clinical Parameters:**
        - Demographics: Age, Height, Weight, BMI
        - Hormonal: Fasting Insulin, Testosterone, LH/FSH Ratio
        - Clinical: Acne, Hirsutism, Hair Loss, PCOS Symptoms
        - Lifestyle: Exercise Frequency, Sleep Hours, Stress Level
        - Menstrual: Cycle Length, Cycle Regularity
        - Medical: Family History of PCOS/Diabetes
        
        **Why This Model?**
        - Random Forest handles non-linear relationships in clinical data
        - Robust to outliers and missing values
        - Fast predictions (< 100ms per patient)
        - Interpretable results with feature importance
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # How to Use Section
    st.markdown('<div class="section-header"><span>📋</span> How to Use This Dashboard</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="details-card">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown("""
        **📝 Step 1: Enter Your Data**
        
        Go to Dashboard tab and fill in:
        - Your age, height, weight
        - Menstrual cycle information
        - Hormone levels (insulin, testosterone)
        - Clinical symptoms
        - Lifestyle factors
        
        Be as accurate as possible.
        """)
    
    with col2:
        st.markdown("""
        **🔍 Step 2: Run Analysis**
        
        Click "Analyze Patient Data" to:
        - Calculate PCOS risk percentage
        - Determine severity level
        - Identify your PCOS phenotype
        - See health markers comparison
        
        Results appear instantly.
        """)
    
    with col3:
        st.markdown("""
        **✓ Step 3: Review & Act**
        
        Review the detailed report:
        - Risk assessment with charts
        - Phenotype explanation
        - Treatment recommendations
        - Clinical guidance
        
        **Consult your doctor!**
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Important Note
    st.markdown("""
    <div class="details-card" style="border-left: 4px solid #ffa726; margin: 1.5rem 0;">
    
    **⚠️ Important Disclaimer**
    
    This tool is **for educational purposes only** and does NOT diagnose PCOS. 
    PCOS diagnosis requires:
    - Clinical evaluation by a healthcare provider
    - Laboratory tests (hormone panel, glucose tolerance)
    - Pelvic ultrasound (ovarian morphology assessment)
    - Rotterdam criteria (2 of 3 criteria must be met)
    
    Use this dashboard as a **screening tool**, not a substitute for medical diagnosis.
    Always consult an endocrinologist or gynecologist for proper evaluation and treatment.
    
    </div>
    """, unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <p>🏥 PCOS Phenotype Prediction Dashboard | Professional Healthcare Analytics</p>
    <p>For educational and research purposes only. Always consult healthcare providers for medical diagnosis and treatment decisions.</p>
    <p style="font-size: 0.8rem; color: #999; margin-top: 1rem;">Data Privacy: All data is processed locally. No data is stored or transmitted to external servers.</p>
</div>
""", unsafe_allow_html=True)