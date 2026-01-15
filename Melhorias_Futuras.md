# 🚀 Melhorias Futuras e Integração com APIs de IA

Este documento descreve possíveis melhorias e como integrar o sistema com diferentes APIs de IA.

---

## 🤖 INTEGRAÇÃO COM APIs DE IA

### 1. OpenAI GPT (ChatGPT)

#### Instalação
```bash
pip install openai
```

#### Código de Integração
Adicione no `app.py`:

```python
import openai
import os

# Configurar API key (usar variável de ambiente)
openai.api_key = os.getenv('OPENAI_API_KEY')

def classify_with_openai(email_text):
    """Classifica email usando OpenAI GPT"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """Você é um assistente especializado em classificar emails corporativos.
                    Classifique o email em uma destas categorias:
                    - Produtivo: emails que requerem ação (suporte, dúvidas, problemas, solicitações)
                    - Improdutivo: emails sociais (felicitações, agradecimentos)
                    
                    Responda em formato JSON: {"category": "Produtivo" ou "Improdutivo", "confidence": 0-100}"""
                },
                {
                    "role": "user",
                    "content": f"Classifique este email:\n\n{email_text}"
                }
            ],
            temperature=0.3,
            max_tokens=100
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        return result['category'], result['confidence'] / 100
    except Exception as e:
        print(f"Erro na API OpenAI: {e}")
        # Fallback para classificação simples
        return classify_email_simple(email_text)

def generate_response_with_openai(category, email_text):
    """Gera resposta usando OpenAI GPT"""
    try:
        prompt = f"""Gere uma resposta profissional para este email classificado como {category}:

{email_text}

A resposta deve ser:
- Profissional e cordial
- Adequada para email corporativo
- Em português brasileiro
- Máximo 150 palavras"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=250
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Erro ao gerar resposta: {e}")
        return generate_response(category, email_text)
```

#### Configurar Variável de Ambiente
```bash
export OPENAI_API_KEY='sua-api-key-aqui'
```

---

### 2. Hugging Face Transformers

#### Instalação
```bash
pip install transformers torch
```

#### Código de Integração

```python
from transformers import pipeline

# Inicializar modelo (fazer uma vez no início)
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

def classify_with_huggingface(email_text):
    """Classifica email usando Hugging Face"""
    try:
        candidate_labels = ["produtivo", "improdutivo"]
        
        result = classifier(
            email_text,
            candidate_labels,
            hypothesis_template="Este email é {}."
        )
        
        category = "Produtivo" if result['labels'][0] == "produtivo" else "Improdutivo"
        confidence = result['scores'][0]
        
        return category, confidence
    except Exception as e:
        print(f"Erro Hugging Face: {e}")
        return classify_email_simple(email_text)
```

#### Modelo em Português
Para melhor performance em português:

```python
# Usar modelo treinado em português
classifier = pipeline(
    "text-classification",
    model="neuralmind/bert-base-portuguese-cased"
)
```

---

### 3. Hugging Face Inference API (Sem instalar modelo localmente)

#### Instalação
```bash
pip install requests
```

#### Código

```python
import requests

def classify_with_hf_api(email_text):
    """Usa API de Inferência da Hugging Face"""
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
    headers = {"Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}"}
    
    payload = {
        "inputs": email_text,
        "parameters": {
            "candidate_labels": ["produtivo", "improdutivo"]
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()
        
        category = "Produtivo" if result['labels'][0] == "produtivo" else "Improdutivo"
        confidence = result['scores'][0]
        
        return category, confidence
    except Exception as e:
        print(f"Erro HF API: {e}")
        return classify_email_simple(email_text)
```

---

### 4. Google Cloud Natural Language API

#### Instalação
```bash
pip install google-cloud-language
```

#### Código

```python
from google.cloud import language_v1

def classify_with_google_nlp(email_text):
    """Classifica usando Google Cloud NLP"""
    client = language_v1.LanguageServiceClient()
    
    document = language_v1.Document(
        content=email_text,
        type_=language_v1.Document.Type.PLAIN_TEXT
    )
    
    # Análise de sentimento e entidades
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    entities = client.analyze_entities(document=document).entities
    
    # Lógica customizada baseada em sentiment e entities
    # ...
    
    return category, confidence
```

---

## 📊 MELHORIAS FUTURAS

### 1. Machine Learning Customizado

#### Treinar modelo próprio com scikit-learn

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle

# Dados de treinamento (expandir com mais exemplos)
emails_treino = [
    "Preciso de suporte urgente com o sistema",
    "Há um erro ao fazer login",
    "Feliz aniversário para toda equipe!",
    "Obrigado pelo excelente trabalho",
    # ... adicionar mais exemplos
]

labels_treino = [
    "Produtivo",
    "Produtivo", 
    "Improdutivo",
    "Improdutivo",
    # ...
]

# Criar e treinar modelo
model = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=1000)),
    ('classifier', MultinomialNB())
])

model.fit(emails_treino, labels_treino)

