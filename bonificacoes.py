import json
import valida
import menu
import json
import valida

def HistoricoBonificacoesEntregador(email):
    #Função criada para o usuário verificar se possui alguma bonificação ou suas bonificações dos meses passados
    valida.limpaTerminal()
    with open('nome.json', 'r', encoding='utf-8') as arq:
        dados = json.load(arq)

    info = dados.get(email, {})

    print("\033[1;34m=== Histórico de Bonificações ===\033[m")
    bonificacoes = info.get("Bonificacoes", [])

    if bonificacoes:
        for b in bonificacoes:
            print(f"- {b}")
    else:
        print("Nenhuma bonificação registrada até o momento.")

    input("\nPressione Enter para voltar...")
    menu.MenuPrincipalEntregador(email)

def HistoricoBonificacoesCliente(email):
    #Função criada para o usuário verificar se possui alguma bonificação ou suas bonificações dos meses passados
    valida.limpaTerminal()

    with open('nome.json', 'r', encoding='utf-8') as arq:
        dados = json.load(arq)

    info = dados.get(email)
    print("\n\033[1;34m=== Histórico de Bonificações ===\033[m")
    print(f"Cliente: {info['Nome']}\n")

    bonificacoes = info.get("Bonificacoes", [])

    if not bonificacoes:
        print("\033[33mNenhuma bonificação recebida até o momento.\033[m")
    else:
        for i, bonus in enumerate(bonificacoes, start=1):
            print(f"{i}º - {bonus}")

    input("\nPressione Enter para voltar...")
    menu.MenuPrincipal(email)
