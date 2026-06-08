"""
Streamlit app for Height-Weight Linear Regression Prediction
Main entry point for the Streamlit application
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')   # Non-GUI backend for Flask
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Height-Weight Predictor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #667eea;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .reverse-metric-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Load and prepare data
@st.cache_data
def load_and_train_model():
    """Load data and train the model"""
    # Look for data in multiple locations
    data_paths = [
        'data/height-weight.csv',
        '../data/height-weight.csv',
        '../../data/height-weight.csv',
        'height-weight.csv'
    ]
    
    df = None
    for path in data_paths:
        try:
            df = pd.read_csv(path)
            st.sidebar.success(f"✓ Dataset loaded from: {path}")
            break
        except FileNotFoundError:
            continue
    
    if df is None:
        st.error("❌ Error: 'height-weight.csv' not found in expected locations")
        st.info("Expected locations:\n- data/height-weight.csv\n- height-weight.csv")
        st.stop()
    
    # Prepare data
    X = df[['Weight']]
    y = df['Height']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    
    # Scale the data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train regressor
    regressor = LinearRegression()
    regressor.fit(X_train_scaled, y_train)
    
    # Train reverse regressor (height -> weight)
    reverse_regressor = LinearRegression()
    reverse_regressor.fit(y_train.values.reshape(-1, 1), X_train_scaled)
    
    return {
        'df': df,
        'regressor': regressor,
        'reverse_regressor': reverse_regressor,
        'scaler': scaler,
        'X_test': X_test_scaled,
        'y_test': y_test,
        'X_test_original': X_test.values.flatten()
    }

# Load model
try:
    model_data = load_and_train_model()
except:
    st.error("Failed to load model. Please ensure all dependencies are installed.")
    st.stop()

# Display header
st.markdown("<h1 class='main-header'>📊 Height-Weight Prediction System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Predict height from weight and vice versa using Linear Regression</p>", unsafe_allow_html=True)

# Sidebar info
with st.sidebar:
    st.title("📈 Model Info")
    st.info(f"""
    **Dataset:**
    - Total records: {len(model_data['df'])}
    - Features: Weight (kg)
    - Target: Height (cm)
    
    **Model:**
    - Algorithm: Linear Regression
    - Scaler: StandardScaler
    """)

# Create tabs
tab1, tab2, tab3 = st.tabs(["📈 Predict Height", "⚖️ Predict Weight", "📊 Model Analysis"])

# ==================== TAB 1: Predict Height ====================
with tab1:
    st.header("Predict Height from Weight")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        weight_input = st.slider(
            "Select Weight (kg)",
            min_value=40.0,
            max_value=150.0,
            value=70.0,
            step=0.5,
            key="weight_slider"
        )
        
        # Make prediction
        weight_scaled = model_data['scaler'].transform([[weight_input]])
        predicted_height = model_data['regressor'].predict(weight_scaled)[0]
        
        # Display prediction
        st.markdown(f"""
        <div class='metric-box'>
            <h3>Prediction Result</h3>
            <p style='font-size: 1.2rem; margin: 10px 0;'>
                <strong>Weight:</strong> {weight_input:.1f} kg
            </p>
            <p style='font-size: 1.5rem; margin: 10px 0;'>
                <strong>Predicted Height:</strong> {predicted_height:.2f} cm
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Additional info
        st.info(f"""
        **Model Parameters:**
        - Slope: {model_data['regressor'].coef_[0]:.4f}
        - Intercept: {model_data['regressor'].intercept_:.2f}
        """)
    
    with col2:
        # Plot visualization
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.scatter(model_data['X_test'], model_data['y_test'], alpha=0.5, label='Test Data', s=50)
        ax.plot(model_data['X_test'], model_data['regressor'].predict(model_data['X_test']), 
                'r-', linewidth=2, label='Regression Line')
        
        # Plot current prediction
