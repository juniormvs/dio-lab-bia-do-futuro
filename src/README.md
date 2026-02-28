# Código da Aplicação

Esta pasta contém o código do seu agente financeiro.

# Passo a passo de execução
```bash
# 1. Configurar o ambiente virtual de desenvolvimento .venv -> $ python3 -m venv .venv
# 2. Habilitar o ambiente virtual -> $ source .venv/bin/activate
# 3. Criar o arquito requirements.txt
# 4. Instalar o requirements.txt $ pip install -r requirements.txt

```
Utilizar o modelo disponível pelo groq [openai/gtp-oss-120b](https://console.groq.com/docs/model/openai/gpt-oss-120b)

## Estrutura Sugerida

```
📁 lab-agente-financeiro/
│
├── 📄 README.md
│
├── 📁 data/                          # Dados mockados para o agente
│   ├── historico_atendimento.csv     # Histórico de atendimentos (CSV)
│   ├── perfil_investidor.json        # Perfil do cliente (JSON)
│   ├── produtos_financeiros.json     # Produtos disponíveis (JSON)
│   └── transacoes.csv                # Histórico de transações (CSV)
│   └── metricas.csv                      # ← NOVO — gerado automaticamente
│
├── 📁 docs/                          # Documentação do projeto
│   ├── 01-documentacao-agente.md     # Caso de uso e arquitetura
│   ├── 02-base-conhecimento.md       # Estratégia de dados
│   ├── 03-prompts.md                 # Engenharia de prompts
│   ├── 04-metricas.md                # Avaliação e métricas
│   └── 05-pitch.md                   # Roteiro do pitch
│
├── 📁 pages/                             # ← NOVO — páginas do Streamlit
│   ├── dashboard.py                      # Dashboard de métricas com Plotly
│   ├── comparador.py                      # Dashboard de métricas com Plotly
│
├── 📁 utils/                             # ← NOVO — módulos reutilizáveis
│   ├── charts.py                         # Funções de gráficos do dashboard
│
├── 📁 src/                           # Código da aplicação
│   └── ...                           # (exemplo de estrutura)
│
├── 📁 assets/                        # Imagens e diagramas
│   └── ...
│
└── 📁 examples/                      # Referências e exemplos
    └── README.md
```

## Exemplo de requirements.txt

```
pandas
json
time
dotenv
groq
streamlit
```

## Como Rodar

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar a aplicação
streamlit run src/app.py
```
##  Evidência de Execução
<img width="1920" height="1928" alt="image" src="https://github.com/user-attachments/assets/44a5af66-fc7a-4d7a-92d6-2fb8207f38f4" />

