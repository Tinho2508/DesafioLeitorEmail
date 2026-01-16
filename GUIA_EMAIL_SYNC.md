# 📧 Guia de Sincronização Automática de Emails

Sistema que busca emails automaticamente e os classifica usando IA.

---

## 🎯 O QUE FAZ?

1. ✅ Conecta automaticamente com seu email (Gmail, Outlook, Yahoo)
2. ✅ Busca emails não lidos a cada 60 segundos
3. ✅ Classifica cada email usando IA
4. ✅ Gera resposta automática
5. ✅ Salva log de todas as classificações

---

## ⚙️ CONFIGURAÇÃO

### 1️⃣ Gmail (Recomendado)

#### Passo 1: Gerar Senha de App

1. Acesse: https://myaccount.google.com/security
2. Ative **"Verificação em duas etapas"**
3. Procure por **"Senhas de app"**
4. Crie nova senha:
   - Selecione: **Email**
   - Dispositivo: **Outro (nome personalizado)**
   - Digite: **"Classificador IA"**
5. Copie a senha gerada (16 caracteres)

#### Passo 2: Configurar no Código

Abra `email_sync.py` e edite:
```python
EMAIL_ADDRESS = "seu-email@gmail.com"  # Seu email
EMAIL_PASSWORD = "abcd efgh ijkl mnop"  # Senha de app (16 caracteres)
IMAP_SERVER = "imap.gmail.com"
```

---

### 2️⃣ Outlook/Hotmail
```python
EMAIL_ADDRESS = "seu-email@outlook.com"
EMAIL_PASSWORD = "sua-senha-normal"
IMAP_SERVER = "outlook.office365.com"
```

---

### 3️⃣ Yahoo Mail
```python
EMAIL_ADDRESS = "seu-email@yahoo.com"
EMAIL_PASSWORD = "senha-de-app-yahoo"
IMAP_SERVER = "imap.mail.yahoo.com"
```

💡 Yahoo também requer senha de app

---

## 🚀 COMO USAR

### Modo 1: Sincronização Contínua

Terminal 1 - Rodar o classificador:
```bash
python app.py
```

Terminal 2 - Rodar o sincronizador:
```bash
python email_sync.py
```

O sistema vai:
- Verificar emails a cada 60 segundos
- Classificar automaticamente
- Mostrar resultados no terminal
- Salvar log em `email_classifications.json`

---

### Modo 2: Verificação Única

Edite `email_sync.py`, comente a linha do loop:
```python
# time.sleep(self.config.CHECK_INTERVAL)  # Comentar
break  # Adicionar
```

Execute:
```bash
python email_sync.py
```

Processa uma vez e para.

---

## 🎛️ CONFIGURAÇÕES AVANÇADAS

Edite estas variáveis em `EmailConfig`:
```python
# Intervalo entre verificações (segundos)
CHECK_INTERVAL = 60  # Padrão: 60s

# Classificar automaticamente
AUTO_CLASSIFY = True  # True = classifica

# Responder automaticamente (CUIDADO!)
AUTO_RESPOND = False  # Deixe False

# Marcar como lido após processar
MARK_AS_READ = False  # False = mantém não lido
```

---

## 📊 LOG DE CLASSIFICAÇÕES

O arquivo `email_classifications.json` salva:
```json
[
  {
    "timestamp": "2025-01-15T10:30:00",
    "subject": "Problema no sistema",
    "from": "usuario@empresa.com",
    "category": "Produtivo",
    "confidence": 92.5,
    "response": "Prezado(a)..."
  }
]
```

---

## 🔍 EXEMPLO DE USO

### Saída no Terminal:
```
🔍 Verificando emails... [10:30:45]
📬 3 emails não lidos encontrados

============================================================
📨 PROCESSANDO 3 EMAILS
============================================================

📧 Email 1/3
   De: joao@empresa.com
   Assunto: Erro no login
   Data: Wed, 15 Jan 2025 10:25:33

🤖 Classificando: 'Erro no login'...
   ✅ Categoria: Produtivo
   📊 Confiança: 87.3%
   📝 Resposta sugerida:
      Prezado(a), Identificamos que você está reportando...
   💾 Log salvo em email_classifications.json
   ✅ Processado

📧 Email 2/3
   De: maria@empresa.com
   Assunto: Feliz Ano Novo!
   Data: Wed, 15 Jan 2025 09:15:22

🤖 Classificando: 'Feliz Ano Novo!'...
   ✅ Categoria: Improdutivo
   📊 Confiança: 95.1%
   📝 Resposta sugerida:
      Agradecemos sua mensagem! Ficamos felizes...
   💾 Log salvo em email_classifications.json
   ✅ Processado
```

---

## ⚠️ SEGURANÇA

### ✅ RECOMENDAÇÕES:

1. **Nunca compartilhe** sua senha de app
2. **Deixe AUTO_RESPOND = False** até testar bem
3. **Use senha de app**, não sua senha principal
4. **Revise os logs** regularmente
5. **Teste em email secundário** primeiro

### 🔒 SENHAS DE APP:

- Não dão acesso total à conta
- Podem ser revogadas a qualquer momento
- Específicas para cada aplicação

---

## 🐛 TROUBLESHOOTING

### Erro: "Authentication failed"

**Solução:**
1. Verifique se usou senha de app (não senha normal)
2. Confirme que verificação em 2 etapas está ativa
3. Tente gerar nova senha de app

### Erro: "Connection refused"

**Solução:**
1. Verifique conexão com internet
2. Confira IMAP_SERVER correto
3. Alguns provedores bloqueiam IMAP (habilite nas configurações)

### "Classificador não está rodando"

**Solução:**
```bash
# Em outro terminal
python app.py
```

---

## 🎯 CASOS DE USO

### 1. Monitor de Suporte
- Detecta emails de suporte automaticamente
- Prioriza casos urgentes
- Gera respostas padrão

### 2. Filtro de Spam Social
- Separa emails sociais de trabalho
- Permite focar no importante

### 3. Assistente de Email
- Sugere respostas
- Economiza tempo da equipe

---

## 📈 PRÓXIMOS PASSOS

### Melhorias Possíveis:

1. **Dashboard Web**
   - Visualizar estatísticas
   - Gráficos de classificação

2. **Notificações**
   - Alertas para emails urgentes
   - Telegram/Slack

3. **Respostas Automáticas**
   - Implementar SMTP
   - Envio automático seguro

4. **Múltiplas Contas**
   - Monitorar vários emails
   - Centralizar em uma interface

---

## 💡 DICAS

1. **Teste primeiro** com email pessoal
2. **Monitore o log** email_classifications.json
3. **Ajuste intervalo** conforme necessidade
4. **Use filtros** para emails específicos

---

**Dúvidas? Consulte a documentação ou entre em contato!**