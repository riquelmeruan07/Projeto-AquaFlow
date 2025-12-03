from time import sleep
from auth import Cadastro
from login import SistemaLogin
from dados import GerenciadorConta
import sys
import admin_usuarios
from valida import Validador
from compras import GerenciadorCompras
from bonificacoes import GerenciadorBonificacoes
from rankings import GerenciadorRanking
from entregas import Entregador
from admin_estoque import AdminEstoque
from admin_usuarios import AdminUsuarios
import json

def MenuInicial():  # Menu inicial
    cadastro = Cadastro()
    sistema_login = SistemaLogin()
    
    opcao = ''
    while opcao != '3':
        Validador.limpa_terminal()
        print('\033[1;34m--- AquaFlow ---\033[m')
        print('1 - Cadastro')
        print('2 - Login')
        print('3 - Sair do programa')
        
        opcao = input('Escolha uma opção: ').strip()
        
        if opcao == '1':
            email, criado_novo = cadastro.cadastrar()
            if not email:
                continue
            if not criado_novo:
                while True: 
                    escolha = input("Esse email já está cadastrado. Deseja ir para o login? [s/n] ").strip().lower()

                    if escolha == 's':
                        email_logado, tipo = sistema_login.login()
                        if email_logado:
                            if tipo == "admin":
                                menu_admin(email_logado)
                            elif tipo == "entregador":
                                MenuPrincipalEntregador(email_logado)
                            else:
                                MenuPrincipal(email_logado)
                        break 
                    
                    elif escolha == 'n':
                        print("Voltando ao menu inicial...")
                        sleep(1)
                    # Sai do loop interno e continua para o break que volta para o menu principal
                        break 
                    
                    else:
                    # Opção inválida, o loop volta a rodar (não há 'break' aqui)
                        print("\033[1;31mOpção inválida. Digite apenas [s/n].\033[m")
                        sleep(1)
                    
        elif opcao == '2':
            email_logado, tipo = sistema_login.login()
            if not email_logado:
                continue

            if tipo == "admin":
                menu_admin(email_logado)
            elif tipo == "entregador":
                MenuPrincipalEntregador(email_logado)
            else:
                MenuPrincipal(email_logado)
            

        elif opcao == '3':
            print('Encerrando programa...')
            sleep(1)
            break
        else:
            print('\033[1;31mA opção é inválida.\033[m')
            sleep(1)
            
