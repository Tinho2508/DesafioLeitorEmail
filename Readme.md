# 📧 Classificador Inteligente de Emails

Solução completa de IA para classificação automática de emails corporativos e geração de respostas inteligentes.

## 🎯 Sobre o Projeto

Este projeto foi desenvolvido como resposta ao desafio AutoU, criando uma aplicação web que utiliza inteligência artificial para:

- ✅ Classificar emails em **Produtivo** ou **Improdutivo**
- ✅ Gerar respostas automáticas contextualizadas
- ✅ Processar arquivos .txt e .pdf
- ✅ Interface moderna e intuitiva
- ✅ Deploy em nuvem

## 🚀 Funcionalidades

### Classificação Inteligente
- Análise de conteúdo usando NLP
- Categorização automática (Produtivo/Improdutivo)
- Nível de confiança da classificação

### Geração de Respostas
- Respostas automáticas contextualizadas
- Adaptadas ao tipo de solicitação
- Prontas para copiar e usar

### Interface Amigável
- Design moderno e responsivo
- Upload por drag & drop
- Feedback visual em tempo real
- Experiência mobile-first

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.11+**
- **Flask** - Framework web
- **PyPDF2** - Processamento de PDFs
- **NLP** - Processamento de linguagem natural

### Frontend
- **HTML5**
- **CSS3** (Design moderno com variáveis CSS)
- **JavaScript** (Vanilla JS - sem frameworks)

### Deploy
- **Render / Heroku / Vercel** (compatível com múltiplas plataformas)
- **Gunicorn** - Servidor WSGI

## 📋 Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Git

## 🔧 Instalação e Uso Local

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/DesafioLeitorEmail.git
cd DesafioLeitorEmail
```

### 2. Crie um ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação

```bash
python app.py
```

### 5. Acesse no navegador

Abra seu navegador e acesse: `http://localhost:5000`

## 🌐 Deploy na Nuvem

### Opção 1: Render (Recomendado)

1. Crie uma conta em [render.com](https://render.com)
2. Conecte seu repositório GitHub
3. Configure um novo Web Service
4. Use as seguintes configurações:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment**: Python 3

### Opção 2: Heroku

```bash
# Instale o Heroku CLI
heroku login
heroku create seu-app-name
git push heroku main
heroku open
```

### Opção 3: Vercel

1. Instale Vercel CLI: `npm i -g vercel`
2. Execute: `vercel`
3. Siga as instruções

## 📂 Estrutura do Projeto

```
cd DesafioLeitorEmail
/
├── app.py                  # Aplicação Flask principal
├── requirements.txt        # Dependências Python
├── README.md              # Documentação
├── Procfile               # Configuração Heroku (opcional)
├── static/
│   ├── css/
│   │   └── style.css      # Estilos da aplicação
│   └── js/
│       └── script.js      # Lógica do frontend
├── templates/
│   └── index.html         # Página principal
└── uploads/               # Pasta temporária (criada automaticamente)
```

## 🎨 Como Usar a Aplicação

### Método 1: Colar Texto
1. Selecione a aba "Colar Texto"
2. Cole o conteúdo do email no campo de texto
3. Clique em "Analisar Email"

### Método 2: Upload de Arquivo
1. Selecione a aba "Upload de Arquivo"
2. Arraste um arquivo .txt ou .pdf OU clique para selecionar
3. Clique em "Analisar Email"

### Resultado
- Veja a **categoria** (Produtivo/Improdutivo)
- Confira o **nível de confiança** da análise
- Leia a **resposta sugerida**
- Clique em "Copiar" para usar a resposta

## 🧠 Como Funciona a IA

### 1. Pré-processamento
- Limpeza do texto
- Remoção de caracteres especiais
- Normalização de espaços

### 2. Classificação
O sistema usa análise de palavras-chave e contexto para classificar:

**Emails Produtivos** contêm termos como:
- Solicitações (suporte, ajuda, dúvida)
- Status (atualização, prazo, pendência)
- Problemas (erro, bug, problema)
- Documentos (relatório, análise, aprovação)

**Emails Improdutivos** contêm termos como:
- Felicitações (parabéns, feliz)
- Agradecimentos
- Mensagens sociais

### 3. Geração de Resposta
Baseado na categoria e contexto, o sistema gera uma resposta adequada:
- Para problemas técnicos → Resposta com número de ticket
- Para dúvidas → Resposta com prazo de atendimento
- Para mensagens sociais → Resposta cordial

## 🔄 Integração com APIs de IA (Opcional)

O código está preparado para integração com APIs como:

### Hugging Face
```python
import requests

API_URL = "https://api-inference.huggingface.co/models/..."
headers = {"Authorization": f"Bearer {YOUR_TOKEN}"}
response = requests.post(API_URL, headers=headers, json={"inputs": text})
```

### OpenAI
```python
import openai

openai.api_key = "your-api-key"
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": text}]
)
```

## 📊 Exemplos de Emails para Teste

### Email Produtivo - Suporte
```
Assunto: Problema no sistema

Olá,

Estou tendo dificuldades para acessar o sistema desde ontem.
Quando tento fazer login, recebo uma mensagem de erro.

Podem me ajudar?

Obrigado
```

### Email Produtivo - Status
```
Assunto: Status da requisição #1234

Boa tarde,

Gostaria de saber o andamento da requisição #1234
que foi aberta na semana passada.

Há previsão de conclusão?

Atenciosamente
```

### Email Improdutivo
```
Assunto: Feliz Natal!

Olá equipe,

Desejo a todos um Feliz Natal e um próspero Ano Novo!

Que 2025 seja repleto de realizações.

Abraços!
```

## 🎯 Diferenciais do Projeto

- ✨ Interface moderna e profissional
- 🎨 Design system consistente
- 📱 Totalmente responsivo
- ⚡ Performance otimizada
- 🔒 Tratamento de erros robusto
- 📝 Código limpo e documentado
- 🚀 Fácil deploy em múltiplas plataformas

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests

## 📝 Licença

Este projeto foi desenvolvido como parte de um desafio técnico e está disponível para fins educacionais.

## 👤 Autor

Jose Ailton
Desenvolvido para o desafio AutoU

## 📧 Contato

Para dúvidas ou sugestões, entre em contato através do GitHub.

---

**⭐ Se este projeto foi útil para você, considere dar uma estrela no GitHub!**