"""
Data preprocessing utilities
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def load_data(filepath):
    """Load CSV data"""
    try:
        df = pd.read_csv(filepath)
        print(f"✓ Data loaded: {len(df)} records")
        return df
    except FileNotFoundError:
        print(f"✗ File not found: {filepath}")
        return None
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        return None

def validate_data(df):
    """Validate dataset structure"""
    required_cols = ['Weight', 'Height']
    
    if not all(col in df.columns for col in required_cols):
        print(f"✗ Missing required columns: {required_cols}")
        return False
    
    if df.isnull().any().any():
        print("⚠ Warning: Dataset contains null values")
        df = df.dropna()
    
    return True

def preprocess_data(df, test_size=0.20, random_state=42):
    """Preprocess data for modeling"""
    X = df[['Weight']]
    y = df['Height']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    # Scale data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"✓ Data preprocessed:")
    print(f"  Train: {len(X_train)} | Test: {len(X_test)}")
    print(f"  Scaled: {X_train_scaled.shape}")
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler
