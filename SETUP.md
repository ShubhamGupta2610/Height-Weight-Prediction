## SETUP INSTRUCTIONS

### Step 1: Dataset Placement

1. Obtain your `height-weight.csv` file
2. Place it in the `data/` folder
3. Ensure it has columns: `Weight` (kg) and `Height` (cm)

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Choose Your App

#### Option A: Streamlit (Easiest)

```bash
python run_streamlit.py
# Visit http://localhost:8501
```

#### Option B: Flask

```bash
python run_flask.py
# Visit http://localhost:5000
```

#### Option C: Jupyter Notebook

```bash
jupyter notebook
# Open: notebooks/3.0-Simple+Linear+Regression.ipynb
```

### Step 4: Using the App

- Adjust sliders to input weight/height
- View predictions in real-time
- Check Model Analysis tab for statistics

## STRUCTURE OVERVIEW

```
height-weight-predictor/
├── data/                 # ← Place CSV file here
├── notebooks/            # Jupyter experiments
├── streamlit_app/        # Streamlit frontend
├── flask_app/            # Flask backend
│   ├── app.py           # Server
│   └── templates/       # HTML
├── docs/                # Documentation
├── config/              # Settings
├── scripts/             # Utilities
├── requirements.txt     # Dependencies
└── README.md           # Main docs
```

## QUICK REFERENCE

| Command                            | Purpose              |
| ---------------------------------- | -------------------- |
| `python run_streamlit.py`          | Launch Streamlit app |
| `python run_flask.py`              | Launch Flask app     |
| `jupyter notebook`                 | Open Jupyter         |
| `python -m scripts.show_structure` | View project tree    |
| `docker-compose up streamlit`      | Docker Streamlit     |

## TROUBLESHOOTING

**Q: "height-weight.csv not found"**

- A: Place the file in `data/` folder

**Q: "Module not found"**

- A: Run `pip install -r requirements.txt`

**Q: "Port already in use"**

- A: Change port in launcher script or stop other apps

For more help, see detailed guides in `docs/` folder.
