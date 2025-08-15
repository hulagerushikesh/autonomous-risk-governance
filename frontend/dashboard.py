import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Custom styling
st.set_page_config(
    page_title="Risk Governance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown("""
    <style>
    .main {
        padding: 20px;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    .stAlert {
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

def display_metrics(result: dict):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="Risk Score",
            value=f"{result.get('data', {}).get('risk_score', 0):.2f}",
            delta="normal" if result.get('data', {}).get('risk_score', 0) < 0.5 else "elevated"
        )
    with col2:
        st.metric(
            label="Bias Score",
            value=f"{result.get('data', {}).get('bias_score', 0):.2f}"
        )
    with col3:
        st.metric(
            label="Risk Level",
            value=result.get('data', {}).get('risk_level', 0)
        )

def call_fastapi_endpoint(endpoint: str, data: dict = None) -> dict:
    base_url = "http://localhost:8000"
    if data:
        response = requests.post(f"{base_url}/{endpoint}", json=data)
    else:
        response = requests.get(f"{base_url}/{endpoint}")
    return response.json()

def main():
    st.title("🎯 Autonomous Risk Governance Dashboard")
    
    # Dashboard layout with tabs
    tab1, tab2 = st.tabs(["Risk Assessment", "Historical Data"])
    
    with tab1:
        # Sidebar for inputs
        with st.sidebar:
            st.header("Risk Assessment Parameters")
            risk_score = st.slider("Risk Score", 0.0, 1.0, 0.5)
            bias_score = st.slider("Bias Score", 0.0, 1.0, 0.2)
            risk_level = st.selectbox("Risk Level", [0, 1, 2])
            features = st.multiselect(
                "Features", 
                ["income", "credit_score", "age", "employment_status"]
            )

        # Main content area
        if st.button("Evaluate Risk", type="primary"):
            evaluation_data = {
                "risk_score": risk_score,
                "bias_score": bias_score,
                "risk_level": risk_level,
                "features": features,
                "context": {"timestamp": datetime.now().isoformat()}
            }
            
            try:
                result = call_fastapi_endpoint("evaluate", evaluation_data)
                st.success("Evaluation Complete")
                display_metrics(result)
                
                # Detailed results in expander
                with st.expander("View Detailed Results"):
                    st.json(result)
            except Exception as e:
                st.error(f"Error connecting to FastAPI backend: {str(e)}")
    
    with tab2:
        st.subheader("Historical Risk Assessments")
        # Placeholder for historical data visualization
        chart_data = pd.DataFrame({
            'Risk Score': [0.5, 0.6, 0.3, 0.8],
            'Bias Score': [0.2, 0.3, 0.2, 0.4]
        }, index=['Jan', 'Feb', 'Mar', 'Apr'])
        st.line_chart(chart_data)

if __name__ == "__main__":
    main()