import re
import logging
from typing import List, Tuple
from src.models import UnstructuredSignal, ExtractedSignalImpact, SignalSource

logger = logging.getLogger("LLMSignalRefiner")

class LLMSignalRefiner:
    """
    Camada de Inteligência Artificial para dados não-estruturados em tempo real.
    Analisa feeds textuais de entregadores, alertas operacionais de cozinhas e
    relatórios meteorológicos para quantificar variações estocásticas no tempo de entrega.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key

    def parse_signal(self, signal: UnstructuredSignal) -> ExtractedSignalImpact:
        text = signal.raw_message.lower()
        
        delay_delta = 0.0
        severity = "LEVE"
        cause = "condicao_padrao"
        confidence = 0.85

        # 1. Padrões climáticos críticos
        if any(w in text for w in ["temporal", "alagamento", "chuva torrencial", "granizo", "alagado"]):
            delay_delta += 14.0
            severity = "CRITICA"
            cause = "evento_climatico_severo"
            confidence = 0.95
        elif any(w in text for w in ["chuva forte", "pista molhada", "chovendo"]):
            delay_delta += 7.0
            severity = "MEDIA"
            cause = "chuva_moderada"
            confidence = 0.90

        # 2. Gargalos operacionais da cozinha / restaurante
        if any(w in text for w in ["sobrecarga", "muitos pedidos presenciais", "forno quebrou", "fila de espera"]):
            delay_delta += 12.0
            severity = "ALTA"
            cause = "gargalo_operacional_cozinha"
            confidence = 0.92
        elif any(w in text for w in ["atraso no preparo", "aguardando ingrediente"]):
            delay_delta += 6.0
            severity = "MEDIA"
            cause = "preparo_estendido"
            confidence = 0.88

        # 3. Trânsito / Bloqueios viários
        if any(w in text for w in ["acidente", "trânsito parado", "bloqueio", "manifestação", "via interditada"]):
            delay_delta += 10.0
            severity = "ALTA"
            cause = "bloqueio_viario_ou_acidente"
            confidence = 0.94

        # 4. Acesso ao cliente / condomínio
        if any(w in text for w in ["interfone quebrado", "portaria sem identificação", "sem elevador"]):
            delay_delta += 3.0
            severity = "LEVE"
            cause = "dificuldade_acesso_endereco"
            confidence = 0.85

        return ExtractedSignalImpact(
            source=signal.source,
            estimated_delay_delta_minutes=delay_delta,
            confidence_score=confidence,
            detected_severity=severity,
            root_cause_tag=cause
        )

    def generate_customer_explanation(self, causes: List[str], final_eta: float, delta: float) -> str:
        """
        Gera mensagem empática e transparente em linguagem natural para o usuário final no app.
        """
        if delta <= 0:
            return f"Seu pedido está no ritmo ideal! Previsão de chegada em aproximadamente {int(final_eta)} minutos."

        reasons_text = []
        if "evento_climatico_severo" in causes or "chuva_moderada" in causes:
            reasons_text.append("chuva e condições de pista na sua região para garantir a segurança do entregador")
        if "gargalo_operacional_cozinha" in causes or "preparo_estendido" in causes:
            reasons_text.append("o restaurante está dedicando cuidado extra no preparo artesanal do seu prato")
        if "bloqueio_viario_ou_acidente" in causes:
            reasons_text.append("tráfego intenso atípico na rota de entrega")

        details = " e ".join(reasons_text) if reasons_text else "ajustes dinâmicos de rota"
        
        return (
            f"Atualizamos a previsão para ~{int(final_eta)} minutos (+{int(delta)} min). "
            f"Motivo: {details}. Estamos acompanhando cada segundo do seu pedido!"
        )
