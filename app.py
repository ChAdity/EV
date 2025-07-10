import os
import pickle
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import folium
import json
from pathlib import Path

# Initialize FastAPI app
app = FastAPI(
    title="EV Charging Station Placement Predictor",
    description="AI-powered system for predicting optimal EV charging station locations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
MODELS_PATH = Path("evtotal final/models")
models = {}

try:
    if MODELS_PATH.exists():
        for model_file in MODELS_PATH.glob("*.pkl"):
            model_name = model_file.stem.replace("_model", "")
            with open(model_file, 'rb') as f:
                models[model_name] = pickle.load(f)
                print(f"Loaded model: {model_name}")
except Exception as e:
    print(f"Error loading models: {e}")

# Load existing predictions
PREDICTIONS_PATH = Path("evtotal final/data")
predictions_data = None

try:
    if (PREDICTIONS_PATH / "delhi_ev_station_predictions.csv").exists():
        predictions_data = pd.read_csv(PREDICTIONS_PATH / "delhi_ev_station_predictions.csv")
        print(f"Loaded predictions data: {len(predictions_data)} records")
except Exception as e:
    print(f"Error loading predictions: {e}")

# Pydantic models
class LocationData(BaseModel):
    latitude: float
    longitude: float
    parking: int = 0
    edges: int = 0
    parking_space: int = 0
    civic: int = 0
    restaurant: int = 0
    park: int = 0
    school: int = 0
    node: int = 0
    community_centre: int = 0
    place_of_worship: int = 0
    university: int = 0
    cinema: int = 0
    library: int = 0
    commercial: int = 0
    retail: int = 0
    townhall: int = 0
    government: int = 0
    residential: int = 0
    population: float = 0

class PredictionRequest(BaseModel):
    locations: List[LocationData]
    model_name: Optional[str] = "xgboost"

class PredictionResponse(BaseModel):
    predictions: List[dict]
    model_used: str
    confidence_scores: List[float]

# Routes
@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main dashboard"""
    return FileResponse("templates/index.html")

@app.get("/api/models")
async def get_available_models():
    """Get list of available ML models"""
    return {
        "models": list(models.keys()),
        "default": "xgboost" if "xgboost" in models else list(models.keys())[0] if models else None
    }

@app.get("/api/stats")
async def get_project_stats():
    """Get project statistics and overview"""
    stats = {
        "total_models": len(models),
        "available_models": list(models.keys()),
        "prediction_records": len(predictions_data) if predictions_data is not None else 0,
        "cities_covered": ["Delhi"],
        "features_used": [
            "parking", "edges", "parking_space", "civic", "restaurant", 
            "park", "school", "node", "community_centre", "place_of_worship",
            "university", "cinema", "library", "commercial", "retail",
            "townhall", "government", "residential", "population"
        ]
    }
    return stats

@app.post("/api/predict", response_model=PredictionResponse)
async def predict_locations(request: PredictionRequest):
    """Predict EV station suitability for given locations"""
    if not models:
        raise HTTPException(status_code=500, detail="No models available")
    
    model_name = request.model_name if request.model_name in models else list(models.keys())[0]
    model = models[model_name]
    
    # Prepare features
    features = []
    for location in request.locations:
        feature_vector = [
            location.parking, location.edges, location.parking_space, location.civic,
            location.restaurant, location.park, location.school, location.node,
            location.community_centre, location.place_of_worship, location.university,
            location.cinema, location.library, location.commercial, location.retail,
            location.townhall, location.government, location.residential, location.population
        ]
        features.append(feature_vector)
    
    try:
        # Make predictions
        X = np.array(features)
        predictions = model.predict(X)
        probabilities = model.predict_proba(X)[:, 1] if hasattr(model, 'predict_proba') else [0.5] * len(X)
        
        # Prepare response
        results = []
        for i, (location, pred, prob) in enumerate(zip(request.locations, predictions, probabilities)):
            results.append({
                "location_id": i,
                "latitude": location.latitude,
                "longitude": location.longitude,
                "prediction": int(pred),
                "confidence": float(prob),
                "recommendation": "Suitable" if pred == 1 else "Not Suitable"
            })
        
        return PredictionResponse(
            predictions=results,
            model_used=model_name,
            confidence_scores=probabilities.tolist()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/api/existing-predictions")
async def get_existing_predictions(limit: int = 100):
    """Get existing predictions for Delhi"""
    if predictions_data is None:
        raise HTTPException(status_code=404, detail="No prediction data available")
    
    # Sample data for performance
    sample_data = predictions_data.head(limit)
    
    # Convert to response format
    results = []
    for _, row in sample_data.iterrows():
        # Extract coordinates from geometry if available
        lat, lon = 28.6139, 77.209  # Default Delhi center
        if 'geometry' in row and pd.notna(row['geometry']):
            # Simple geometry parsing - in production you'd use proper GIS libraries
            geom_str = str(row['geometry'])
            if 'POINT' in geom_str:
                try:
                    coords = geom_str.replace('POINT (', '').replace(')', '').split()
                    lon, lat = float(coords[0]), float(coords[1])
                    # Convert from projected coordinates to lat/lon if needed
                    # This is a simplified conversion - proper GIS transformation needed
                    lat = lat / 100000 + 20  # Rough approximation
                    lon = lon / 100000 + 70  # Rough approximation
                except:
                    pass
        
        results.append({
            "id": int(row.get('Unnamed: 0', 0)),
            "latitude": lat,
            "longitude": lon,
            "prediction": int(row.get('EV_station_prediction', 0)),
            "existing_stations": int(row.get('EV_stations', 0)),
            "population": float(row.get('population', 0)),
            "features": {
                "parking": int(row.get('parking', 0)),
                "restaurant": int(row.get('restaurant', 0)),
                "school": int(row.get('school', 0)),
                "commercial": int(row.get('commercial', 0))
            }
        })
    
    return {
        "total_records": len(predictions_data),
        "returned_records": len(results),
        "predictions": results
    }

@app.get("/api/map")
async def generate_map():
    """Generate interactive map with predictions"""
    if predictions_data is None:
        raise HTTPException(status_code=404, detail="No prediction data available")
    
    # Create folium map centered on Delhi
    m = folium.Map(location=[28.6139, 77.209], zoom_start=10)
    
    # Add predicted locations (sample first 50 for performance)
    sample_predictions = predictions_data[predictions_data['EV_station_prediction'] == 1].head(50)
    
    for _, row in sample_predictions.iterrows():
        # Default coordinates
        lat, lon = 28.6139 + np.random.uniform(-0.5, 0.5), 77.209 + np.random.uniform(-0.5, 0.5)
        
        folium.Marker(
            [lat, lon],
            popup=f"Predicted EV Station<br>Population: {row.get('population', 0):.0f}",
            icon=folium.Icon(color='red', icon='bolt', prefix='fa')
        ).add_to(m)
    
    # Save map
    map_path = "static/current_predictions_map.html"
    os.makedirs("static", exist_ok=True)
    m.save(map_path)
    
    return {"map_url": "/static/current_predictions_map.html"}

@app.get("/api/feature-importance")
async def get_feature_importance():
    """Get feature importance from models"""
    if not models:
        raise HTTPException(status_code=404, detail="No models available")
    
    feature_names = [
        "parking", "edges", "parking_space", "civic", "restaurant", 
        "park", "school", "node", "community_centre", "place_of_worship",
        "university", "cinema", "library", "commercial", "retail",
        "townhall", "government", "residential", "population"
    ]
    
    importance_data = {}
    
    for model_name, model in models.items():
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            importance_data[model_name] = [
                {"feature": name, "importance": float(imp)}
                for name, imp in zip(feature_names, importances)
            ]
            # Sort by importance
            importance_data[model_name].sort(key=lambda x: x['importance'], reverse=True)
    
    return importance_data

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)