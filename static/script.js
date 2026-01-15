// Elementos do DOM
const tabs = document.querySelectorAll('.tab');
const tabContents = document.querySelectorAll('.tab-content');
const emailForm = document.getElementById('emailForm');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const submitBtn = document.getElementById('submitBtn');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');
const resultsSection = document.getElementById('resultsSection');
const newAnalysisBtn = document.getElementById('newAnalysisBtn');
const copyBtn = document.getElementById('copyBtn');

// Estado atual
let currentTab = 'text';
let selectedFile = null;

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    setupTabSwitching();
    setupFileUpload();
    setupFormSubmit();
    setupCopyButton();
    setupNewAnalysis();
});

// Configurar troca de abas
function setupTabSwitching() {
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.dataset.tab;
            switchTab(targetTab);
        });
    });
}

function switchTab(tabName) {
    currentTab = tabName;

    // Atualizar abas
    tabs.forEach(tab => {
        if (tab.dataset.tab === tabName) {
            tab.classList.add('active');
        } else {
            tab.classList.remove('active');
        }
    });

    // Atualizar conteúdo
    tabContents.forEach(content => {
        if (content.id === `${tabName}-tab`) {
            content.classList.add('active');
        } else {
            content.classList.remove('active');
        }
    });

    // Limpar estado
    hideError();
}

// Configurar upload de arquivo
function setupFileUpload() {
    const fileUploadLabel = document.querySelector('.file-upload-label');

    // Click no label
    fileInput.addEventListener('change', handleFileSelect);

    // Drag and drop
    fileUploadLabel.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileUploadLabel.style.borderColor = 'var(--primary-color)';
        fileUploadLabel.style.background = 'rgba(102, 126, 234, 0.05)';
    });

    fileUploadLabel.addEventListener('dragleave', () => {
        fileUploadLabel.style.borderColor = 'var(--border-color)';
        fileUploadLabel.style.background = 'var(--bg-secondary)';
    });

    fileUploadLabel.addEventListener('drop', (e) => {
        e.preventDefault();
        fileUploadLabel.style.borderColor = 'var(--border-color)';
        fileUploadLabel.style.background = 'var(--bg-secondary)';

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelect();
        }
    });
}

