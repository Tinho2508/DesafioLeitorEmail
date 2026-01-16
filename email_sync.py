"""
Sistema de Sincronização Automática de Emails
Suporta: Gmail API e IMAP (Gmail, Outlook, Yahoo, etc.)
"""

import imaplib
import email
from email.header import decode_header
import time
import requests
import json
from datetime import datetime
import os

# ===============================================
# CONFIGURAÇÕES
# ===============================================

class EmailConfig:
    """Configurações de email"""
    
    # IMAP - Funciona com Gmail, Outlook, Yahoo, etc.
    IMAP_ENABLED = True
    IMAP_SERVER = "imap.gmail.com"  # Gmail
    # IMAP_SERVER = "outlook.office365.com"  # Outlook
    # IMAP_SERVER = "imap.mail.yahoo.com"  # Yahoo
    
    IMAP_PORT = 993
    EMAIL_ADDRESS = "seu-email@gmail.com"  # ALTERE AQUI
    EMAIL_PASSWORD = "sua-senha-app"  # ALTERE AQUI (senha de app, não senha normal)
    
    # Gmail API - Mais seguro, recomendado para Gmail
    GMAIL_API_ENABLED = False  # Deixe False por enquanto (requer configuração OAuth)
    
    # Configurações de sincronização
    CHECK_INTERVAL = 60  # Verificar emails a cada 60 segundos
    AUTO_CLASSIFY = True  # Classificar automaticamente
    AUTO_RESPOND = False  # Responder automaticamente (cuidado!)
    MARK_AS_READ = False  # Marcar como lido após processar
    
    # URL do classificador (quando estiver rodando)
    CLASSIFIER_URL = "http://localhost:5000/classify"


# ===============================================
# CLASSE PRINCIPAL DE SINCRONIZAÇÃO
# ===============================================

