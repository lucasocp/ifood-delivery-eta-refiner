import unittest
import sys
from pathlib import Path

root = str(Path(__file__).resolve().parent.parent)
if root not in sys.path:
    sys.path.insert(0, root)

from src.models import StructuredLogisticsData, UnstructuredSignal, SignalSource
from src.pyspark_pipeline import StructuredETAPipeline
from src.llm_signal_refiner import LLMSignalRefiner
from src.hybrid_eta_engine import HybridETAEngine

class TestDeliveryETARefiner(unittest.TestCase):
    def setUp(self):
        self.pyspark_pipeline = StructuredETAPipeline()
        self.llm_refiner = LLMSignalRefiner()
        self.engine = HybridETAEngine()

    def test_structured_baseline_calculation(self):
        # 10 km a 20 km/h = 30 min trânsito * 1.45 (pico) = 43.5 min + 15 min preparo + 4 min buffer = 62.5 min
        data = StructuredLogisticsData(
            order_id="ORD-T1",
            restaurant_id="REST-T1",
            distance_km=10.0,
            historical_merchant_prep_minutes=15.0,
            standard_speed_kmh=20.0,
            is_peak_hour=True
        )
        baseline = self.pyspark_pipeline.compute_baseline_eta(data)
        self.assertAlmostEqual(baseline, 62.5, places=1)

    def test_llm_unstructured_signal_parsing(self):
        signal_storm = UnstructuredSignal(
            source=SignalSource.WEATHER_REPORT,
            raw_message="Alerta: chuva torrencial e granizo com alagamentos.",
            timestamp="18:30"
        )
        impact = self.llm_refiner.parse_signal(signal_storm)
        self.assertEqual(impact.estimated_delay_delta_minutes, 14.0)
        self.assertEqual(impact.detected_severity, "CRITICA")
        self.assertEqual(impact.root_cause_tag, "evento_climatico_severo")

    def test_hybrid_engine_end_to_end(self):
        logistics = StructuredLogisticsData(
            order_id="ORD-END2END",
            restaurant_id="REST-BAHIA",
            distance_km=2.0,
            historical_merchant_prep_minutes=10.0,
            standard_speed_kmh=20.0,
            is_peak_hour=False
        )
        signals = [
            UnstructuredSignal(
                source=SignalSource.RESTAURANT_ALERT,
                raw_message="Aguardando reposição de insumo, sobrecarga na chapa.",
                timestamp="12:00"
            )
        ]
        result = self.engine.predict_refined_eta(logistics, signals)
        self.assertGreater(result.final_refined_eta_minutes, result.baseline_statistical_eta_minutes)
        self.assertIn("cuidado extra no preparo", result.customer_facing_explanation)
        self.assertEqual(result.unstructured_signals_analyzed, 1)

if __name__ == "__main__":
    unittest.main()
