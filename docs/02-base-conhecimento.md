# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Utilização no Agente |
|---|---|---|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores e dar respostas mais inteligentes |
| `perfil_investidor.json` | JSON | Personalizar recomendações tanto de tópicos explicativos, dicas, quanto investimentos |
| `produtos_financeiros.json` | JSON | Sugerir produtos adequados ao perfil, de acordo com o perfil avaliado |
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente, tendo assim uma base de comportamento financeiro do usuário |

### Dados Gerados pelo Agente

Além dos dados mockados originais, o projeto gera automaticamente dois arquivos durante o uso:

| Arquivo | Formato | Descrição |
|---|---|---|
| `metricas.csv` | CSV | Gerado a cada interação — registra latência, tokens, velocidade, feedback do usuário e detecção de escopo |
| `metricas_comparador.csv` | CSV | Gerado pelo comparador de modelos — registra métricas separadas por modelo LLM testado |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

O produto **Fundo Imobiliário (FII)** foi acrescentado ao `produtos_financeiros.json`, expandindo o leque de opções disponíveis para recomendação:

```json
{
  "nome": "Fundo Imobiliário (FII)",
  "categoria": "fundo",
  "risco": "medio",
  "rentabilidade": "Variável - 6% a 12% ao ano",
  "aporte_minimo": 100.00,
  "indicado_para": "Perfil moderado que busca diversificação e renda recorrente mensal"
}
```

---

## Estratégia de Integração

### Como os dados são carregados?

Os dados são carregados via código usando `pandas` para os arquivos CSV e `json` para os arquivos JSON. O decorator `@st.cache_data` garante que os arquivos sejam lidos do disco **apenas uma vez** — nas interações seguintes o Streamlit retorna o resultado direto da memória, com ganho real de performance:

```python
import pandas as pd
import json
import streamlit as st

@st.cache_data  # ← carrega do disco só uma vez, retorna do cache nas próximas
def carregar_dados():
    historico  = pd.read_csv('data/historico_atendimento.csv')
    transacoes = pd.read_csv('data/transacoes.csv')
    with open('data/perfil_investidor.json', 'r', encoding='utf-8') as f:
        perfil = json.load(f)
    with open('data/produtos_financeiros.json', 'r', encoding='utf-8') as f:
        produtos = json.load(f)
    return historico, transacoes, perfil, produtos

historico, transacoes, perfil, produtos = carregar_dados()
```

> **Atenção:** o `@st.cache_data` deve ser usado **apenas para dados estáticos**. O `metricas.csv` cresce a cada interação e por isso **não usa cache** — caso contrário o dashboard exibiria dados desatualizados.

---

### Como os dados são usados no prompt?

Os dados são injetados dinamicamente em uma f-string que monta o contexto a cada interação, garantindo que o modelo sempre tenha acesso às informações mais recentes do cliente:

```python
CONTEXTO = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO R$: {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""
```

Dois detalhes técnicos importantes nessa montagem:

- **`index=False`** — remove o índice numérico do pandas antes de enviar ao modelo. Esse número é apenas um contador interno do Python e não representa nenhuma informação financeira real — removê-lo economiza tokens desnecessários a cada chamada.
- **`ensure_ascii=False`** — garante que acentos e caracteres especiais do português apareçam legíveis no contexto. Sem isso, palavras como "Aplicação" chegariam ao modelo como `Aplica\u00e7\u00e3o`, consumindo mais tokens e tornando o texto menos natural.

---

## Exemplo de Contexto Montado

Exemplo de como os dados são formatados antes de serem enviados ao modelo — organizado, padronizado e conciso, seguindo boas práticas de economia de tokens:

