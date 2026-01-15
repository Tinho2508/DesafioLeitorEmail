# 🚀 Guia Completo de Deploy

Este guia contém instruções detalhadas para fazer deploy da aplicação em diferentes plataformas de nuvem.

---

## 📋 PRÉ-REQUISITOS

Antes de começar, certifique-se de ter:
- [ ] Conta no GitHub
- [ ] Código do projeto em um repositório público no GitHub
- [ ] Git instalado localmente

---

## 🎯 OPÇÃO 1: RENDER (RECOMENDADO - MAIS FÁCIL)

### Por que Render?
✅ Totalmente gratuito
✅ Deploy automático
✅ SSL/HTTPS incluso
✅ Muito simples de configurar

### Passo a Passo

#### 1. Criar conta no Render
1. Acesse: https://render.com
2. Clique em "Get Started"
3. Crie conta com GitHub (recomendado)

#### 2. Preparar o projeto
Certifique-se que seu repositório tem:
```
cd DesafioLeitorEmail
/
├── app.py
├── requirements.txt
├── Procfile (opcional para Render)
├── static/
├── templates/
└── ...
```

#### 3. Criar novo Web Service
1. No dashboard do Render, clique em "New +"
2. Selecione "Web Service"
3. Conecte seu repositório GitHub
4. Selecione o repositório `cd DesafioLeitorEmail
`

#### 4. Configurar o serviço
**Preencha os campos:**
- **Name**: `cd DesafioLeitorEmail
-[seu-nome]` (deve ser único)
- **Region**: Choose the closest region
- **Branch**: `main` ou `master`
- **Runtime**: `Python 3`
- **Build Command**: 
  ```
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```
  gunicorn app:app
  ```

#### 5. Configurações avançadas (opcional)
- **Instance Type**: `Free`
- **Environment Variables**: Nenhuma necessária no momento

#### 6. Deploy
1. Clique em "Create Web Service"
2. Aguarde o build (3-5 minutos)
3. Quando aparecer "Live", seu site está no ar! 🎉

#### 7. Testar
1. Acesse a URL fornecida: `https://cd DesafioLeitorEmail
-[seu-nome].onrender.com`
2. Teste todas as funcionalidades

### ⚠️ IMPORTANTE - Render Free Tier
- O serviço gratuito "dorme" após 15 minutos de inatividade
- Primeira requisição após "acordar" demora ~30 segundos
- Perfeito para demonstrações e testes

---

## 🎯 OPÇÃO 2: HEROKU

### Preparação

#### 1. Criar conta
1. Acesse: https://heroku.com
2. Crie uma conta gratuita

#### 2. Instalar Heroku CLI
**Windows:**
- Baixe: https://devcenter.heroku.com/articles/heroku-cli
- Execute o instalador

**Mac:**
```bash
brew tap heroku/brew && brew install heroku
```

**Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

### Deploy

#### 1. Login via CLI
```bash
heroku login
```

#### 2. Criar aplicação
```bash
cd cd DesafioLeitorEmail

heroku create cd DesafioLeitorEmail
-[seu-nome]
```

#### 3. Deploy
```bash
git push heroku main
```

Se seu branch principal é `master`:
```bash
git push heroku master
```

#### 4. Verificar
```bash
heroku open
```

#### 5. Ver logs (se necessário)
```bash
heroku logs --tail
```

### Problemas Comuns

**Erro: "No web processes running"**
```bash
heroku ps:scale web=1
```

**Erro de build:**
```bash
heroku logs --tail
# Verifique requirements.txt e Procfile
```

---

## 🎯 OPÇÃO 3: RAILWAY

### Por que Railway?
✅ Interface moderna
✅ Deploy via GitHub
✅ Tier gratuito generoso

### Passo a Passo

#### 1. Criar conta
1. Acesse: https://railway.app
2. "Start a New Project"
3. Login com GitHub

#### 2. Deploy
1. "New Project"
2. "Deploy from GitHub repo"
3. Selecione seu repositório
4. Railway detecta automaticamente que é Python

#### 3. Configurar
**Railway detecta automaticamente:**
- Build: `pip install -r requirements.txt`
- Start: `gunicorn app:app`

Se precisar configurar manualmente:
1. Settings → Build Command → `pip install -r requirements.txt`
2. Settings → Start Command → `gunicorn app:app`

#### 4. Gerar domínio público
1. Settings → Networking
2. "Generate Domain"
3. Copie a URL

---

## 🎯 OPÇÃO 4: VERCEL (Para Frontend + Serverless)

**Nota:** Vercel é mais indicado para aplicações Next.js, mas funciona com Flask usando serverless.

### Preparação

#### 1. Instalar Vercel CLI
```bash
npm i -g vercel
```

#### 2. Criar arquivo `vercel.json`
Crie na raiz do projeto:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### Deploy

```bash
cd cd DesafioLeitorEmail

