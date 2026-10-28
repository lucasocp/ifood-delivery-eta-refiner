"""
Camada de Engenharia de Dados: Baseline Logístico Estruturado (PySpark / Databricks)
Calcula a estimativa base (ETA) a partir de telemetria histórica de restaurantes,
distâncias geodésicas e modelos de velocidade média por faixa horária.
"""
import logging
from typing import Dict, Any
from src.models import StructuredLogisticsData

logger = logging.getLogger("PySparkLogisticsPipeline")

class StructuredETAPipeline:
    """
    Simula e implementa os cálculos de feature store do Databricks / PySpark
    para previsão estocástica do ETA base.
    """
    def __init__(self):
        # Multiplicadores de tráfego por faixa horária (típicos de capitais como SP e Salvador)
        self.traffic_multipliers = {
            "peak": 1.45,   # Almoço (12-14h) e Jantar (18-21h)
            "off_peak": 1.05 # Horários de vale
        }

    def compute_baseline_eta(self, data: StructuredLogisticsData) -> float:
        """
        Calcula o ETA determinístico baseado nas features estruturadas:
        ETA = Tempo de Preparo + (Distância / Velocidade Média * 60 * Fator Tráfego) + Buffer de Handover
        """
        prep_time = data.historical_merchant_prep_minutes
        
        # Determina o fator de tráfego
        traffic_factor = self.traffic_multipliers["peak"] if data.is_peak_hour else self.traffic_multipliers["off_peak"]
        
        transit_time_hours = data.distance_km / max(data.standard_speed_kmh, 10.0)
        transit_time_minutes = transit_time_hours * 60.0 * traffic_factor
        
        # Buffer de entrega (estacionar bike/moto, elevador, portaria)
        handover_buffer = 4.0

        baseline_eta = prep_time + transit_time_minutes + handover_buffer
        baseline_eta = round(baseline_eta, 1)

        logger.info(
            f"PySpark Feature Pipeline calculado para Ordem {data.order_id}: "
            f"Preparo={prep_time}m, Trânsito={transit_time_minutes:.1f}m -> Baseline ETA={baseline_eta}m"
        )
        return baseline_eta