class EmailSynchronizer:
    """Sincroniza emails usando IMAP ou Gmail API"""
    
    def __init__(self, config):
        self.config = config
        self.mail = None
        self.processed_emails = set()  # IDs já processados
        
    def connect_imap(self):
        """Conecta ao servidor IMAP"""
        try:
            print(f"🔌 Conectando ao servidor IMAP: {self.config.IMAP_SERVER}...")
            
            # Conectar com SSL
            self.mail = imaplib.IMAP4_SSL(
                self.config.IMAP_SERVER,
                self.config.IMAP_PORT
            )
            
            # Login
            self.mail.login(
                self.config.EMAIL_ADDRESS,
                self.config.EMAIL_PASSWORD
            )
            
            print("✅ Conectado com sucesso!")
            return True
            
        except imaplib.IMAP4.error as e:
            print(f"❌ Erro de autenticação: {e}")
            print("\n💡 DICA: Para Gmail, use 'Senha de App':")
            print("   1. Acesse: https://myaccount.google.com/security")
            print("   2. Ative verificação em 2 etapas")
            print("   3. Gere uma 'Senha de app' para 'Email'")
            return False
            
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            return False
    
    def get_unread_emails(self):
        """Busca emails não lidos"""
        try:
            # Selecionar caixa de entrada
            self.mail.select('inbox')
            
            # Buscar emails não lidos
            status, messages = self.mail.search(None, 'UNSEEN')
            
            if status != 'OK':
                print("❌ Erro ao buscar emails")
                return []
            
            email_ids = messages[0].split()
            
            if not email_ids:
                return []
            
            print(f"📬 {len(email_ids)} emails não lidos encontrados")
            
            emails = []
            for email_id in email_ids:
                email_data = self.fetch_email(email_id)
                if email_data:
                    emails.append(email_data)
            
            return emails
            
        except Exception as e:
            print(f"❌ Erro ao buscar emails: {e}")
            return []
    
    def fetch_email(self, email_id):
        """Busca detalhes de um email específico"""
        try:
            # Buscar email
            status, msg_data = self.mail.fetch(email_id, '(RFC822)')
            
            if status != 'OK':
                return None
            
            # Parse do email
            email_message = email.message_from_bytes(msg_data[0][1])
            
            # Extrair informações
            subject = self.decode_subject(email_message.get('Subject', ''))
            from_email = email_message.get('From', '')
            date = email_message.get('Date', '')
            
            # Extrair corpo do email
            body = self.get_email_body(email_message)
            
            email_data = {
                'id': email_id.decode(),
                'subject': subject,
                'from': from_email,
                'date': date,
                'body': body,
                'full_text': f"Assunto: {subject}\n\nDe: {from_email}\n\n{body}"
            }
            
            return email_data
            
        except Exception as e:
            print(f"❌ Erro ao processar email {email_id}: {e}")
            return None
    
    def decode_subject(self, subject):
        """Decodifica assunto do email"""
        if not subject:
            return "(Sem assunto)"
        
        try:
            decoded = decode_header(subject)[0]
            if isinstance(decoded[0], bytes):
                return decoded[0].decode(decoded[1] or 'utf-8')
            return decoded[0]
        except:
            return subject
    
    def get_email_body(self, email_message):
        """Extrai corpo do email"""
        body = ""
        
        try:
            if email_message.is_multipart():
                # Email com múltiplas partes
                for part in email_message.walk():
                    content_type = part.get_content_type()
                    
                    if content_type == "text/plain":
                        try:
                            payload = part.get_payload(decode=True)
                            if payload:
                                body = payload.decode('utf-8', errors='ignore')
                                break
                        except:
                            continue
            else:
                # Email simples
                payload = email_message.get_payload(decode=True)
                if payload:
                    body = payload.decode('utf-8', errors='ignore')
            
            return body.strip()
            
        except Exception as e:
            print(f"⚠️  Erro ao extrair corpo: {e}")
            return "(Não foi possível extrair o conteúdo)"
    
    def classify_email(self, email_data):
        """Classifica email usando o sistema de IA"""
        try:
            print(f"\n🤖 Classificando: '{email_data['subject']}'...")
            
            # Preparar dados para envio
            data = {'email_text': email_data['full_text']}
            
            # Enviar para classificador
            response = requests.post(
                self.config.CLASSIFIER_URL,
                data=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"   ✅ Categoria: {result['category']}")
                print(f"   📊 Confiança: {result['confidence']}%")
                print(f"   📝 Resposta sugerida:")
                print(f"      {result['suggested_response'][:100]}...")
                
                return result
            else:
                print(f"   ❌ Erro: {response.status_code}")
                return None
                
        except requests.exceptions.ConnectionError:
            print("   ⚠️  Classificador não está rodando!")
            print("   💡 Execute: python app.py")
            return None
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return None
    
    def mark_as_read(self, email_id):
        """Marca email como lido"""
        try:
            self.mail.store(email_id, '+FLAGS', '\\Seen')
        except Exception as e:
            print(f"⚠️  Erro ao marcar como lido: {e}")
    
    def send_response(self, email_data, response_text):
        """
        Envia resposta automática (CUIDADO!)
        Desabilitado por padrão para segurança
        """
        print("⚠️  Envio automático desabilitado (configuração de segurança)")
        print("💡 Para habilitar, implemente SMTP no código")
        
        # TODO: Implementar SMTP para envio
        # import smtplib
        # ...
    
    def save_classification_log(self, email_data, classification):
        """Salva log das classificações"""
        log_file = 'email_classifications.json'
        
        try:
            # Carregar logs existentes
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            # Adicionar novo log
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'email_id': email_data['id'],
                'subject': email_data['subject'],
                'from': email_data['from'],
                'category': classification.get('category'),
                'confidence': classification.get('confidence'),
                'response': classification.get('suggested_response')
            }
            
            logs.append(log_entry)
            
            # Salvar
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
            
            print(f"   💾 Log salvo em {log_file}")
            
        except Exception as e:
            print(f"   ⚠️  Erro ao salvar log: {e}")
    
    def process_emails(self):
        """Processa emails não lidos"""
        emails = self.get_unread_emails()
        
        if not emails:
            print("📭 Nenhum email novo")
            return
        
        print(f"\n{'='*60}")
        print(f"📨 PROCESSANDO {len(emails)} EMAILS")
        print(f"{'='*60}")
        
        for i, email_data in enumerate(emails, 1):
            # Verificar se já foi processado
            if email_data['id'] in self.processed_emails:
                continue
            
            print(f"\n📧 Email {i}/{len(emails)}")
            print(f"   De: {email_data['from']}")
            print(f"   Assunto: {email_data['subject']}")
            print(f"   Data: {email_data['date']}")
            
            # Classificar
            if self.config.AUTO_CLASSIFY:
                classification = self.classify_email(email_data)
                
                if classification:
                    # Salvar log
                    self.save_classification_log(email_data, classification)
                    
                    # Responder automaticamente (se habilitado)
                    if self.config.AUTO_RESPOND:
                        self.send_response(email_data, classification['suggested_response'])
            
            # Marcar como lido (se habilitado)
            if self.config.MARK_AS_READ:
                self.mark_as_read(email_data['id'].encode())
            
            # Marcar como processado
            self.processed_emails.add(email_data['id'])
            
            print(f"   ✅ Processado")
        
        print(f"\n{'='*60}\n")
    
    def run_continuous(self):
        """Executa sincronização contínua"""
        print(f"\n🚀 INICIANDO SINCRONIZAÇÃO DE EMAILS")
        print(f"{'='*60}")
        print(f"📧 Email: {self.config.EMAIL_ADDRESS}")
        print(f"🔄 Intervalo: {self.config.CHECK_INTERVAL}s")
        print(f"🤖 Auto-classificar: {self.config.AUTO_CLASSIFY}")
        print(f"📤 Auto-responder: {self.config.AUTO_RESPOND}")
        print(f"{'='*60}\n")
        
        # Conectar
        if not self.connect_imap():
            return
        
        print("✅ Sistema iniciado! Pressione Ctrl+C para parar\n")
        
        try:
            while True:
                try:
                    print(f"🔍 Verificando emails... [{datetime.now().strftime('%H:%M:%S')}]")
                    self.process_emails()
                    
                except imaplib.IMAP4.abort:
                    print("⚠️  Conexão perdida. Reconectando...")
                    time.sleep(5)
                    if not self.connect_imap():
                        break
                
                except Exception as e:
                    print(f"❌ Erro: {e}")
                
                # Aguardar próxima verificação
                time.sleep(self.config.CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            print("\n\n👋 Encerrando sincronização...")
            self.disconnect()
    
    def disconnect(self):
        """Desconecta do servidor"""
        try:
            if self.mail:
                self.mail.logout()
                print("✅ Desconectado com sucesso")
        except:
            pass


# ===============================================
# EXECUÇÃO
# ===============================================

def main():
    """Função principal"""
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     📧 SINCRONIZADOR AUTOMÁTICO DE EMAILS COM IA 🤖      ║
║                                                          ║
║   Classifica automaticamente emails usando IA           ║
║   Suporta: Gmail, Outlook, Yahoo e outros via IMAP      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Verificar configurações
    config = EmailConfig()
    
    if config.EMAIL_ADDRESS == "seu-email@gmail.com":
        print("⚠️  CONFIGURAÇÃO NECESSÁRIA!")
        print("\n📝 Edite o arquivo email_sync.py e configure:")
        print("   1. EMAIL_ADDRESS = 'seu-email@gmail.com'")
        print("   2. EMAIL_PASSWORD = 'sua-senha-de-app'")
        print("\n💡 Para Gmail, gere uma senha de app em:")
        print("   https://myaccount.google.com/security")
        print("\n   Ative verificação em 2 etapas → Senhas de app → Email")
        return
    
    # Criar sincronizador
    sync = EmailSynchronizer(config)
    
    # Executar
    sync.run_continuous()


if __name__ == "__main__":
    main()