vercel
```

Siga as instruções interativas.

---

## 🎯 OPÇÃO 5: GOOGLE CLOUD PLATFORM (Free Tier)

### Preparação

#### 1. Criar projeto no GCP
1. Acesse: https://console.cloud.google.com
2. Crie novo projeto

#### 2. Criar arquivo `app.yaml`
```yaml
runtime: python39

handlers:
  - url: /static
    static_dir: static

  - url: /.*
    script: auto
```

### Deploy

#### 1. Instalar Google Cloud SDK
Siga: https://cloud.google.com/sdk/docs/install

#### 2. Deploy
```bash
gcloud init
gcloud app deploy
```

---

## 📊 COMPARAÇÃO DAS PLATAFORMAS

| Plataforma | Facilidade | Gratuito | SSL | Deploy Automático |
|------------|------------|----------|-----|-------------------|
| **Render** | ⭐⭐⭐⭐⭐ | ✅ | ✅ | ✅ |
| **Heroku** | ⭐⭐⭐⭐ | ✅* | ✅ | ✅ |
| **Railway** | ⭐⭐⭐⭐⭐ | ✅ | ✅ | ✅ |
| **Vercel** | ⭐⭐⭐ | ✅ | ✅ | ✅ |
| **GCP** | ⭐⭐⭐ | ✅* | ✅ | ⚠️ |

*Com limitações

---

## ✅ CHECKLIST PÓS-DEPLOY

Após fazer deploy, verifique:

- [ ] Site está acessível via HTTPS
- [ ] Upload de arquivo .txt funciona
- [ ] Upload de arquivo .pdf funciona
- [ ] Classificação de texto direto funciona
- [ ] Respostas são geradas corretamente
- [ ] Botão "Copiar" funciona
- [ ] Interface responsiva em mobile
- [ ] Sem erros no console do navegador

---

## 🐛 TROUBLESHOOTING

### Problema: Site retorna 500 Internal Server Error

**Solução:**
1. Verificar logs da plataforma
2. Conferir se todas as dependências estão em requirements.txt
3. Verificar se a pasta `uploads` existe

### Problema: Upload de arquivo não funciona

**Solução:**
1. Verificar se a pasta uploads tem permissões corretas
2. Conferir limite de tamanho do arquivo
3. Em algumas plataformas, pode precisar usar storage externo

### Problema: Site muito lento

**Solução:**
1. Plataformas gratuitas têm cold start
2. Primeira requisição demora mais
3. Considere usar tier pago se necessário

### Problema: CSS/JS não carregam

**Solução:**
1. Verificar paths dos arquivos estáticos
2. Conferir se pasta `static` está no repositório
3. Limpar cache do navegador

---

## 🔗 LINKS IMPORTANTES

### Documentação Oficial
- [Render Docs](https://render.com/docs)
- [Heroku Python](https://devcenter.heroku.com/articles/getting-started-with-python)
- [Railway Docs](https://docs.railway.app/)
- [Vercel Docs](https://vercel.com/docs)

### Suporte
- [Render Community](https://community.render.com/)
- [Heroku Support](https://help.heroku.com/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/flask)

---

## 📝 DICAS FINAIS

1. **Teste localmente primeiro**: Sempre teste tudo funcionando antes de fazer deploy
2. **Mantenha secrets seguros**: Nunca commite API keys
3. **Use variáveis de ambiente**: Para configurações sensíveis
4. **Monitore seu app**: Verifique os logs regularmente
5. **Documente tudo**: Anote URLs, credenciais, configurações

---

## 🎓 APÓS O DEPLOY

1. Copie a URL da aplicação
2. Teste todas as funcionalidades
3. Tire screenshots para documentação
4. Adicione a URL no README do GitHub
5. Use a URL no formulário de submissão do desafio

---

**Parabéns! 🎉 Sua aplicação está no ar!**

Se tiver problemas, consulte a documentação da plataforma escolhida ou procure ajuda nas comunidades.