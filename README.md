# 🔋 EV Charging Station Placement Predictor

An AI-powered web application that predicts optimal locations for Electric Vehicle (EV) charging stations using advanced machine learning algorithms and geographic data analysis.

![EV Station Predictor](https://img.shields.io/badge/AI-Powered-blue) ![Python](https://img.shields.io/badge/Python-3.11-green) ![FastAPI](https://img.shields.io/badge/FastAPI-Latest-red) ![ML](https://img.shields.io/badge/ML-XGBoost%20%7C%20CatBoost%20%7C%20LightGBM-orange)

## 🌟 Features

### 🤖 Advanced Machine Learning
- **Multiple ML Models**: XGBoost, CatBoost, and Gradient Boosting for robust predictions
- **Feature Engineering**: 19 geographic and demographic features including parking availability, amenities, population density
- **Real-time Predictions**: Instant suitability assessment for any location
- **Model Comparison**: Compare performance across different algorithms

### 🗺️ Interactive Mapping
- **Live Map Interface**: Interactive Leaflet.js map with real-time marker placement
- **Click-to-Predict**: Click anywhere on the map to get coordinates and predictions
- **Visualization**: Color-coded markers showing suitable vs. unsuitable locations
- **Geographic Data**: Integrated with Delhi city data and existing EV station locations

### 📊 Data Analytics
- **Feature Importance**: Visualize which factors most influence EV station placement
- **Statistical Dashboard**: Real-time project statistics and model performance metrics
- **Prediction History**: View and analyze existing predictions for Delhi region
- **Data Export**: Access prediction data through REST API endpoints

### 🎨 Modern Web Interface
- **Responsive Design**: Beautiful, mobile-friendly interface built with Bootstrap 5
- **Interactive Forms**: Easy-to-use forms with presets for common location types
- **Real-time Updates**: Live prediction results with confidence scores
- **Professional UI**: Gradient backgrounds, smooth animations, and modern styling

## 🏗️ Technical Architecture

### Backend (FastAPI)
```
app.py                 # Main FastAPI application
├── API Endpoints
│   ├── /api/predict   # ML prediction endpoint
│   ├── /api/stats     # Project statistics
│   ├── /api/models    # Available models info
│   └── /api/map       # Map generation
├── Model Loading      # Automatic ML model discovery
└── Data Processing    # CSV and geographic data handling
```

### Frontend (HTML/JavaScript)
```
templates/index.html   # Main dashboard interface
├── Interactive Map    # Leaflet.js integration
├── Prediction Forms   # Dynamic form handling
├── Data Visualization # Chart.js integration
└── Responsive Design  # Bootstrap 5 styling
```

### Machine Learning Pipeline
```
evtotal final/
├── models/           # Trained ML models (.pkl files)
│   ├── xgboost_model.pkl
│   ├── catboost_model.pkl
│   └── gradient_boosting_model.pkl
├── data/            # Training and prediction data
│   ├── delhi_ev_station_predictions.csv
│   ├── all_city_data_with_pop.csv
│   └── *.html (map visualizations)
└── Copy of ev final.ipynb  # Jupyter notebook with training code
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip package manager
- 4GB+ RAM (for ML models)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd ev-charging-station-predictor
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app.py
```

4. **Access the dashboard**
Open your browser and navigate to: `http://localhost:8000`

### Docker Deployment

1. **Build the container**
```bash
docker build -t ev-station-predictor .
```

2. **Run the container**
```bash
docker run -p 8000:8000 ev-station-predictor
```

## 📖 Usage Guide

### 1. Making Predictions

#### Option A: Interactive Map
1. Click anywhere on the Delhi map to set coordinates
2. Select your preferred ML model (XGBoost, CatBoost, or Gradient Boosting)
3. Choose a location type preset (Commercial or Residential) or manually input features
4. Click "Predict Location Suitability"
5. View results with confidence scores and map markers

#### Option B: Manual Input
1. Enter specific latitude/longitude coordinates
2. Input location features:
   - **Parking**: Number of parking facilities
   - **Restaurants**: Number of nearby restaurants
   - **Schools**: Number of educational institutions
   - **Commercial**: Commercial establishment count
   - **Population**: Local population density
   - **Parks**: Number of parks and recreational areas

### 2. Feature Analysis
1. Switch to the "Analysis" tab
2. Click "Show Feature Importance" to see which factors most influence predictions
3. View interactive charts showing model decision factors
4. Load existing Delhi predictions to see patterns

### 3. API Usage

The application provides RESTful API endpoints for programmatic access:

#### Predict Location Suitability
```bash
curl -X POST "http://localhost:8000/api/predict" \
-H "Content-Type: application/json" \
-d '{
  "locations": [{
    "latitude": 28.6139,
    "longitude": 77.209,
    "parking": 5,
    "restaurant": 10,
    "school": 3,
    "commercial": 8,
    "population": 7500,
    "park": 2
  }],
  "model_name": "xgboost"
}'
```

#### Get Project Statistics
```bash
curl "http://localhost:8000/api/stats"
```

#### Get Available Models
```bash
curl "http://localhost:8000/api/models"
```

## 🧠 Machine Learning Models

### Model Performance
The system uses three state-of-the-art gradient boosting algorithms:

1. **XGBoost**: Extreme Gradient Boosting
   - High performance on tabular data
   - Excellent feature importance insights
   - Robust against overfitting

2. **CatBoost**: Categorical Boosting
   - Handles categorical features well
   - Built-in regularization
   - Fast inference

3. **LightGBM**: Light Gradient Boosting Machine
   - Memory efficient
   - Fast training
   - High accuracy

### Features Used
The models consider 19 key features:
- **Infrastructure**: Parking facilities, edges, parking spaces
- **Amenities**: Restaurants, parks, schools, libraries, cinemas
- **Institutional**: Universities, government buildings, town halls
- **Commercial**: Retail, commercial establishments
- **Residential**: Residential density
- **Community**: Community centers, places of worship
- **Demographics**: Population density

## 🚀 Deployment Options

### Local Development
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Production Deployment

#### Docker
```bash
docker run -d -p 8000:8000 --name ev-predictor ev-station-predictor
```

#### Cloud Platforms

**Heroku**
```bash
heroku create your-app-name
git push heroku main
```

**AWS/GCP/Azure**
- Use the provided Dockerfile
- Configure environment variables
- Set up load balancing and auto-scaling

### Environment Variables
```bash
# Optional configuration
export MODEL_PATH="evtotal final/models"
export DATA_PATH="evtotal final/data"
export DEBUG=False
```

## 📊 Project Statistics

- **📈 ML Models**: 3 advanced algorithms
- **🗺️ Predictions**: 2,083+ Delhi locations analyzed
- **🔧 Features**: 19 geographic and demographic factors
- **🏙️ Cities**: Delhi (expandable to other cities)
- **⚡ Performance**: Real-time predictions (<1 second)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenStreetMap** for geographic data
- **Bootstrap 5** for responsive UI components
- **Leaflet.js** for interactive mapping
- **FastAPI** for high-performance web framework
- **scikit-learn ecosystem** for machine learning tools

## 📧 Contact

For questions, suggestions, or collaborations:
- **Email**: [your-email@domain.com]
- **LinkedIn**: [Your LinkedIn Profile]
- **GitHub**: [Your GitHub Profile]

---

**Made with ❤️ for sustainable transportation and smart city planning**