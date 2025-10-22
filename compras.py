import menu
import json
from time import sleep
import valida
from datetime import datetime
def RegistraCompra(email):
    #Função para o cliente registrar sua compra
    valida.limpaTerminal()
    with open('nome.json', 'r', encoding='utf-8') as arq:
        dados = json.load(arq)
    with open('produtos.json', 'r', encoding='utf-8') as arquivo:
        produtos = json.load(arquivo)

    print('\033[1;34mLista de produtos: \033[m')
    produto = list(produtos.keys())
    for i, p in enumerate(produto, start=1):
        print(f"{i} - {p}")
        
    while True:
        escolha = input('Digite o número do produto que você comprou: ').strip()
        if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(produto):
            print('\033[1;31mOpção inválida. Digite um número da lista\033[m')
            continue
        produto_escolhido = produto[int(escolha)-1]
        break
    
    estoque_atual = int(produtos[produto_escolhido]["Quantidade no estoque"])
    
    while True:
        entrada = input(f'Digite a quantidade de {produto_escolhido} que você comprou: ').strip()
    
    # Verifica se é um número inteiro positivo
        if not entrada.isdigit() or int(entrada) <= 0:
            print("\033[1;31mDigite apenas um número inteiro maior que zero.\033[m")
            continue
        qtd = int(entrada)
    # Verifica se não ultrapassa o estoque
        if qtd > estoque_atual:
            print(f'\033[1;31mQuantidade maior do que a disponível no estoque ({estoque_atual}). Tente novamente.\033[m')
            continue
        break
    valor_unit = produtos[produto_escolhido]["Valor do produto"].replace("R$", "").strip()
    valor_unit = float(valor_unit)
    valor_total = valor_unit * qtd

    compra = {
        "Produto": produto_escolhido,
        "Quantidade": qtd,
        "Valor Unitário": produtos[produto_escolhido]["Valor do produto"],
        "Valor Total": f"R${valor_total:.2f}",
        "Data": datetime.now().strftime("%d/%m/%Y")
    }

    if "compras" not in dados[email]:
        dados[email]["compras"] = []

    dados[email]["compras"].append(compra)

    # Salvar no nome.json
    with open('nome.json', 'w', encoding='utf-8') as arq:
        json.dump(dados, arq, ensure_ascii=False, indent=4)

    # Atualizar estoque no produtos.json
    produtos[produto_escolhido]["Quantidade no estoque"] = str(estoque_atual - qtd)

    with open('produtos.json', 'w', encoding='utf-8') as arquivo:
        json.dump(produtos, arquivo, ensure_ascii=False, indent=4)

    print("\033[1;32mCompra registrada e estoque atualizado com sucesso! Retornando para o menu de compras...\033[m")
    sleep(2)
    menu.Compras(email)
    
def HistoricoCompras(email):
    valida.limpaTerminal()

    # Carrega os dados dos usuários
    with open('nome.json', 'r', encoding='utf-8') as arq:
        dados = json.load(arq)

    # Verifica se o cliente tem registro de compras
    if "compras" not in dados[email] or not dados[email]["compras"]:
        print("\033[33mVocê ainda não realizou nenhuma compra. Voltando para o Menu de Compras...\033[m")
        sleep(2)
        menu.Compras(email)

    print("\033[1;34m=== Histórico de Compras ===\033[m")

    # Listar todas as compras
    for i, compra in enumerate(dados[email]["compras"], start=1):
        print(f"\nCompra {i}:")
        print(f"Produto: {compra['Produto']}")
        print(f"Quantidade: {compra['Quantidade']}")
        print(f"Valor Unitário: {compra['Valor Unitário']}")
        print(f"Valor Total: {compra['Valor Total']}")
        print(f"Data: {compra['Data']}")

    input("\nPressione Enter para voltar ao Menu de Compras...")
    sleep(1)
    menu.Compras(email)