```
Dados do Cliente:
- Nome: João Silva
- Perfil: Moderado
- Objetivo: Construir reserva de emergência
- Reserva atual: R$ 15.000 (meta: R$ 20.000)

Resumo de Gastos:
- Moradia: R$ 1.300
- Alimentação: R$ 570
- Transporte: R$ 295
- Saúde: R$ 188
- Lazer: R$ 55,90
- Total de saídas: R$ 2.488,90

Produtos Disponíveis Para Explicar/Sugerir:
- Tesouro Selic (risco baixo)
- CDB Liquidez Diária (risco baixo)
- LCI/LCA (risco baixo)
- Fundo Imobiliário - FII (risco médio)
- Fundo Multimercado (risco médio)
- Fundo de Ações (risco alto)
```

---

## Base de Dados Completa

Abaixo estão os dados completos utilizados pelo agente em produção.

### perfil_investidor.json

```json
{
  "nome": "João Silva",
  "idade": 32,
  "profissao": "Analista de Sistemas",
  "renda_mensal": 5000.00,
  "perfil_investidor": "moderado",
  "objetivo_principal": "Construir reserva de emergência",
  "patrimonio_total": 15000.00,
  "reserva_emergencia_atual": 10000.00,
  "aceita_risco": false,
  "metas": [
    {
      "meta": "Completar reserva de emergência",
      "valor_necessario": 15000.00,
      "prazo": "2026-06"
    },
    {
      "meta": "Entrada do apartamento",
      "valor_necessario": 50000.00,
      "prazo": "2027-12"
    }
  ]
}
```

### transacoes.csv

| data | descricao | categoria | valor | tipo |
|---|---|---|---|---|
| 2025-10-01 | Salário | receita | 5000.00 | entrada |
| 2025-10-02 | Aluguel | moradia | 1200.00 | saida |
| 2025-10-03 | Supermercado | alimentacao | 450.00 | saida |
| 2025-10-05 | Netflix | lazer | 55.90 | saida |
| 2025-10-07 | Farmácia | saude | 89.00 | saida |
| 2025-10-10 | Restaurante | alimentacao | 120.00 | saida |
| 2025-10-12 | Uber | transporte | 45.00 | saida |
| 2025-10-15 | Conta de Luz | moradia | 180.00 | saida |
| 2025-10-20 | Academia | saude | 99.00 | saida |
| 2025-10-25 | Combustível | transporte | 250.00 | saida |

### produtos_financeiros.json

| Nome | Categoria | Risco | Rentabilidade | Aporte Mínimo | Indicado Para |
|---|---|---|---|---|---|
| Tesouro Selic | renda_fixa | baixo | 100% da Selic | R$ 30,00 | Reserva de emergência e iniciantes |
| CDB Liquidez Diária | renda_fixa | baixo | 102% do CDI | R$ 100,00 | Quem busca segurança com rendimento diário |
| LCI/LCA | renda_fixa | baixo | 95% do CDI | R$ 1.000,00 | Quem pode esperar 90 dias (isento de IR) |
| Fundo Multimercado | fundo | medio | CDI + 2% | R$ 500,00 | Perfil moderado que busca diversificação |
| Fundo Imobiliário (FII) ⭐ | fundo | medio | 6% a 12% ao ano | R$ 100,00 | Perfil moderado que busca renda recorrente mensal |
| Fundo de Ações | fundo | alto | Variável | R$ 100,00 | Perfil arrojado com foco no longo prazo |

> ⭐ Produto adicionado como expansão dos dados mockados originais.

### historico_atendimento.csv

| data | canal | tema | resumo | resolvido |
|---|---|---|---|---|
| 2025-09-15 | chat | CDB | Cliente perguntou sobre rentabilidade e prazos | sim |
| 2025-09-22 | telefone | Problema no app | Erro ao visualizar extrato foi corrigido | sim |
| 2025-10-01 | chat | Tesouro Selic | Cliente pediu explicação sobre o funcionamento do Tesouro Direto | sim |
| 2025-10-12 | chat | Metas financeiras | Cliente acompanhou o progresso da reserva de emergência | sim |
| 2025-10-25 | email | Atualização cadastral | Cliente atualizou e-mail e telefone | sim |
