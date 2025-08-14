import requests
import time
import threading
from datetime import datetime
import logging
from flask import Flask, jsonify
import os

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuração dos sites
SITES_CONFIG = [
    {
        "name": "instamoda",
        "base_url": "https://instamoda.org",
        "login_url": "https://instamoda.org/login",
        "send_follower_url": "https://instamoda.org/tools/send-follower",
        "login_data": {
            "username": "",  # Será preenchido dinamicamente
            "password": ""   # Será preenchido dinamicamente
        }
    },
    {
        "name": "fastfollow",
        "base_url": "https://fastfollow.in",
        "login_url": "https://fastfollow.in/member",
        "send_follower_url": "https://fastfollow.in/tools/send-follower",
        "login_data": {
            "username": "",
            "password": ""
        }
    },
    {
        "name": "takipcikrali",
        "base_url": "https://takipcikrali.com",
        "login_url": "https://takipcikrali.com/login",
        "send_follower_url": "https://takipcikrali.com/tools/send-follower",
        "login_data": {
            "username": "",
            "password": ""
        }
    },
    {
        "name": "birtakipci",
        "base_url": "https://birtakipci.com",
        "login_url": "https://birtakipci.com/member",
        "send_follower_url": "https://birtakipci.com/tools/send-follower",
        "login_data": {
            "username": "",
            "password": ""
        }
    },
    {
        "name": "takipcitime",
        "base_url": "https://takipcitime.com",
        "login_url": "https://takipcitime.com/login",
        "send_follower_url": "https://takipcitime.com/tools/send-follower",
        "login_data": {
            "username": "",
            "password": ""
        }
    },
    {
        "name": "medyahizmeti",
        "base_url": "https://medyahizmeti.com",
        "login_url": "https://medyahizmeti.com/login",
        "send_follower_url": "https://medyahizmeti.com/tools/send-follower",
        "login_data": {
            "username": "",
            "password": ""
        }
    },
    {
        "name": "mixtakip",
        "base_url": "https://mixtakip.com",
        "login_url": "https://mixtakip.com/login",
        "send_follower_url": "https://mixtakip.com/tools/send-follower",
        "login_data": {
            "username": "",
            "password": ""
        }
    },
    {
        "name": "takipciking_net",
        "base_url": "https://takipciking.net",
        "login_url": "https://takipciking.net/login",
        "send_follower_url": "https://takipciking.net/tools/send-follower",
        "login_data": {
            "username": "",
            "password": ""
        }
    },
    {
        "name": "takipcigir",
        "base_url": "https://takipcigir.com",
        "login_url": "https://takipcigir.com/login",
        "send_follower_url": "https://takipcigir.com/tools/send-follower",
        "login_data": {
            "username": "",
            "password": ""
        }
    },
    {
        "name": "canlitakipci",
        "base_url": "https://canlitakipci.com",
        "login_url": "https://canlitakipci.com/login",
        "send_follower_url": "https://canlitakipci.com/tools/send-follower",
        "login_data": {
            "username": "",
            "password": ""
        }
    },
    {
        "name": "takipcimax",
        "base_url": "https://takipcimax.com",
        "login_url": "https://takipcimax.com/login",
        "send_follower_url": "https://takipcimax.com/tools/send-follower",
        "login_data": {
            "username": "",
            "password": ""
        }
    },
    {
        "name": "takipciking_com",
        "base_url": "https://www.takipciking.com",
        "login_url": "https://www.takipciking.com/login",
        "send_follower_url": "https://www.takipciking.com/tools/send-follower",
        "login_data": {
            "username": "",
            "password": ""
        }
    },
    {
        "name": "takipcizen",
        "base_url": "https://takipcizen.com",
        "login_url": "https://takipcizen.com/login",
        "send_follower_url": "https://takipcizen.com/tools/send-follower/6887835530",
        "login_data": {
            "username": "",
            "password": ""
        }
    },
    {
        "name": "takipcivar",
        "base_url": "https://takipcivar.net",
        "login_url": "https://takipcivar.net/login",
        "send_follower_url": "https://takipcivar.net/tools/send-follower",
        "login_data": {
            "username": "",
            "password": ""
        }
    },
    {
        "name": "hepsitakipci",
        "base_url": "https://www.hepsitakipci.com",
        "login_url": "https://www.hepsitakipci.com/login",
        "send_follower_url": "https://www.hepsitakipci.com/tools/send-follower",
        "login_data": {
            "username": "",
            "password": ""
        }
    }
]

