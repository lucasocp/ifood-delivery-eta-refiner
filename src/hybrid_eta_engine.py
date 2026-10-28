import sys
from pathlib import Path

root = str(Path(__file__).resolve().parent.parent)
if root not in sys.path:
    sys.path.insert(0, root)

import logging
from typing import List
from src.models import (
    StructuredLogisticsData,
    UnstructuredSignal,
    RefinedETAResult,
    ExtractedSignalImpact
)
from src.pyspark_pipeline import StructuredETAPipeline
from src.llm_signal_refiner import LLMSignalRefiner

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("HybridETAEngine")

class HybridETAEngine:
    """
    Motor Híbrido iFood para Refinamento de ETA:
    Combina a robustez de pipelines analíticos de dados estruturados (Databricks/PySpark)
    com a adaptabilidade contextual de LLMs processando sinais em tempo real.
    """
    def __init__(self):
        self.structured_pipeline = StructuredETAPipeline()
        self.llm_refiner = LLMSignalRefiner()

    def predict_refined_eta(
        self,
        logistics_data: StructuredLogisticsData,
        unstructured_signals: List[UnstructuredSignal]
    ) -> RefinedETAResult:
        # 1. Obter o baseline matemático estruturado
        baseline_eta = self.structured_pipeline.compute_baseline_eta(logistics_data)

        # 2. Processar sinais não estruturados com a camada de IA
        total_delta = 0.0
        causes = []
        confidences = []

        for signal in unstructured_signals:
            impact: ExtractedSignalImpact = self.llm_refiner.parse_signal(signal)
            total_delta += impact.estimated_delay_delta_minutes
            if impact.root_cause_tag != "condicao_padrao":
                causes.append(impact.root_cause_tag)
            confidences.append(impact.confidence_score)

        avg_confidence = (sum(confidences) / len(confidences)) if confidences else 0.90
        final_eta = round(baseline_eta + total_delta, 1)

        # 3. Gerar explicação humanizada transparente para o cliente
        explanation = self.llm_refiner.generate_customer_explanation(causes, final_eta, total_delta)

        telemetry = {
            "order_id": logistics_data.order_id,
            "distance_km": logistics_data.distance_km,
            "baseline_minutes": baseline_eta,
            "llm_delta_minutes": total_delta,
            "detected_causes": causes
        }

        logger.info(
            f"ETA Refinado para {logistics_data.order_id}: "
            f"Baseline={baseline_eta}m + LLM Delta={total_delta}m = {final_eta}m"
        )

        return RefinedETAResult(
            order_id=logistics_data.order_id,
            baseline_statistical_eta_minutes=baseline_eta,
            llm_signal_delay_delta_minutes=total_delta,
            final_refined_eta_minutes=final_eta,
            confidence=round(avg_confidence, 2),
            unstructured_signals_analyzed=len(unstructured_signals),
            customer_facing_explanation=explanation,
            internal_ops_telemetry=telemetry
        )

if __name__ == "__main__":
    from src.models import SignalSource

    engine = HybridETAEngine()

    test_logistics = StructuredLogisticsData(
        order_id="ORD-SP-5501",
        restaurant_id="BURGER-KING-CENTRO",
        distance_km=4.8,
        historical_merchant_prep_minutes=18.0,
        is_peak_hour=True
    )

    test_signals = [
        UnstructuredSignal(
            source=SignalSource.DRIVER_NOTE,
            raw_message="Chuva torrencial na avenida, pista alagada próximo ao cruzamento principal.",
            timestamp="19:15"
        ),
        UnstructuredSignal(
            source=SignalSource.RESTAURANT_ALERT,
            raw_message="Cozinha com sobrecarga temporária devido a fluxo de pedidos no salão.",
            timestamp="19:16"
        )
    ]

    result = engine.predict_refined_eta(test_logistics, test_signals)
    print("\n--- RESULTADO DA PREDIÇÃO HÍBRIDA DE ETA ---")
    print(f"Ordem: {result.order_id}")
    print(f"Baseline Estruturado: {result.baseline_statistical_eta_minutes} minutos")
    print(f"Ajuste da IA (LLM Delta): +{result.llm_signal_delay_delta_minutes} minutos")
    print(f"ETA Final Refinado: {result.final_refined_eta_minutes} minutos")
    print(f"Mensagem ao Cliente: {result.customer_facing_explanation}")
