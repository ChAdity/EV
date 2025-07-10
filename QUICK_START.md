# ⚡ Quick Start Guide - EV Station Predictor

Get your EV charging station prediction system running in 5 minutes!

## 🚀 Option 1: Instant Local Setup (Recommended)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the application
python app.py

# 3. Open your browser
# Go to: http://localhost:8000
```

**That's it!** Your EV station predictor is now running.

## 🐳 Option 2: Docker (One Command)

```bash
# Quick Docker deployment
./deploy.sh docker
```

The script will:
- ✅ Check requirements
- ✅ Build Docker image
- ✅ Start container
- ✅ Run health checks
- ✅ Provide access URLs

## 🎯 Quick Test

Once running, try this:

1. **Open the dashboard**: `http://localhost:8000`
2. **Click on the map** to set coordinates (try Delhi area)
3. **Choose "Commercial"** preset for quick features
4. **Click "Predict Location Suitability"**
5. **See results** with confidence scores and map markers

## 🧪 Verify Everything Works

```bash
# Run automated tests
python test_api.py
```

This will test all API endpoints and ML models.

## 📱 What You'll See

### 🎨 Beautiful Dashboard
- Modern gradient design
- Interactive maps with Delhi focus
- Real-time prediction forms
- Statistical overview

### 🤖 AI Predictions
- Choose from 3 ML models (XGBoost, CatBoost, Gradient Boosting)
- Get instant suitability predictions
- View confidence scores (0-100%)
- See color-coded map markers

### 📊 Data Analysis
- Feature importance charts
- Model comparison
- Access to 2,083+ Delhi predictions
- Export capabilities

## ⚙️ Configuration (Optional)

Copy `.env.template` to `.env` and customize:

```bash
cp .env.template .env
# Edit .env with your preferences
```

## 🆘 Troubleshooting

### Models Not Found?
Ensure your `evtotal final/models/` directory contains:
- `xgboost_model.pkl`
- `catboost_model.pkl`
- `gradient_boosting_model.pkl`

### Port Already in Use?
Change the port in `app.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Use different port
```

### Dependencies Issues?
```bash
# Upgrade pip first
pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v
```

## 🌟 Key Features to Try

1. **Interactive Map**: Click anywhere to predict
2. **Location Presets**: Try "Commercial" vs "Residential"
3. **Model Comparison**: Test different ML algorithms
4. **Feature Analysis**: View what factors matter most
5. **Batch Data**: Load existing Delhi predictions

## 📖 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for technical overview
- Explore the API at `http://localhost:8000/docs`

## 🎉 Success!

You now have a production-ready EV charging station prediction system!

**Dashboard**: `http://localhost:8000`
**API Docs**: `http://localhost:8000/docs`
**Health Check**: `http://localhost:8000/api/stats`

---

🔋 **Ready to predict optimal EV charging station locations with AI!**