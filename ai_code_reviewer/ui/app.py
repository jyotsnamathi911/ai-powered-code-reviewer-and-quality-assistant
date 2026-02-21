import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import streamlit as st
import pandas as pd
from ai_code_reviewer.core.metrics import MetricsCalculator
from ai_code_reviewer.core.reviewer import CodeReviewer
from ai_code_reviewer.core.apply import apply_docstrings
from ai_code_reviewer.config.config_loader import ConfigLoader
st.set_page_config(page_title='AI Code Reviewer', layout='wide')
st.markdown('\n<style>\n\n@import url(\'https://fonts.googleapis.com/css2?family=Manrope:wght@400;600&display=swap\');\n\n/* Apply background to full Streamlit container */\n[data-testid="stAppViewContainer"] {\n    background: radial-gradient(circle at 20% 30%, #1e3a8a 0%, #0f172a 60%);\n    color: white;\n}\n\n/* Global font */\nhtml, body, [class*="css"] {\n    font-family: \'Manrope\', sans-serif;\n    color: white;\n}\n\n/* Glow background effects */\n[data-testid="stAppViewContainer"]::before {\n    content: "";\n    position: fixed;\n    width: 600px;\n    height: 600px;\n    background: radial-gradient(circle, rgba(0,255,255,0.15), transparent 70%);\n    top: -200px;\n    left: -200px;\n    filter: blur(120px);\n    z-index: -1;\n}\n\n[data-testid="stAppViewContainer"]::after {\n    content: "";\n    position: fixed;\n    width: 600px;\n    height: 600px;\n    background: radial-gradient(circle, rgba(0,255,150,0.15), transparent 70%);\n    bottom: -200px;\n    right: -200px;\n    filter: blur(120px);\n    z-index: -1;\n}\n\n.glass {\n    background: rgba(255,255,255,0.08);\n    backdrop-filter: blur(18px);\n    padding: 25px;\n    border-radius: 20px;\n    margin-top: 20px;\n    border: 1px solid rgba(255,255,255,0.1);\n}\n\n.stButton>button {\n    border-radius: 12px;\n    background: linear-gradient(90deg, #00f5a0, #00d9f5);\n    color: black;\n    border: none;\n    font-weight: 600;\n    padding: 0.5rem 1.2rem;\n}\n\n</style>\n', unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center;'>⚡ AI Code Reviewer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; opacity:0.7;'>Advanced Static Analysis & Quality Gate Engine</p>", unsafe_allow_html=True)
config = ConfigLoader().load()
exclude = config.get('exclude', [])
style = config.get('style', 'google')
coverage_threshold = config.get('coverage_threshold', 0)
path = st.text_input('Project Path', '.')
use_ai = st.toggle('🤖 Enable AI Semantic Review', value=False)
if 'coverage_result' not in st.session_state:
    st.session_state.coverage_result = None
if 'review_issues' not in st.session_state:
    st.session_state.review_issues = None
c1, c2, c3 = st.columns(3)
with c1:
    if st.button('📊 Scan Coverage'):
        metrics = MetricsCalculator(path, exclude=exclude)
        st.session_state.coverage_result = metrics.calculate()
with c2:
    if st.button('🔍 Run Review'):
        reviewer = CodeReviewer(path, exclude=exclude, use_ai=use_ai)
        st.session_state.review_issues = reviewer.review()
with c3:
    if st.button('✨ Apply Docstrings'):
        apply_docstrings(path, style=style)
        st.success('Docstrings Applied Successfully')
if st.session_state.coverage_result:
    result = st.session_state.coverage_result
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader('📈 Coverage & Maintainability')
    colA, colB, colC = st.columns(3)
    colA.metric('Coverage %', result['coverage_percent'])
    colB.metric('Avg Complexity', result['avg_complexity'])
    colC.metric('Maintainability Index', result['maintainability_index'])
    if result['coverage_percent'] < coverage_threshold:
        st.error('Quality Gate Failed')
    else:
        st.success('Quality Gate Passed')
    st.markdown('</div>', unsafe_allow_html=True)
if st.session_state.review_issues is not None:
    issues = st.session_state.review_issues
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader('🔎 Code Review Findings')
    if not issues:
        st.success('No issues found 🎉')
    else:
        severity_filter = st.selectbox('Filter by Severity', ['All', 'critical', 'warning', 'info'])
        filtered = issues if severity_filter == 'All' else [i for i in issues if i['severity'] == severity_filter]
        st.write(f'Showing {len(filtered)} issues')
        df = pd.DataFrame(filtered)
        st.dataframe(df, use_container_width=True)
        if st.button('Export Issues as CSV'):
            df.to_csv('reports/issues_report.csv', index=False)
            st.success('Exported to reports/issues_report.csv')
    st.markdown('</div>', unsafe_allow_html=True)