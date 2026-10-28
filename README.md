# ⏱️ iFood Delivery ETA Refiner (Hybrid PySpark & Real-Time LLM Engine)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![PySpark & Databricks](https://img.shields.io/badge/Data%20Engine-PySpark%20%2F%20Databricks-red.svg)](https://spark.apache.org/)
[![LLM Multi-Signal](https://img.shields.io/badge/AI%20Layer-Contextual%20LLM%20Signals-blueviolet.svg)](https://arxiv.org/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Arquitetura híbrida que funde telemetria logística de larga escala (Databricks / PySpark) com Inteligência Artificial para processamento de sinais não-estruturados em tempo real, refinando a previsão de chegada de pedidos (ETA) e comunicando de forma transparente com os clientes.**

---

## 🎯 Desafio de Negócio & Oportunidade iFood

Modelos estatísticos tradicionais de ETA falham em prever anomalias pontuais: temporais repentinos, vias alagadas, sobrecarga imprevista na chapa do restaurante ou interfones quebrados.
- **Antes (Apenas Estatística):** O app informava previsão de 30 minutos; o cliente esperava 60 minutos sem explicação, gerando ansiedade, chamados no suporte e cancelamento do pedido.
- **Agora (Engenharia de Dados + AI Híbrida):** O pipeline em PySpark gera o baseline ótimo e a camada de IA ingere e quantifica notas de texto de entregadores, relatórios meteorológicos e avisos de cozinha, calculando o $\Delta$ exato de atraso e gerando uma justificativa empática e transparente em linguagem natural para o consumidor.

---

## 🏗️ Arquitetura Híbrida de Dados e IA

```mermaid
flowchart TD
    subgraph DataEngineering ["1. Camada de Engenharia de Dados (Batch/Near-Real-Time)"]
        A[Telemetria Histórica de Restaurantes] --> C[Feature Store / Databricks]
        B[Distância Geodésica & Tráfego] --> C
        C --> D[PySpark Pipeline: Cálculo de Baseline ETA]
    end

    subgraph LLMLayer ["2. Camada de IA & Sinais Não-Estruturados"]
        E[Chat / Notas de Voz de Entregadores] --> H[LLMSignalRefiner]
        F[Alertas de Sobrecarga de Cozinha] --> H
        G[Relatórios Climáticos da Defesa Civil] --> H
        H -->|Extração de Deltas & Severidade| I[Variação Estocástica de Tempo (Delta Minutos)]
    end

    subgraph HybridFusion ["3. Motor de Fusão & Comunicação"]
        D --> J[HybridETAEngine]
        I --> J
        J --> K[Previsão Final de ETA Refinada]
        J --> L[Mensagem Empática Gerada para o App iFood]
    end
```

---

## 📁 Estrutura do Repositório

```text
├── app.py                     # API FastAPI com rotas REST e documentação interativa
├── requirements.txt           # Dependências
├── Dockerfile                 # Conteinerização pronta para produção
├── docker-compose.yml         # Orquestrador local
├── src/
│   ├── compat.py              # Camada de interoperabilidade Pydantic v2 / Dataclasses
│   ├── models.py              # Contratos de telemetria estruturada e sinais textuais
│   ├── pyspark_pipeline.py    # Pipeline analítico de baseline logístico (PySpark/Databricks)
│   ├── llm_signal_refiner.py  # Agente de extração de severidade e geração de linguagem natural
│   └── hybrid_eta_engine.py   # Motor de unificação e orquestração do cálculo
└── tests/
    └── test_eta_refiner.py    # Suíte completa de testes unitários
```

---

## ⚡ Como Executar

### 1. Suíte de Testes Unitários
```bash
python -u tests/test_eta_refiner.py
```
> Resultado: **3 testes unitários cobrindo PySpark baseline, parsing do LLM e fusão de dados.**

### 2. Demonstração Interativa via Linha de Comando
```bash
python -u src/hybrid_eta_engine.py
```

### 3. Execução em Servidor FastAPI / Docker
```bash
docker-compose up --build
```
Acesse `http://localhost:8003/docs` para testar os endpoints via Swagger.

---

## 💡 Exemplo de Saída do Sistema

* **Entrada Estruturada:** Pedido em horário de pico, 4.8 km de distância, tempo médio de cozinha de 18 min $\rightarrow$ **Baseline = 41.0 min**.
* **Sinais em Tempo Real:** 
  * Entregador: *"Chuva torrencial na avenida, pista alagada próximo ao cruzamento."*
  * Restaurante: *"Cozinha com sobrecarga temporária devido ao fluxo de salão."*
* **Ajuste da IA:** $+26.0\text{ minutos}$ de impacto cumulativo.
* **ETA Final:** **67 minutos**.
* **Mensagem Exibida ao Cliente no App iFood:**
  > *"Atualizamos a previsão para ~67 minutos (+26 min). Motivo: chuva e condições de pista na sua região para garantir a segurança do entregador e o restaurante está dedicando cuidado extra no preparo artesanal do seu prato. Estamos acompanhando cada segundo do seu pedido!"*

---

## 👨‍💻 Autor

**Lucas Oliveira Costa Pinto**  
- **LinkedIn:** [linkedin.com/in/lucas-oliveira-costa-pinto](https://www.linkedin.com/in/lucas-oliveira-costa-pinto/)  
- **GitHub:** [github.com/lucasocp](https://github.com/lucasocp)  
- **Curso:** Engenharia de Software – UCSal (Formação prevista: Dez/2028)
