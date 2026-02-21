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
src/
├── app.py              # Aplicação principal (Streamlit)
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

