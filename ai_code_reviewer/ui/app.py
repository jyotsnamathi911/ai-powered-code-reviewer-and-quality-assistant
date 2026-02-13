import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import streamlit as st
from ai_code_reviewer.core.metrics import MetricsCalculator
from ai_code_reviewer.core.apply import apply_docstrings
from ai_code_reviewer.config.config_loader import ConfigLoader
st.set_page_config(page_title='AI Code Reviewer', layout='wide')
st.title('🚀 AI Powered Code Reviewer')
st.markdown('Automated docstring generation & quality enforcement')
config = ConfigLoader().load()
exclude = config.get('exclude', [])
style = config.get('style', 'google')
coverage_threshold = config.get('coverage_threshold', 0)
path = st.text_input('Enter file or folder path:', '.')
col1, col2 = st.columns(2)
with col1:
    if st.button('📊 Scan Project'):
        metrics = MetricsCalculator(path, exclude=exclude)
        result = metrics.calculate()
        st.subheader('📈 Coverage Overview')
        coverage = result['coverage_percent']
        st.progress(min(int(coverage), 100))
        m1, m2, m3 = st.columns(3)
        m1.metric('Files Scanned', result['files_scanned'])
        m2.metric('Total Functions', result['total_functions'])
        m3.metric('Total Classes', result['total_classes'])
        st.metric('Coverage %', coverage)
        if coverage < coverage_threshold:
            st.error(f'❌ Coverage below threshold ({coverage_threshold}%)')
        else:
            st.success('✅ Coverage meets threshold')
with col2:
    if st.button('✨ Apply Docstrings'):
        apply_docstrings(path, style=style)
        st.success('Docstrings applied successfully!')
st.markdown('---')
st.caption('AI Code Reviewer — Production Demo UI')