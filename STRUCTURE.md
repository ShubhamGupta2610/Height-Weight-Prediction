## PROJECT STRUCTURE GUIDE

### Root Level Files

```
├── README.md              # Main documentation
├── SETUP.md              # Quick setup guide
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker image config
├── docker-compose.yml   # Multi-container setup
├── .gitignore          # Git exclusions
├── run_streamlit.py    # Streamlit launcher
└── run_flask.py        # Flask launcher
```

### `/data` - Dataset Storage

```
data/
└── height-weight.csv    # Place your dataset here
                         # Required columns: Weight, Height
```

### `/notebooks` - Jupyter Experiments

```
notebooks/
└── 3.0-Simple+Linear+Regression.ipynb
    ├── Data loading & exploration
    ├── Model training
    ├── Interactive UI widgets
    └── Performance analysis
```

### `/streamlit_app` - Streamlit Application

```
streamlit_app/
├── app.py              # Main Streamlit app
│   ├── Page config
│   ├── Data loading
│   ├── Tab 1: Height prediction
│   ├── Tab 2: Weight prediction
│   └── Tab 3: Model analysis
└── __init__.py
```

**Features:**

- Real-time predictions
- Interactive sliders
- Data visualization
- Model metrics dashboard
- No additional config needed

### `/flask_app` - Flask Application

```
flask_app/
├── app.py              # Flask server
│   ├── Routes
│   ├── API endpoints
│   └── Model training
├── templates/
│   └── index.html      # Web interface
├── static/             # CSS/JS (optional)
└── __init__.py
```

**API Endpoints:**

- POST `/api/predict-height` - Predict height
- POST `/api/predict-weight` - Predict weight
- GET `/api/metrics` - Model metrics
- GET `/api/dataset-stats` - Data statistics

### `/docs` - Documentation

```
docs/
├── SETUP.md           # Installation steps
├── USAGE.md           # How to use
├── API.md             # API reference
├── DEPLOYMENT.md      # Deployment guide
└── TROUBLESHOOTING.md # Common issues
```

### `/config` - Configuration

```
config/
├── settings.py        # App settings
├── __init__.py
└── logging.conf       # Logging setup
```

**Available Settings:**

- Model parameters
- Slider ranges
- Color schemes
- Logging config

### `/scripts` - Utility Scripts

```
scripts/
├── preprocess_data.py      # Data loading
├── train_model.py          # Model training
├── show_structure.py       # Directory tree
└── validate_setup.py       # Environment check
```

## Workflow

### Development

```
1. Edit source files (streamlit_app/, flask_app/)
2. Test locally (run_streamlit.py or run_flask.py)
3. Update docs in docs/
4. Commit to git
```

### Deployment

```
1. Prepare data in data/
2. Update config in config/
3. Build Docker image
4. Deploy to cloud platform
```

### Data Flow

```
CSV → Load → Validate → Split → Scale → Train
                                        ↓
                                    Models
                                        ↓
                     Web UI ← API ← Endpoints
```

## File Organization Best Practices

✅ **DO:**

- Keep data in `data/` folder
- Keep apps in their own folders
- Use config/ for settings
- Document in docs/

❌ **DON'T:**

- Mix frontend and backend code
- Hardcode configuration values
- Put large files in root
- Commit CSV files (use .gitignore)

## Extending the Project

### Add New Feature

```
1. Create file in appropriate folder
2. Import in main app (app.py)
3. Test thoroughly
4. Document in docs/
5. Update README
```

### Add New Dependency

```
1. Install: pip install package_name
2. Update requirements.txt
3. Test in both apps
4. Commit changes
```

### Customize UI

```
Streamlit: Edit colors in config/settings.py
Flask: Edit templates/index.html styles
```

## Quick Navigation

| Need          | Location                                                   |
| ------------- | ---------------------------------------------------------- |
| Change colors | `config/settings.py`                                       |
| Update UI     | `streamlit_app/app.py` or `flask_app/templates/index.html` |
| Add data      | `data/height-weight.csv`                                   |
| Read docs     | `docs/` folder                                             |
| Update deps   | `requirements.txt`                                         |
| Docker config | `Dockerfile` or `docker-compose.yml`                       |