def menu_admin(email_logado): #Menu Administrativo
    usuario = AdminUsuarios(email_logado)
    while True:
        Validador.limpa_terminal()
        print("\n--- MENU ADMINISTRATIVO ---")
        print('1- Estoque')
        print('2 - Configurações')
        print('3 - Deletar Entrega')
        print('4 - Deletar Compra')
        print("5 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            Estoque(email_logado)
        elif opcao == "2":
            ConfiguracoesAdmin(email_logado)
        elif opcao == '3':
            usuario.deletar_compras()
        elif opcao == '4':
            usuario.deletar_entregas
        elif opcao == "5":
            print("Saindo do modo ADM...")
            sleep(1)
            sys.exit()
        else:
            print("Opção inválida!")
            sleep(1)

def ConfiguracoesAdmin(email_logado): #Configurações Adm
    usuario = AdminUsuarios(email_logado)
    opcao = ''
    while opcao != '4':
        Validador.limpa_terminal()
        print('\033[1;34m---Configurações---\033[m')
        print('1 - Ver dados')
        print('2- Atualizar Dados')
        print('3 - Deletar Conta')
        print('4 - Retornar ao Menu principal')
        
        opcao = input('Escolha uma opção: ').strip()
        if opcao == '1':
            usuario.mostrar_dados()
        elif opcao == '2':
            usuario.atualizar_dados()
        elif opcao == '3':
            usuario.deletar_conta_admin()
        elif opcao == '4':
            print('Retornando ao Menu principal...')
            sleep(1)
            menu_admin(email_logado)
            break
        else:
            print('\033[1;31mA opção é inválida.\033[m')
            sleep(1)

def Estoque(email_logado):# Menu de estoque do adm
    estoque = AdminEstoque(email_logado)
    opcao = ''
    
    estoque.mostrar_alerta_estoque()
    while opcao != '4':
        Validador.limpa_terminal()
        print('\033[1;34m---Menu estoque---\033[m')
        print('1 - Adicionar produto')
        print('2 - Editar produto')
        print('3 - Deletar produto')
        print('4 - Retornar ao menu principal')
                
        opcao = input('Escolha uma opção: ')
        if opcao == '1':
            estoque.adicionar_produto()
        if opcao == '2':
            estoque.editar_produto()
        if opcao == '3':
            estoque.deletar_produto()
        if opcao == '4': 
            print('Retornando ao Menu principal...')
            sleep(1)
            menu_admin(email_logado)
            break
        
def MenuPrincipal(email_logado): #Menu principal dos clientes
    ranking = GerenciadorRanking(email_logado)
    bonifi = GerenciadorBonificacoes(email_logado)
    opcao = ''
    while opcao != '5':
        Validador.limpa_terminal()
        print('\033[1;34m--- Menu principal ---\033[m')
        print('1 - Configurações')
        print('2- Compras')
        print('3 - Rankings')
        print('4 - Bonificações')
        print('5 - Fechar programa')
        
        opcao = input('Escolha uma opção: ').strip()
        if opcao == '1':
            configuracoes(email_logado)
        elif opcao == '2':
            Compras(email_logado)
        elif opcao == '3':
            ranking.mostrar_ranking_clientes()
        elif opcao == '4':
            bonifi.mostrar_historico_cliente()
        elif opcao == '5':
            print('\033[1;36mFechando programa...\033[m')
            sleep(1)
            sys.exit()
        else:
            print('\033[1;31mA opção é inválida.\033[m')
            sleep(1)
            
def MenuPrincipalEntregador(email_logado): #Menu principal dos entregadores
    ranking = GerenciadorRanking(email_logado)
    bonifi = GerenciadorBonificacoes(email_logado)
    entrega = Entregador(email_logado)
    opcao = ''
    while opcao != '6':
        Validador.limpa_terminal()
        print('\033[1;34m--- Menu principal ---\033[m')
        print('1 - Configurações')
        print('2- Entregas')
        print('3 - Rankings')
        print('4 - Bonificações ')
        print('5 - Metas Diárias')
        print('6 - Fechar programa')
        
        opcao = input('Escolha uma opção: ').strip()
        if opcao == '1':
            configuracoes(email_logado)
        elif opcao == '2':
            MenuEntregas(email_logado)
        elif opcao == '3':
            ranking.mostrar_ranking_entregadores()
        elif opcao == '4':
            bonifi.mostrar_historico_entregador()
        elif opcao == '5':
            entrega.verificar_meta_diaria()
        elif opcao == '6':
            print('Fechando programa...')
            sleep(1)
            sys.exit()
        else:
            print('\033[1;31mA opção é inválida.\033[m')
            sleep(1)
            
def MenuEntregas(email_logado): #Menu de Entregas7
    entregador = Entregador(email_logado)
     
    opcao = ''
    while opcao != '3':
        Validador.limpa_terminal()
        print('\033[1;34m---Entregas---\033[m')
        print('1 - Registrar Entrega')
        print('2- Histórico de Entregas')
        print('3 - Retornar ao Menu principal')
        
        opcao = input('Escolha uma opção: ').strip()
        if opcao == '1':
            entregador.registrar_entrega()
        elif opcao == '2':
            entregador.historico_entregas()
        elif opcao == '3':
            print('Retornando ao Menu principal...')
            sleep(1)
            MenuPrincipalEntregador(email_logado)
            break
        else:
            print('\033[1;31mA opção é inválida.\033[m')
            sleep(1)
            
def configuracoes(email_logado): # Configurações para os clientes e entregadores
    # 1. CORREÇÃO: Crie uma INSTÂNCIA da classe GerenciadorConta.
    config = GerenciadorConta(email_logado) 
    
    # 2. Nota: A lógica de carregar o JSON para status_usuario pode ser movida
    # para a classe GerenciadorConta ou mantida aqui, mas a instância já tem o email.
    with open('nome.json', 'r', encoding='utf-8') as arq:
        dados_json = json.load(arq)
        info = dados_json.get(email_logado, {})
        status_usuario = info.get('Status', 'Cliente')
            
    opcao = ''
    while opcao != '4':
        Validador.limpa_terminal()
        print('\033[1;34m---Configurações---\033[m')
        print('1 - Ver dados')
        print('2 - Atualizar Dados')
        print('3 - Deletar Conta')
        print('4 - Retornar ao Menu principal')
        
        opcao = input('Escolha uma opção: ').strip()
        
        if opcao == '1':
            # 3. CORREÇÃO: Chame o método na INSTÂNCIA e não passe o email_logado.
            # Baseado na sua função mostrar_dados anterior:
            # (novo_email, status, atualizou) = config.mostrar_dados()
            
            # Se a função retornar o fluxo (como discutido anteriormente):
            email_atualizado, status_usuario, houve_atualizacao = config.mostrar_dados()
            
            # Se o email foi atualizado, atualize a variável local
            if houve_atualizacao:
                email_logado = email_atualizado
                # Se o email mudou, você precisa reiniciar o loop ou a função
                # para garantir que a instância da classe GerenciadorConta use o novo email.
                # Para simplificar, vamos quebrar o loop e deixar o menu_principal lidar com o fluxo
                break
        elif opcao == '2':
            config.atualizar_dados()
        elif opcao == '3':
            config.deletar_conta()
        elif opcao == '4':
            print('Retornando ao Menu principal...')
            sleep(1)
            if status_usuario == 'Entregador':
                MenuPrincipalEntregador(email_logado) 
            else:
                MenuPrincipal(email_logado)
                
            break
        else:
            print('\033[1;31mA opção é inválida.\033[m')
            sleep(1)
            
def Compras(email_logado): #Menu de compras
    
    compra = GerenciadorCompras(email_logado)
    opcao = ''
    while opcao != '3':
        Validador.limpa_terminal()
        print('\033[1;34m---Compras---\033[m')
        print('1 - Registrar Compra')
        print('2- Histórico de Compras')
        print('3 - Retornar ao Menu principal')
        
        opcao = input('Escolha uma opção: ').strip()
        if opcao == '1':
            compra.registrar_compra()
        elif opcao == '2':
            compra.historico_compras()
        elif opcao == '3':
            print('Retornando ao Menu principal...')
            sleep(1)
            MenuPrincipal(email_logado)
            break
        else:
            print('\033[1;31mA opção é inválida.\033[m')
            sleep(1)
            
if __name__ == "__main__":
    MenuInicial()
