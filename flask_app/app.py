"""
Flask app for Height-Weight Linear Regression Prediction
Main Flask application with API endpoints
"""

import os
import sys
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib
matplotlib.use('Agg')   # Non-GUI backend for Flask
import matplotlib.pyplot as plt
import io
import base64
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Load and train model once on startup
def load_and_train_model():
    """Load data and train the model"""
    # Look for data in multiple locations
    data_paths = [
        os.path.join(os.path.dirname(__file__), '..', 'data', 'height-weight.csv'),
        os.path.join(os.path.dirname(__file__), 'height-weight.csv'),
        'height-weight.csv'
    ]
    
    df = None
    for path in data_paths:
        try:
            df = pd.read_csv(path)
            print(f"✓ Dataset loaded from: {path}")
            break
        except FileNotFoundError:
            continue
    
    if df is None:
        print("❌ Error: 'height-weight.csv' not found")
        return None
    
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
    
    # Train reverse regressor
    reverse_regressor = LinearRegression()
    reverse_regressor.fit(y_train.values.reshape(-1, 1), X_train_scaled)
    
    # Calculate metrics
    y_pred_test = regressor.predict(X_test_scaled)
    mse = mean_squared_error(y_test, y_pred_test)
    mae = mean_absolute_error(y_test, y_pred_test)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred_test)
    
    return {
        'df': df,
        'regressor': regressor,
        'reverse_regressor': reverse_regressor,
        'scaler': scaler,
        'X_test': X_test_scaled,
        'y_test': y_test,
        'X_test_original': X_test.values.flatten(),
        'metrics': {
            'mse': mse,
            'mae': mae,
            'rmse': rmse,
            'r2': r2
        }
    }

# Load model
model_data = load_and_train_model()

def generate_plot_base64(fig):
    """Convert matplotlib figure to base64 string"""
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png', bbox_inches='tight')
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.read()).decode()
    plt.close(fig)
    return f"data:image/png;base64,{img_base64}"

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html', model_loaded=(model_data is not None))

@app.route('/api/predict-height', methods=['POST'])
def predict_height():
    """API endpoint to predict height from weight"""
    try:
        data = request.json
        weight = float(data.get('weight', 70))
        
        # Validate input
        if weight < 40 or weight > 150:
            return jsonify({'error': 'Weight must be between 40 and 150 kg'}), 400
        
        # Make prediction
        weight_scaled = model_data['scaler'].transform([[weight]])
        predicted_height = model_data['regressor'].predict(weight_scaled)[0]
        
        # Generate plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(model_data['X_test'], model_data['y_test'], alpha=0.5, label='Test Data', s=50)
        ax.plot(model_data['X_test'], model_data['regressor'].predict(model_data['X_test']), 
                'r-', linewidth=2, label='Regression Line')
        ax.scatter([weight_scaled[0][0]], [predicted_height], color='green', s=200, 
                   marker='*', label='Your Prediction', zorder=5)
        ax.set_xlabel('Weight (scaled)', fontweight='bold')
        ax.set_ylabel('Height (cm)', fontweight='bold')
        ax.set_title('Height vs Weight Prediction')
        ax.legend()
        ax.grid(alpha=0.3)
        
        plot_url = generate_plot_base64(fig)
        
        return jsonify({
            'weight': weight,
            'predicted_height': round(predicted_height, 2),
            'plot': plot_url,
            'slope': round(model_data['regressor'].coef_[0], 4),
            'intercept': round(model_data['regressor'].intercept_, 2)
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict-weight', methods=['POST'])
def predict_weight():
    """API endpoint to predict weight from height"""
    try:
        data = request.json
        height = float(data.get('height', 170))

        # Validate input
        if height < 140 or height > 210:
            return jsonify({
                'error': 'Height must be between 140 and 210 cm'
            }), 400

        # Predict scaled weight
        weight_scaled_pred = model_data['reverse_regressor'].predict(
            np.array([[height]])
        )

        # Convert scaled value back to actual weight
        predicted_weight = model_data['scaler'].inverse_transform(
            weight_scaled_pred.reshape(-1, 1)
        )[0][0]

        # Generate plot
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.scatter(
            model_data['y_test'],
            model_data['X_test'],
            alpha=0.5,
            label='Test Data',
            s=50
        )

        heights_range = np.linspace(
            model_data['y_test'].min(),
            model_data['y_test'].max(),
            100
        )

        weights_pred = model_data['reverse_regressor'].predict(
            heights_range.reshape(-1, 1)
        )

        ax.plot(
            heights_range,
            weights_pred,
            'r-',
            linewidth=2,
            label='Regression Line'
        )

        ax.scatter(
            [height],
            [weight_scaled_pred[0][0]],
            color='orange',
            s=200,
            marker='*',
            label='Your Prediction',
            zorder=5
        )

        ax.set_xlabel('Height (cm)', fontweight='bold')
        ax.set_ylabel('Weight (scaled)', fontweight='bold')
        ax.set_title('Weight vs Height Prediction')
        ax.legend()
        ax.grid(alpha=0.3)

        plot_url = generate_plot_base64(fig)

        return jsonify({
            'height': height,
            'predicted_weight': round(float(predicted_weight), 2),
            'plot': plot_url,
            'slope': round(float(model_data['reverse_regressor'].coef_[0][0]), 4),
            'intercept': round(float(model_data['reverse_regressor'].intercept_[0]), 4)
        })

    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """API endpoint to get model metrics"""
    if model_data is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    return jsonify({
        'mse': round(model_data['metrics']['mse'], 4),
        'mae': round(model_data['metrics']['mae'], 4),
        'rmse': round(model_data['metrics']['rmse'], 4),
        'r2': round(model_data['metrics']['r2'], 4),
        'dataset_size': len(model_data['df']),
        'train_size': int(len(model_data['df']) * 0.8),
        'test_size': len(model_data['X_test'])
    })

@app.route('/api/dataset-stats', methods=['GET'])
def get_dataset_stats():
    """API endpoint to get dataset statistics"""
    if model_data is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    stats = model_data['df'].describe().to_dict()
    
    return jsonify({
        'weight_stats': stats['Weight'],
        'height_stats': stats['Height']
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    if model_data is None:
        print("❌ ERROR: Could not load model data. Ensure 'height-weight.csv' is in the data/ directory.")
    else:
        print("✅ Model loaded successfully")
        print(f"   Dataset size: {len(model_data['df'])} records")
        print(f"   Model R² Score: {model_data['metrics']['r2']:.4f}")
        print("\nStarting Flask server...")
        print("Open http://localhost:5000 in your browser")
    
    app.run(debug=True, port=5000)
