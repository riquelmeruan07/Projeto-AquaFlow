from time import sleep
import json
import sys
from valida import Validador

class GerenciadorConta:
    ARQUIVO_DADOS = 'nome.json'

    def __init__(self, email):
        """
        Gerencia a conta de um usuário específico.
        :param email: email do usuário logado
        """
        self.email = email
        self.dados = self._carregar_dados()

    def _carregar_dados(self):
        """Carrega o JSON de usuários."""
        with open(self.ARQUIVO_DADOS, 'r', encoding='utf-8') as arq:
            return json.load(arq)

    def _salvar_dados(self):
        """Salva o JSON de usuários."""
        with open(self.ARQUIVO_DADOS, 'w', encoding='utf-8') as arq:
            json.dump(self.dados, arq, ensure_ascii=False, indent=4)

    def mostrar_dados(self):
        """Mostra os dados básicos do usuário logado."""
        Validador.limpa_terminal()
        self.dados = self._carregar_dados()  # recarrega para garantir dados atualizados

        info = self.dados[self.email]
        status_usuario = info.get('Status', 'Cliente')

        print("\n\033[1;34m=== SEUS DADOS CADASTRADOS ===\033[m")
        print(f"Email: {self.email}")
        print(f"Nome: {info.get('Nome', '---')}")
        print(f"Senha: {info.get('Senha', '---')}")
        print(f"Status: {status_usuario}")

        deseja = input("\nDeseja atualizar algum desses dados? [s/n] ").strip().lower()
        while deseja not in ['s', 'n']:
            print('\033[1;31mA opção é inválida.\033[m')
            deseja = input('Digite apenas [s/n]: ').strip().lower()

        if deseja == 's':
            novo_email = self.atualizar_dados()
            # Se mudou o email, atualiza o atributo
            self.email = novo_email
            # Retorna o NOVO EMAIL e o TIPO de usuário, indicando que houve uma ação (True)
            return self.email, status_usuario, True 
        
        else:
            print('\033[33mVoltando ao menu principal...\033[m')
            sleep(1)
            # Retorna o EMAIL ATUAL e o TIPO de usuário, indicando que NÃO houve ação (False)
            return self.email, status_usuario, False

    def atualizar_dados(self):
        """
        Atualiza nome, senha, email ou todos.
        Retorna o email atual (que pode ter mudado).
        """
        Validador.limpa_terminal()
        self.dados = self._carregar_dados()

        print("\nO que deseja atualizar?")
        print("[1] Nome")
        print("[2] Senha")
        print("[3] Email")
        print("[4] Todos")
        
        opcao = input("Escolha: ").strip()
        while opcao not in ['1', '2', '3', '4']:
            print("\033[31mOpção inválida!\033[m")
            opcao = input("Digite 1, 2, 3 ou 4: ").strip()

        email_atual = self.email
        novo_email = email_atual

        # Atualizar Nome
        if opcao in ['1', '4']:
            novo_nome = Validador.valida_nome()
            if novo_nome:
                self.dados[email_atual]['Nome'] = novo_nome

        # Atualizar Senha
        if opcao in ['2', '4']:
            nova_senha = Validador.valida_senha()
            if nova_senha:
                self.dados[email_atual]['Senha'] = nova_senha

        # Atualizar Email (mudando a chave do dicionário)
        if opcao in ['3', '4']:
            novo_email = Validador.valida_email()
            if novo_email == email_atual:
                print("\033[33mO e-mail informado é igual ao atual. Nenhuma alteração feita.\033[m")
            else:
                # move os dados pra nova chave
                self.dados[novo_email] = self.dados[email_atual]
                del self.dados[email_atual]
                print("\033[32mE-mail alterado com sucesso!\033[m")

        # salva alterações
        self._salvar_dados()

        print("\033[32mDados atualizados com sucesso!\033[m")
        input("Pressione Enter para voltar...")

        return novo_email

    def deletar_conta(self):
        """Deleta a conta do usuário atual."""
        Validador.limpaTerminal()
        self.dados = self._carregar_dados()

        print("\033[33mAtenção! Você está prestes a deletar sua conta.\033[m")
        print("Todos os seus dados serão apagados permanentemente.\n")
        print('Confirme a sua senha abaixo')
        senha = Validador.valida_senha()

        if senha != self.dados[self.email]['Senha']:
            print("\033[31mSenha incorreta. Cancelando exclusão da conta.\033[m")
            sleep(2)
            return  # não muda o email

        confirma = input("Tem certeza que deseja deletar sua conta? [s/n]: ").strip().lower()
        while confirma not in ['s', 'n']:
            print("\033[1;31mOpção inválida.\033[m")
            confirma = input("Digite apenas [s/n]: ").strip().lower()

        if confirma == 's':
            del self.dados[self.email]
            self._salvar_dados()
            print("\033[32mConta deletada com sucesso!\033[m")
            sleep(2)
            sys.exit()  # encerra o programa
        else:
            print("Exclusão cancelada. Voltando ao menu...")
            sleep(1)
            return  # só volta
