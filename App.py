from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import PyPDF2
import re
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf'}

# Criar pasta de uploads se não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_pdf(pdf_path):
    """Extrai texto de um arquivo PDF"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        raise Exception(f"Erro ao ler PDF: {str(e)}")

def preprocess_text(text):
    """Pré-processa o texto do email"""
    # Remove espaços extras e quebras de linha excessivas
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def classify_email_simple(text):
    """
    Classificação baseada em palavras-chave (fallback caso API não esteja disponível)
    """
    text_lower = text.lower()
    
    # Palavras-chave para emails produtivos
    productive_keywords = [
        'suporte', 'problema', 'erro', 'ajuda', 'dúvida', 'solicitação',
        'urgente', 'status', 'atualização', 'prazo', 'pendência', 'requisição',
        'sistema', 'acesso', 'senha', 'login', 'configuração', 'bug',
        'relatório', 'documento', 'análise', 'aprovação', 'revisão'
    ]
    
    # Palavras-chave para emails improdutivos
    unproductive_keywords = [
        'feliz', 'parabéns', 'aniversário', 'natal', 'ano novo', 'obrigado',
        'agradecimento', 'festa', 'celebração', 'feriado'
    ]
    
    productive_score = sum(1 for keyword in productive_keywords if keyword in text_lower)
    unproductive_score = sum(1 for keyword in unproductive_keywords if keyword in text_lower)
    
    if productive_score > unproductive_score:
        return "Produtivo", productive_score / (productive_score + unproductive_score + 1)
    else:
        return "Improdutivo", unproductive_score / (productive_score + unproductive_score + 1)

def generate_response(category, email_text):
    """
    Gera uma resposta automática baseada na categoria
    """
    if category == "Produtivo":
        # Detectar tipo específico de solicitação
        text_lower = email_text.lower()
        
        if any(word in text_lower for word in ['status', 'andamento', 'atualização']):
            return """Prezado(a),

Recebemos sua solicitação de atualização sobre o caso em andamento.

Nossa equipe já está verificando o status atual e em breve retornaremos com as informações solicitadas.

Tempo estimado de resposta: 24-48 horas úteis.

Atenciosamente,
Equipe de Suporte"""
        
        elif any(word in text_lower for word in ['problema', 'erro', 'bug', 'defeito']):
            return """Prezado(a),

Identificamos que você está reportando um problema técnico.

Nossa equipe técnica foi notificada e irá analisar a situação com prioridade.

Por favor, mantenha este email como referência. Número do ticket: #{ticket_id}

Atenciosamente,
Equipe de Suporte Técnico"""
        
        elif any(word in text_lower for word in ['dúvida', 'pergunta', 'como', 'ajuda']):
            return """Prezado(a),

Recebemos sua dúvida e estamos preparando uma resposta detalhada.

Nossa equipe de atendimento entrará em contato em breve para esclarecer todas as suas questões.

Tempo estimado de resposta: 24 horas úteis.

Atenciosamente,
Equipe de Atendimento"""
        
        else:
            return """Prezado(a),

Recebemos sua mensagem e ela está sendo analisada pela equipe responsável.

Retornaremos com uma resposta em breve.

Atenciosamente,
Equipe de Atendimento"""
    
    else:  # Improdutivo
        return """Prezado(a),

Agradecemos sua mensagem!

Ficamos felizes com seu contato e desejamos tudo de melhor.

Atenciosamente,
Equipe"""

def classify_with_api(text):
    """
    Classificação usando API de IA (Hugging Face como exemplo)
    Você pode substituir por OpenAI, Anthropic, ou outra API
    """
    try:
        # Aqui você pode integrar com APIs reais
        # Exemplo com Hugging Face Inference API:
        
        # import requests
        # API_URL = "https://api-inference.huggingface.co/models/..."
        # headers = {"Authorization": f"Bearer {API_TOKEN}"}
        # response = requests.post(API_URL, headers=headers, json={"inputs": text})
        
        # Por enquanto, usando classificação simples
        return classify_email_simple(text)
    except Exception as e:
        # Fallback para classificação simples
        print(f"Erro na API: {e}")
        return classify_email_simple(text)

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    """Endpoint para classificar emails"""
    try:
        email_text = None
        
        # Verificar se há arquivo enviado
        if 'file' in request.files:
            file = request.files['file']
            
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Extrair texto baseado no tipo de arquivo
                if filename.endswith('.pdf'):
                    email_text = extract_text_from_pdf(filepath)
                else:  # .txt
                    with open(filepath, 'r', encoding='utf-8') as f:
                        email_text = f.read()
                
                # Remover arquivo após processamento
                os.remove(filepath)
        
        # Verificar se há texto direto
        elif 'email_text' in request.form:
            email_text = request.form['email_text']
        
        if not email_text or email_text.strip() == '':
            return jsonify({
                'success': False,
                'error': 'Nenhum conteúdo de email fornecido'
            }), 400
        
        # Pré-processar texto
        processed_text = preprocess_text(email_text)
        
        # Classificar email
        category, confidence = classify_with_api(processed_text)
        
        # Gerar resposta automática
        suggested_response = generate_response(category, processed_text)
        
        return jsonify({
            'success': True,
            'category': category,
            'confidence': round(confidence * 100, 2),
            'suggested_response': suggested_response,
            'email_preview': email_text[:200] + '...' if len(email_text) > 200 else email_text,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health')
def health():
    """Endpoint de health check para monitoramento"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Para desenvolvimento local
    app.run(debug=True, host='0.0.0.0', port=5000)