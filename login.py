import json
from time import sleep
from valida import Validador

class SistemaLogin:
    def __init__(
        self,
        arquivo_usuarios='nome.json',
        admin_email="phdeoliveira14@gmail.com",
        admin_senha="P97hol"
    ):
        self.arquivo_usuarios = arquivo_usuarios
        self.admin_email = admin_email
        self.admin_senha = admin_senha

    def carregar_usuarios(self):
        """Lê o arquivo JSON com os usuários cadastrados."""
        try:
            with open(self.arquivo_usuarios, 'r', encoding='utf-8') as arq:
                return json.load(arq)
        except FileNotFoundError:
            print("\033[31mArquivo de usuários não encontrado.\033[m")
            sleep(2)
            return {}
        except json.JSONDecodeError:
            print("\033[31mErro ao ler o arquivo de usuários (JSON inválido).\033[m")
            sleep(2)
            return {}

    def login(self):
        """Fluxo de login do usuário."""
        
        while True:
            Validador.limpa_terminal()
            print('\033[1;34m--- Login do usuário ---\033[m')
            email = Validador.valida_email()
            senha = Validador.valida_senha()

            with open('nome.json', 'r', encoding='utf-8') as arq:
                dados = json.load(arq)

            # Verifica admin primeiro
            if email == self.admin_email and senha == self.admin_senha:
                print("\033[32mLogin realizado com sucesso!\033[m")
                print("\033[33mModo Administrador ativado!\033[m")
                sleep(1)
                return email, "admin"

            # Agora verifica se é usuário normal
            if email in dados and dados[email]["Senha"] == senha:
                status_usuario = dados[email].get('Status', 'Cliente')

                print("\033[32mLogin realizado com sucesso!\033[m")
                sleep(1)

                if status_usuario.lower() == 'entregador':
                    print('\033[1;36mEncaminhando para o menu de Entregador...\033[m')
                    sleep(1)
                    return email, "entregador"
                else:
                    print('\033[1;36mEncaminhando para o menu de Clientes...\033[m')
                    sleep(1)
                    return email, "cliente"
            else:
                print("\033[31mEmail ou senha incorretos.\033[m")
                deseja = input("Deseja tentar novamente? [s/n]: ").strip().lower()
                if deseja != 's':
                    return None, None
