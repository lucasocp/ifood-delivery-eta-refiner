from enum import Enum
from typing import List, Optional, Dict, Any
from src.compat import BaseModel, Field

class SignalSource(str, Enum):
    DRIVER_NOTE = "nota_do_entregador"
    RESTAURANT_ALERT = "alerta_do_restaurante"
    WEATHER_REPORT = "relatorio_climatico"
    CUSTOMER_LOCATION_NOTE = "instrucao_local_cliente"

class StructuredLogisticsData(BaseModel):
    order_id: str
    restaurant_id: str
    distance_km: float
    historical_merchant_prep_minutes: float
    standard_speed_kmh: float = 22.0
    hour_of_day: int = 19
    is_peak_hour: bool = True

class UnstructuredSignal(BaseModel):
    source: SignalSource
    raw_message: str
    timestamp: str

class ExtractedSignalImpact(BaseModel):
    source: SignalSource
    estimated_delay_delta_minutes: float
    confidence_score: float
    detected_severity: str = "MEDIA" # LEVE, MEDIA, ALTA, CRITICA
    root_cause_tag: str

class RefinedETAResult(BaseModel):
    order_id: str
    baseline_statistical_eta_minutes: float
    llm_signal_delay_delta_minutes: float
    final_refined_eta_minutes: float
    confidence: float
    unstructured_signals_analyzed: int
    customer_facing_explanation: str
    internal_ops_telemetry: Dict[str, Any] = Field(default_factory=dict)
