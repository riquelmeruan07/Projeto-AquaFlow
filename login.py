import json
import valida
from time import sleep
import menu

ADMIN_EMAIL = "phdeoliveira14@gmail.com"
ADMIN_SENHA = "P97hol"

def login():
    #Login do usuário
    while True:
        valida.limpaTerminal()
        print('\033[1;34m--- Login do usuário ---\033[m')
        email = valida.validaemail()
        senha = valida.validasenha()

        with open('nome.json', 'r', encoding='utf-8') as arq:
            dados = json.load(arq)

        if email in dados:
            if dados[email]["Senha"] == senha:
                email_logado = email
                status_usuario = dados[email].get('Status', 'Cliente')
                print("\033[32mLogin realizado com sucesso!\033[m")
                sleep(1)

                # Verifica se é o administrador
                if email == ADMIN_EMAIL and senha == ADMIN_SENHA:
                    print("\033[33mModo Administrador ativado!\033[m")
                    sleep(1)
                    menu.menu_admin(email_logado)
                elif status_usuario.lower() == 'entregador':
                    print("\033[1;36mEncaminhando para o menu de Entregador...\033[m")
                    sleep(1)
                    menu.MenuPrincipalEntregador(email_logado)
                else:
                    print('\033[1;36mEncaminhando para o menu de Clientes\033[m')
                    sleep(1)
                    menu.MenuPrincipal(email_logado)
                return
            else:
                print("\033[31mEmail ou senha incorretos.\033[m")
                input("Pressione Enter para tentar novamente...")
        else:
            print("\033[31mEsse email não está no nosso banco de dados.\033[m")
            input("Pressione Enter para tentar novamente...")