function handleFileSelect() {
    const file = fileInput.files[0];
    
    if (!file) {
        fileInfo.classList.remove('active');
        selectedFile = null;
        return;
    }

    // Validar tipo de arquivo
    const allowedTypes = ['text/plain', 'application/pdf'];
    if (!allowedTypes.includes(file.type)) {
        showError('Formato de arquivo não suportado. Use .txt ou .pdf');
        fileInput.value = '';
        return;
    }

    // Validar tamanho (16MB)
    const maxSize = 16 * 1024 * 1024;
    if (file.size > maxSize) {
        showError('Arquivo muito grande. O tamanho máximo é 16MB');
        fileInput.value = '';
        return;
    }

    selectedFile = file;

    // Mostrar informações do arquivo
    const fileSize = formatFileSize(file.size);
    fileInfo.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
            </svg>
            <div style="flex: 1;">
                <div style="font-weight: 500; color: var(--text-primary);">${file.name}</div>
                <div style="font-size: 0.875rem; color: var(--text-secondary);">${fileSize}</div>
            </div>
            <button type="button" onclick="clearFile()" style="padding: 0.5rem; background: none; border: none; cursor: pointer; color: var(--text-secondary);">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </button>
        </div>
    `;
    fileInfo.classList.add('active');
    hideError();
}

function clearFile() {
    fileInput.value = '';
    selectedFile = null;
    fileInfo.classList.remove('active');
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Configurar envio do formulário
function setupFormSubmit() {
    emailForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await handleSubmit();
    });
}

async function handleSubmit() {
    hideError();
    
    // Validar entrada
    const emailText = document.getElementById('emailText').value.trim();
    
    if (currentTab === 'text' && !emailText) {
        showError('Por favor, insira o conteúdo do email');
        return;
    }
    
    if (currentTab === 'file' && !selectedFile) {
        showError('Por favor, selecione um arquivo');
        return;
    }

    // Preparar dados
    const formData = new FormData();
    
    if (currentTab === 'text') {
        formData.append('email_text', emailText);
    } else {
        formData.append('file', selectedFile);
    }

    // Mostrar loading
    showLoading();

    try {
        const response = await fetch('/classify', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Erro ao processar email');
        }

        displayResults(data);
    } catch (error) {
        console.error('Erro:', error);
        showError(error.message || 'Erro ao processar sua solicitação. Tente novamente.');
    } finally {
        hideLoading();
    }
}

// Mostrar resultados
function displayResults(data) {
    // Preencher preview do email
    document.getElementById('emailPreview').textContent = data.email_preview;

    // Preencher categoria
    const categoryValue = document.getElementById('categoryValue');
    categoryValue.textContent = data.category;
    categoryValue.className = 'badge-value ' + (data.category === 'Produtivo' ? 'productive' : 'unproductive');

    // Preencher confiança
    const confidenceFill = document.getElementById('confidenceFill');
    const confidenceValue = document.getElementById('confidenceValue');
    
    // Animar a barra de confiança
    setTimeout(() => {
        confidenceFill.style.width = `${data.confidence}%`;
    }, 100);
    
    confidenceValue.textContent = `${data.confidence}%`;

    // Preencher resposta sugerida
    document.getElementById('responseContent').textContent = data.suggested_response;

    // Preencher timestamp
    document.getElementById('timestampInfo').innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle;">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
        </svg>
        Análise realizada em ${data.timestamp}
    `;

    // Mostrar seção de resultados
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Configurar botão de copiar
function setupCopyButton() {
    copyBtn.addEventListener('click', async () => {
        const responseText = document.getElementById('responseContent').textContent;
        
        try {
            await navigator.clipboard.writeText(responseText);
            
            // Feedback visual
            const originalHTML = copyBtn.innerHTML;
            copyBtn.innerHTML = `
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
                Copiado!
            `;
            copyBtn.style.background = 'var(--success-color)';
            copyBtn.style.color = 'white';
            
            setTimeout(() => {
                copyBtn.innerHTML = originalHTML;
                copyBtn.style.background = '';
                copyBtn.style.color = '';
            }, 2000);
        } catch (error) {
            console.error('Erro ao copiar:', error);
            showError('Erro ao copiar texto');
        }
    });
}

// Configurar nova análise
function setupNewAnalysis() {
    newAnalysisBtn.addEventListener('click', () => {
        // Limpar formulário
        document.getElementById('emailText').value = '';
        clearFile();
        
        // Esconder resultados
        resultsSection.style.display = 'none';
        
        // Voltar ao topo
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// Funções de utilidade
function showLoading() {
    loading.style.display = 'block';
    submitBtn.disabled = true;
    resultsSection.style.display = 'none';
}

function hideLoading() {
    loading.style.display = 'none';
    submitBtn.disabled = false;
}

function showError(message) {
    errorText.textContent = message;
    errorMessage.style.display = 'flex';
    
    // Auto-hide após 5 segundos
    setTimeout(() => {
        hideError();
    }, 5000);
}

function hideError() {
    errorMessage.style.display = 'none';
}
```

Salve: `Ctrl + S`

---

## 📧 PARTE 6: EMAILS DE EXEMPLO

### Passo 17: exemplos/email_produtivo_suporte.txt

Abra `exemplos/email_produtivo_suporte.txt` e cole:
```
Assunto: Erro ao acessar o sistema

Prezados,

Estou com um problema urgente para reportar. Desde ontem pela manhã, não consigo acessar o sistema financeiro. 

Quando tento fazer login, recebo a seguinte mensagem de erro:
"Erro 500 - Internal Server Error"

Já tentei:
- Limpar o cache do navegador
- Usar outro navegador
- Reiniciar meu computador

O problema persiste. Este acesso é crítico para minhas atividades diárias e preciso de ajuda o mais rápido possível.

Meu usuário: Ailton.silva@empresa.com.br
Horário do primeiro erro: 15/01/2025 às 09:30

Agradeço a atenção,

Ailton Silva
Departamento Financeiro
```

Salve: `Ctrl + S`

---

### Passo 18: exemplos/email_produtivo_status.txt

Abra `exemplos/email_produtivo_status.txt` e cole:
```
Assunto: Atualização sobre requisição #2845

Boa tarde,

Gostaria de solicitar uma atualização sobre o status da requisição #2845, aberta em 10/01/2025.

A requisição é referente à solicitação de acesso ao módulo de relatórios avançados para nossa equipe.

Pontos que gostaria de esclarecer:
1. Qual o status atual da aprovação?
2. Há alguma documentação adicional necessária?
3. Qual a previsão para conclusão do processo?

Esta funcionalidade é importante para entregarmos o relatório trimestral dentro do prazo, que vence em 25/01/2025.

Fico no aguardo do retorno.

Atenciosamente,

Ailton
Gerente de Análise de Dados
Tel: (21) 99954-0432
```

Salve: `Ctrl + S`

---

### Passo 19: exemplos/email_improdutivo_felicitacao.txt

Abra `exemplos/email_improdutivo_felicitacao.txt` e cole:
```
Assunto: Feliz Natal e Próspero Ano Novo! 🎄

Querida equipe,

Espero que todos estejam bem!

Quero aproveitar esta mensagem para desejar a cada um de vocês um Feliz Natal repleto de alegria, paz e amor ao lado de seus entes queridos.

Foi um ano de muito trabalho e conquistas, e isso só foi possível graças ao esforço e dedicação de todos. Vocês são incríveis!

Que 2025 traga muitas realizações, saúde e felicidade para todos nós.

Nos vemos ano que vem com energia renovada!

Um grande abraço,

Ailton
Coordenador de Equipe
```

Salve: `Ctrl + S`

---

### Passo 20: exemplos/email_improdutivo_agradecimento.txt

Abra `exemplos/email_improdutivo_agradecimento.txt` e cole:
```
Assunto: Muito obrigado pelo apoio!

Olá time,

Só passei para agradecer imensamente o apoio de todos durante o projeto do último trimestre.

Foi realmente inspirador trabalhar com uma equipe tão dedicada e colaborativa. Cada um de vocês fez a diferença!

O sucesso que alcançamos é fruto do trabalho em equipe e do comprometimento de todos.

Muito obrigado mesmo! Vocês são demais! 🙌

Abraços,

Ailton