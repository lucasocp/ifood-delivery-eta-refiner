"""
FastAPI Server for Delivery ETA Refiner (Hybrid PySpark + LLM Engine)
"""
import sys
from pathlib import Path

root = str(Path(__file__).resolve().parent)
if root not in sys.path:
    sys.path.insert(0, root)

try:
    from fastapi import FastAPI
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False

from typing import List
from src.compat import BaseModel
from src.models import StructuredLogisticsData, UnstructuredSignal, RefinedETAResult
from src.hybrid_eta_engine import HybridETAEngine

engine = HybridETAEngine()

class ETAPredictionPayload(BaseModel):
    logistics: StructuredLogisticsData
    signals: List[UnstructuredSignal]

if HAS_FASTAPI:
    app = FastAPI(
        title="iFood Delivery ETA Refiner API",
        description="Motor híbrido combinando Data Engineering estruturado com IA generativa em tempo real.",
        version="1.0.0"
    )

    @app.get("/health")
    def health():
        return {"status": "healthy", "service": "ifood-delivery-eta-refiner"}

    @app.post("/api/v1/eta/predict", response_model=None)
    def predict_eta(payload: ETAPredictionPayload):
        result = engine.predict_refined_eta(payload.logistics, payload.signals)
        return result.dict() if hasattr(result, "dict") else result.model_dump()

if __name__ == "__main__":
    print("[Standalone ETA Engine Demo]")
    from src.models import SignalSource
    logistics = StructuredLogisticsData(
        order_id="ORD-DEMO",
        restaurant_id="REST-01",
        distance_km=3.0,
        historical_merchant_prep_minutes=15.0,
        is_peak_hour=False
    )
    res = engine.predict_refined_eta(logistics, [])
    print(f"Ordem: {res.order_id} | ETA Base: {res.baseline_statistical_eta_minutes} min")
