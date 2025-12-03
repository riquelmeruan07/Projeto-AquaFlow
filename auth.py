import json
import os
from time import sleep
from valida import Validador

class Cadastro:
    def __init__(self, arquivo_usuarios='nome.json'):
        self.arquivo_usuarios = arquivo_usuarios

    def carregar_dados(self):
        """Carrega o JSON de usuários ou cria dict vazio se não existir."""
        if os.path.exists(self.arquivo_usuarios):
            with open(self.arquivo_usuarios, 'r', encoding='utf-8') as arquivo:
                try:
                    return json.load(arquivo)
                except json.JSONDecodeError:
                    return {}
        return {}

    def salvar_dados(self, dados):
        """Salva o dicionário de usuários no JSON."""
        with open(self.arquivo_usuarios, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

    def cadastrar(self):
        """Fluxo de cadastro do usuário (cliente ou entregador)."""
        dados = self.carregar_dados()
        Validador.limpa_terminal()
        print('\033[1;34mCadastro do usuário\033[m')
        email = Validador.valida_email()
        
        if email in dados:
            print("\033[1;34mEmail já cadastrado no sistema.\033[m")
            sleep(2)
            return email, False

        
        nome = Validador.valida_nome()
        senha = Validador.valida_senha()
        status = Validador.valida_status()

        dados[email] = {
            "Nome": nome,
            "Senha": senha,
            "Status": status
        }

        self.salvar_dados(dados)

        print("\033[32mUsuário cadastrado com sucesso!\033[m")
        sleep(2)
        return email, True
