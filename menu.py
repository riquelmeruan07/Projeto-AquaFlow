from time import sleep
import auth
import login
import dados
import sys
import modoadm
import valida
import compras
import bonificacoes
import rankings
import entregas
import json
def MenuInicial(): #Menu inicial
    opcao = ''
    while opcao != '3':
        valida.limpaTerminal()
        print('\033[1;34m--- AquaFlow ---\033[m')
        print('1 - Cadastro')
        print('2- Login')
        print('3 - Sair do programa')
        
        opcao = input('Escolha uma opção: ').strip()
        if opcao == '1':
            auth.cadastrar()
        elif opcao == '2':
            login.login()
        elif opcao == '3':
            print('Encerrando programa...')
            sleep(1)
            break
        else:
            print('\033[1;31mA opção é inválida.\033[m')
            sleep(1)
            
def menu_admin(email_logado): #Menu Administrativo
    while True:
        valida.limpaTerminal()
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
            modoadm.DeletarEntregas(email_logado)
        elif opcao == '4':
            modoadm.DeletarCompras(email_logado)
        elif opcao == "5":
            print("Saindo do modo ADM...")
            sleep(1)
            sys.exit()
        else:
            print("Opção inválida!")
            sleep(1)

def ConfiguracoesAdmin(email_logado): #Configurações Adm
    opcao = ''
    while opcao != '4':
        valida.limpaTerminal()
        print('\033[1;34m---Configurações---\033[m')
        print('1 - Ver dados')
        print('2- Atualizar Dados')
        print('3 - Deletar Conta')
        print('4 - Retornar ao Menu principal')
        
        opcao = input('Escolha uma opção: ').strip()
        if opcao == '1':
            modoadm.MostrarDados(email_logado)
        elif opcao == '2':
            modoadm.AtualizarDados(email_logado)
        elif opcao == '3':
            modoadm.DeletarContaAdmin(email_logado)
        elif opcao == '4':
            print('Retornando ao Menu principal...')
            sleep(1)
            menu_admin(email_logado)
            break
        else:
            print('\033[1;31mA opção é inválida.\033[m')
            sleep(1)

def Estoque(email_logado):# Menu de estoque do adm
    opcao = ''
    while opcao != '3':
        valida.limpaTerminal()
        print('\033[1;34m---Menu estoque---\033[m')
        print('1 - Adicionar produto')
        print('2 - Editar produto')
        print('3 - Deletar produto')
        print('4 - Retornar ao menu principal')
                
        opcao = input('Escolha uma opção: ')
        if opcao == '1':
            modoadm.AddEstoque(email_logado)
        if opcao == '2':
            modoadm.EditaEstoque(email_logado)
        if opcao == '3':
            modoadm.DeletarProduto(email_logado)
        if opcao == '4': 
            print('Retornando ao Menu principal...')
            sleep(1)
            menu_admin(email_logado)
            break
def MenuPrincipal(email_logado): #Menu principal dos clientes
    opcao = ''
    while opcao != '4':
        valida.limpaTerminal()
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
            rankings.Rankings(email_logado)
        elif opcao == '4':
            bonificacoes.HistoricoBonificacoesCliente(email_logado)
        elif opcao == '5':
            print('\033[1;36mFechando programa...\033[m')
            sleep(1)
            sys.exit()
        else:
            print('\033[1;31mA opção é inválida.\033[m')
            sleep(1)
def MenuPrincipalEntregador(email_logado): #Menu principal dos entregadores
    opcao = ''
    while opcao != '5':
        valida.limpaTerminal()
        print('\033[1;34m--- Menu principal ---\033[m')
        print('1 - Configurações')
        print('2- Entregas')
        print('3 - Rankings')
        print('4 - Bonificações ')
        print('5 - Fechar programa')
        
        opcao = input('Escolha uma opção: ').strip()
        if opcao == '1':
            configuracoes(email_logado)
        elif opcao == '2':
            MenuEntregas(email_logado)
        elif opcao == '3':
            rankings.RankingEntregadores(email_logado)
        elif opcao == '4':
            bonificacoes.HistoricoBonificacoesEntregador(email_logado)
        elif opcao == '5':
            print('Fechando programa...')
            sleep(1)
            sys.exit()
        else:
            print('\033[1;31mA opção é inválida.\033[m')
            sleep(1)
def MenuEntregas(email_logado): #Menu de Entregas 
    opcao = ''
    while opcao != '3':
        valida.limpaTerminal()
        print('\033[1;34m---Entregas---\033[m')
        print('1 - Registrar Entrega')
        print('2- Histórico de Entregas')
        print('3 - Retornar ao Menu principal')
        
        opcao = input('Escolha uma opção: ').strip()
        if opcao == '1':
            entregas.RegistraEntrega(email_logado)
        elif opcao == '2':
            entregas.HistoricoEntregas(email_logado)
        elif opcao == '3':
            print('Retornando ao Menu principal...')
            sleep(1)
            MenuPrincipalEntregador(email_logado)
            break
        else:
            print('\033[1;31mA opção é inválida.\033[m')
            sleep(1)
def configuracoes(email_logado): #Configurações para os clientes e entregadores
    with open('nome.json', 'r', encoding='utf-8') as arq:
        dados_json = json.load(arq)
        info = dados_json.get(email_logado, {})
        status_usuario = info.get('Status', 'Cliente')
            
    opcao = ''
    while opcao != '4':
        valida.limpaTerminal()
        print('\033[1;34m---Configurações---\033[m')
        print('1 - Ver dados')
        print('2- Atualizar Dados')
        print('3 - Deletar Conta')
        print('4 - Retornar ao Menu principal')
        
        opcao = input('Escolha uma opção: ').strip()
        if opcao == '1':
            dados.MostraDados(email_logado)
        elif opcao == '2':
            dados.AtualizarDados(email_logado)
        elif opcao == '3':
            dados.DeletarConta(email_logado)
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
    opcao = ''
    while opcao != '3':
        valida.limpaTerminal()
        print('\033[1;34m---Compras---\033[m')
        print('1 - Registrar Compra')
        print('2- Histórico de Compras')
        print('3 - Retornar ao Menu principal')
        
        opcao = input('Escolha uma opção: ').strip()
        if opcao == '1':
            compras.RegistraCompra(email_logado)
        elif opcao == '2':
            compras.HistoricoCompras(email_logado)
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
