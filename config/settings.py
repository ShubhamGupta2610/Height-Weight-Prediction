"""
Configuration settings for Height-Weight Prediction System
"""

# Model Configuration
MODEL_CONFIG = {
    'test_size': 0.20,
    'random_state': 42,
    'scaler_type': 'StandardScaler'
}

# Streamlit Configuration
STREAMLIT_CONFIG = {
    'page_title': 'Height-Weight Predictor',
    'page_icon': '📊',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Flask Configuration
FLASK_CONFIG = {
    'DEBUG': True,
    'HOST': 'localhost',
    'PORT': 5000,
    'JSON_SORT_KEYS': False
}

# Data Paths
DATA_PATHS = [
    'data/height-weight.csv',
    '../data/height-weight.csv',
    '../../data/height-weight.csv',
    'height-weight.csv'
]

# Slider Ranges
SLIDER_RANGES = {
    'weight': {
        'min': 40,
        'max': 150,
        'default': 70,
        'step': 0.5,
        'unit': 'kg'
    },
    'height': {
        'min': 140,
        'max': 210,
        'default': 170,
        'step': 0.5,
        'unit': 'cm'
    }
}

# Color Scheme
COLORS = {
    'primary_gradient_start': '#667eea',
    'primary_gradient_end': '#764ba2',
    'secondary_gradient_start': '#f093fb',
    'secondary_gradient_end': '#f5576c',
    'success': '#00cc88',
    'error': '#ff4444',
    'warning': '#ffaa00'
}

# Logging Configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        }
    }
}