# Salvar modelo
with open('email_classifier_model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Usar modelo
def classify_with_custom_model(email_text):
    with open('email_classifier_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    prediction = model.predict([email_text])[0]
    proba = model.predict_proba([email_text])[0]
    confidence = max(proba)
    
    return prediction, confidence
```

### 2. Banco de Dados para Histórico

```python
import sqlite3
from datetime import datetime

def save_classification(email_text, category, confidence):
    """Salva classificação no banco"""
    conn = sqlite3.connect('classifications.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_text TEXT,
            category TEXT,
            confidence REAL,
            timestamp DATETIME
        )
    ''')
    
    cursor.execute('''
        INSERT INTO classifications (email_text, category, confidence, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (email_text, category, confidence, datetime.now()))
    
    conn.commit()
    conn.close()

def get_statistics():
    """Retorna estatísticas das classificações"""
    conn = sqlite3.connect('classifications.db')
    cursor = conn.cursor()
    
    stats = cursor.execute('''
        SELECT 
            category,
            COUNT(*) as total,
            AVG(confidence) as avg_confidence
        FROM classifications
        GROUP BY category
    ''').fetchall()
    
    conn.close()
    return stats
```

### 3. Dashboard de Análise

Adicionar rota no Flask:

```python
@app.route('/dashboard')
def dashboard():
    """Dashboard com estatísticas"""
    stats = get_statistics()
    return render_template('dashboard.html', stats=stats)
```

### 4. API REST para Integração

```python
@app.route('/api/classify', methods=['POST'])
def api_classify():
    """API endpoint para classificação"""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'Text is required'}), 400
    
    category, confidence = classify_with_api(data['text'])
    response = generate_response(category, data['text'])
    
    return jsonify({
        'category': category,
        'confidence': confidence * 100,
        'suggested_response': response
    })
```

### 5. Autenticação de Usuários

```python
from flask_login import LoginManager, login_required

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/classify')
@login_required
def classify():
    # Apenas usuários logados podem classificar
    pass
```

### 6. Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/classify')
@limiter.limit("10 per minute")
def classify():
    pass
```

### 7. Cache de Respostas

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def classify_cached(email_text):
    """Classifica com cache para emails repetidos"""
    return classify_with_api(email_text)
```

### 8. Processamento em Lote

```python
@app.route('/classify-batch', methods=['POST'])
def classify_batch():
    """Classifica múltiplos emails de uma vez"""
    emails = request.json.get('emails', [])
    
    results = []
    for email in emails:
        category, confidence = classify_with_api(email)
        results.append({
            'email': email[:100],
            'category': category,
            'confidence': confidence
        })
    
    return jsonify(results)
```

### 9. Exportação de Relatórios

```python
import csv
from io import StringIO

@app.route('/export-csv')
def export_csv():
    """Exporta classificações em CSV"""
    conn = sqlite3.connect('classifications.db')
    cursor = conn.cursor()
    
    data = cursor.execute('SELECT * FROM classifications').fetchall()
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Email', 'Category', 'Confidence', 'Timestamp'])
    writer.writerows(data)
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=classifications.csv'}
    )
```

### 10. Análise de Sentimento

```python
from textblob import TextBlob

def analyze_sentiment(email_text):
    """Analisa sentimento do email"""
    blob = TextBlob(email_text)
    
    sentiment = blob.sentiment.polarity
    
    if sentiment > 0.1:
        return "Positivo"
    elif sentiment < -0.1:
        return "Negativo"
    else:
        return "Neutro"
```

---

## 🎯 ROADMAP DE IMPLEMENTAÇÃO

### Fase 1 - Básico (Atual)
- [x] Interface web funcional
- [x] Classificação por palavras-chave
- [x] Geração de respostas simples
- [x] Deploy na nuvem

### Fase 2 - IA Avançada
- [ ] Integração com OpenAI/Hugging Face
- [ ] Modelo ML customizado
- [ ] Análise de sentimento

### Fase 3 - Features Avançadas
- [ ] Banco de dados
- [ ] Dashboard de estatísticas
- [ ] API REST
- [ ] Autenticação

### Fase 4 - Produção
- [ ] Cache
- [ ] Rate limiting
- [ ] Logs avançados
- [ ] Monitoramento

---

## 💡 DICAS DE IMPLEMENTAÇÃO

1. **Comece simples**: Implemente uma feature por vez
2. **Teste sempre**: Cada mudança deve ser testada
3. **Documente**: Mantenha README atualizado
4. **Use variáveis de ambiente**: Para API keys
5. **Versionamento**: Use git tags para versões

---

## 📚 RECURSOS ADICIONAIS

### Tutoriais
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Hugging Face Course](https://huggingface.co/course)
- [OpenAI Cookbook](https://github.com/openai/openai-cookbook)

### Datasets para Treinamento
- [Kaggle Email Classification](https://www.kaggle.com/datasets)
- [Enron Email Dataset](https://www.cs.cmu.edu/~enron/)

### Ferramentas
- [Postman](https://www.postman.com/) - Testar APIs
- [MLflow](https://mlflow.org/) - Gerenciar experimentos ML
- [Weights & Biases](https://wandb.ai/) - Tracking de modelos

---

**Continue evoluindo seu projeto! 🚀**