class MultiSiteAutomation:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.stats = {
            'cycles_completed': 0,
            'total_successes': 0,
            'total_failures': 0,
            'last_cycle_time': None,
            'next_cycle_time': None
        }

    def login_to_site(self, site_config):
        """Faz login em um site específico"""
        try:
            logger.info(f"[{site_config['name']}] Iniciando processo de login...")
            
            # Primeiro, obter a página de login para capturar tokens CSRF se necessário
            response = self.session.get(site_config['login_url'], timeout=30)
            response.raise_for_status()
            
            # Preparar dados de login
            login_data = {
                'username': self.username,
                'password': self.password
            }
            
            # Fazer login
            login_response = self.session.post(
                site_config['login_url'], 
                data=login_data, 
                timeout=30,
                allow_redirects=True
            )
            
            # Verificar se o login foi bem-sucedido
            if login_response.status_code == 200:
                # Verificar se não há mensagens de erro na resposta
                if 'error' not in login_response.text.lower() and 'wrong' not in login_response.text.lower():
                    logger.info(f"[{site_config['name']}] Login realizado com sucesso!")
                    return True
                else:
                    logger.warning(f"[{site_config['name']}] Login pode ter falhado - verificar credenciais")
                    return False
            else:
                logger.error(f"[{site_config['name']}] Falha no login - Status: {login_response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"[{site_config['name']}] Erro durante o login: {str(e)}")
            return False

    def send_followers_to_site(self, site_config, target_username, follower_count):
        """Envia seguidores em um site específico"""
        try:
            logger.info(f"[{site_config['name']}] Iniciando envio de {follower_count} seguidores para {target_username}...")
            
            # Acessar a página de envio de seguidores
            response = self.session.get(site_config['send_follower_url'], timeout=30)
            response.raise_for_status()
            
            # Preparar dados para envio de seguidores
            follower_data = {
                'target_username': target_username,
                'username': target_username,
                'follower_count': str(follower_count),
                'count': str(follower_count)
            }
            
            # Enviar requisição para adicionar seguidores
            send_response = self.session.post(
                site_config['send_follower_url'],
                data=follower_data,
                timeout=30,
                allow_redirects=True
            )
            
            if send_response.status_code == 200:
                logger.info(f"[{site_config['name']}] Envio de seguidores iniciado com sucesso!")
                return True
            else:
                logger.error(f"[{site_config['name']}] Falha no envio - Status: {send_response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"[{site_config['name']}] Erro durante o envio de seguidores: {str(e)}")
            return False

    def process_site(self, site_config, target_username, follower_count):
        """Processa um site completo (login + envio)"""
        try:
            logger.info(f"\n=== PROCESSANDO SITE: {site_config['name'].upper()} ===")
            
            # Fazer login
            login_success = self.login_to_site(site_config)
            if not login_success:
                logger.warning(f"[{site_config['name']}] Falha no login, pulando para o próximo site...")
                return False
            
            # Enviar seguidores
            send_success = self.send_followers_to_site(site_config, target_username, follower_count)
            if not send_success:
                logger.warning(f"[{site_config['name']}] Falha no envio, mas continuando...")
            
            logger.info(f"[{site_config['name']}] Processamento concluído!")
            return send_success
            
        except Exception as e:
            logger.error(f"[{site_config['name']}] Erro geral: {str(e)}")
            return False

    def execute_full_cycle(self, target_username, follower_count=500):
        """Executa um ciclo completo em todos os sites"""
        start_time = time.time()
        logger.info("\n=== INICIANDO CICLO COMPLETO DE AUTOMAÇÃO MULTI-SITE ===")
        logger.info(f"Alvo: {target_username}")
        logger.info(f"Seguidores por site: {follower_count}")
        logger.info(f"Total de sites: {len(SITES_CONFIG)}")
        logger.info(f"Horário de início: {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}")

        success_count = 0
        fail_count = 0

        for i, site_config in enumerate(SITES_CONFIG):
            try:
                success = self.process_site(site_config, target_username, follower_count)
                if success:
                    success_count += 1
                else:
                    fail_count += 1
            except Exception as e:
                logger.error(f"Erro crítico no site {site_config['name']}: {str(e)}")
                fail_count += 1

            # Aguardar 3 segundos entre sites (exceto no último)
            if i < len(SITES_CONFIG) - 1:
                logger.info(f"\nAguardando 3 segundos antes do próximo site...")
                time.sleep(3)

        end_time = time.time()
        duration = int(end_time - start_time)

        logger.info("\n=== CICLO COMPLETO FINALIZADO ===")
        logger.info(f"Sites processados com sucesso: {success_count}")
        logger.info(f"Sites com falha: {fail_count}")
        logger.info(f"Duração total: {duration} segundos")
        logger.info(f"Horário de término: {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}")

        # Atualizar estatísticas
        self.stats['cycles_completed'] += 1
        self.stats['total_successes'] += success_count
        self.stats['total_failures'] += fail_count
        self.stats['last_cycle_time'] = datetime.now().strftime('%d/%m/%Y, %H:%M:%S')

        return {'success_count': success_count, 'fail_count': fail_count, 'duration': duration}

    def start_infinite_loop(self, target_username, follower_count=500):
        """Inicia o loop infinito de automação"""
        logger.info("\n=== INICIANDO LOOP INFINITO DE AUTOMAÇÃO ===")
        logger.info("Configuração:")
        logger.info(f"- Usuário alvo: {target_username}")
        logger.info(f"- Seguidores por site: {follower_count}")
        logger.info(f"- Intervalo entre ciclos: 1 hora e 30 minutos (5400 segundos)")
        logger.info(f"- Sites por ciclo: {len(SITES_CONFIG)}")

        cycle_count = 0

        while True:
            cycle_count += 1
            logger.info(f"\n\n🔄 INICIANDO CICLO #{cycle_count} - {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}")

            try:
                result = self.execute_full_cycle(target_username, follower_count)
                
                logger.info(f"\n✅ CICLO #{cycle_count} CONCLUÍDO:")
                logger.info(f"   - Sucessos: {result['success_count']}/{len(SITES_CONFIG)}")
                logger.info(f"   - Falhas: {result['fail_count']}/{len(SITES_CONFIG)}")
                logger.info(f"   - Duração: {result['duration']}s")

            except Exception as e:
                logger.error(f"\n❌ ERRO NO CICLO #{cycle_count}: {str(e)}")

            # Aguardar 1 hora e 30 minutos (5400 segundos) antes do próximo ciclo
            wait_time = 5400  # 1.5 horas em segundos
            next_cycle_time = datetime.fromtimestamp(time.time() + wait_time)
            self.stats['next_cycle_time'] = next_cycle_time.strftime('%d/%m/%Y, %H:%M:%S')
            
            logger.info(f"\n⏰ Aguardando {wait_time//60} minutos até o próximo ciclo...")
            logger.info(f"   Próximo ciclo será às: {next_cycle_time.strftime('%d/%m/%Y, %H:%M:%S')}")
            
            time.sleep(wait_time)

# Configuração do Flask para o Render
app = Flask(__name__)

# Configurações do usuário
USERNAME = 'Luisa_sfd11'
PASSWORD = 'LUANLEVY17'
TARGET_USERNAME = 'comedor_di_primas'
FOLLOWER_COUNT = 500

# Instância global da automação
automation = None

@app.route('/')
def home():
    """Página inicial com status da automação"""
    return jsonify({
        'status': 'running',
        'message': 'Automação Multi-Site de Seguidores Instagram',
        'config': {
            'username': USERNAME,
            'target_username': TARGET_USERNAME,
            'follower_count': FOLLOWER_COUNT,
            'total_sites': len(SITES_CONFIG),
            'delay_between_sites': '3 segundos',
            'cycle_interval': '1 hora e 30 minutos'
        },
        'stats': automation.stats if automation else {}
    })

@app.route('/status')
def status():
    """Endpoint para verificar status da automação"""
    return jsonify({
        'automation_running': automation is not None,
        'stats': automation.stats if automation else {},
        'sites_count': len(SITES_CONFIG)
    })

@app.route('/health')
def health():
    """Health check para o Render"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

def start_automation():
    """Inicia a automação em uma thread separada"""
    global automation
    automation = MultiSiteAutomation(USERNAME, PASSWORD)
    automation.start_infinite_loop(TARGET_USERNAME, FOLLOWER_COUNT)

if __name__ == '__main__':
    # Iniciar automação em thread separada
    automation_thread = threading.Thread(target=start_automation, daemon=True)
    automation_thread.start()
    
    # Iniciar servidor Flask
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