# Plot current prediction
        ax.scatter(
                [weight_scaled[0][0]],
                [predicted_height],
                color='green',
                s=200,
                marker='*',
                label='Current Prediction',
                zorder=5
        )

        ax.set_xlabel('Weight (scaled)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Height (cm)', fontsize=12, fontweight='bold')
        ax.set_title('Height vs Weight - Regression Model', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(alpha=0.3)
        plt.tight_layout()
        
        st.pyplot(fig)

# ==================== TAB 2: Predict Weight ====================
with tab2:
    st.header("Predict Weight from Height")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        height_input = st.slider(
            "Select Height (cm)",
            min_value=140.0,
            max_value=210.0,
            value=170.0,
            step=0.5,
            key="height_slider"
       )
        
        # Make reverse prediction
        weight_scaled_pred = model_data['reverse_regressor'].predict( np.array([[height_input]]))
        predicted_weight = model_data['scaler'].inverse_transform(weight_scaled_pred.reshape(-1, 1))[0][0]
        
        # Display prediction
        st.markdown(f"""
        <div class='reverse-metric-box'>
            <h3>Prediction Result</h3>
            <p style='font-size: 1.2rem; margin: 10px 0;'>
                <strong>Height:</strong> {height_input:.1f} cm
            </p>
            <p style='font-size: 1.5rem; margin: 10px 0;'>
                <strong>Predicted Weight:</strong> {predicted_weight:.2f} kg
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Additional info
        st.info(f"""
        **Reverse Model Parameters:**
        - Slope: {float(model_data['reverse_regressor'].coef_[0][0]):.4f}
        - Intercept: {float(model_data['reverse_regressor'].intercept_[0]):.4f}
        """)
    
    with col2:
        # Plot visualization
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.scatter(model_data['y_test'], model_data['X_test'], alpha=0.5, label='Test Data', s=50)
        
        heights_range = np.linspace(model_data['y_test'].min(), model_data['y_test'].max(), 100)
        weights_pred = model_data['reverse_regressor'].predict(heights_range.reshape(-1, 1))
        ax.plot(heights_range, weights_pred, 'r-', linewidth=2, label='Regression Line')
        
        ax.scatter([height_input], [weight_scaled_pred[0][0]], color='orange', s=200,
           marker='*', label='Current Prediction', zorder=5)
        
        ax.set_xlabel('Height (cm)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Weight (scaled)', fontsize=12, fontweight='bold')
        ax.set_title('Weight vs Height - Reverse Regression Model', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(alpha=0.3)
        plt.tight_layout()
        
        st.pyplot(fig)

# ==================== TAB 3: Model Analysis ====================
with tab3:
    st.header("Model Analysis & Performance")
    
    # Calculate metrics
    y_pred_test = model_data['regressor'].predict(model_data['X_test'])
    mse = mean_squared_error(model_data['y_test'], y_pred_test)
    mae = mean_absolute_error(model_data['y_test'], y_pred_test)
    rmse = np.sqrt(mse)
    r2 = r2_score(model_data['y_test'], y_pred_test)
    
    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Mean Squared Error (MSE)", f"{mse:.4f}")
    with col2:
        st.metric("Mean Absolute Error (MAE)", f"{mae:.4f}")
    with col3:
        st.metric("Root Mean Squared Error (RMSE)", f"{rmse:.4f}")
    with col4:
        st.metric("R² Score", f"{r2:.4f}")
    
    # Data distribution
    st.subheader("Dataset Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots()
        ax.hist(model_data['df']['Weight'], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
        ax.set_xlabel('Weight (kg)', fontweight='bold')
        ax.set_ylabel('Frequency', fontweight='bold')
        ax.set_title('Distribution of Weight')
        ax.grid(alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots()
        ax.hist(model_data['df']['Height'], bins=30, color='lightcoral', edgecolor='black', alpha=0.7)
        ax.set_xlabel('Height (cm)', fontweight='bold')
        ax.set_ylabel('Frequency', fontweight='bold')
        ax.set_title('Distribution of Height')
        ax.grid(alpha=0.3)
        st.pyplot(fig)
    
    # Residual plot
    st.subheader("Residual Analysis")
    
    residuals = model_data['y_test'] - y_pred_test
    
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.scatter(y_pred_test, residuals, alpha=0.5, s=50)
    ax.axhline(y=0, color='r', linestyle='--', linewidth=2)
    ax.set_xlabel('Predicted Height (cm)', fontweight='bold')
    ax.set_ylabel('Residuals', fontweight='bold')
    ax.set_title('Residual Plot - Should show random pattern around zero')
    ax.grid(alpha=0.3)
    plt.tight_layout()
    
    st.pyplot(fig)
    
    # Dataset info
    st.subheader("Dataset Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Dataset Summary:**")
        st.write(model_data['df'].describe())
    
    with col2:
        st.write("**Dataset Shape:**")
        st.info(f"""
        - Total records: {len(model_data['df'])}
        - Training set: {len(model_data['X_test']) + len(model_data['X_test'])} records (80%)
        - Test set: {len(model_data['X_test'])} records (20%)
        - Features: Weight (independent)
        - Target: Height (dependent)
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🔧 Built with Streamlit | 📊 Linear Regression Model</p>
    <p>Version 1.0 | 2024</p>
</div>
""", unsafe_allow_html=True)
