# admin_estoque.py
import json
import os
from time import sleep
from valida import Validador


class AdminEstoque:
    ARQ_PRODUTOS = 'produtos.json'
    LIMITE_ESTOQUE_BAIXO = 5
    
    def __init__(self, email_admin):
        self.email_admin = email_admin

    def _carregar_produtos(self):
        if os.path.exists(self.ARQ_PRODUTOS):
            with open(self.ARQ_PRODUTOS, 'r', encoding='utf-8') as arq:
                return json.load(arq)
        return {}

    def _salvar_produtos(self, dados):
        with open(self.ARQ_PRODUTOS, 'w', encoding='utf-8') as arq:
            json.dump(dados, arq, ensure_ascii=False, indent=4)

    def adicionar_produto(self):
        Validador.limpa_terminal()
        print('\033[1;34mAdicione um novo produto no estoque\033[m')
        produto = Validador.valida_produto()
        quantia = str(Validador.valida_qtd())
        valor = Validador.valida_valor()
        data = Validador.valida_data()

        dados = self._carregar_produtos()

        dados[produto] = {
            "Quantidade no estoque": quantia,
            "Valor do produto": valor,
            "Data de validade": data.strftime('%d/%m/%Y')
        }

        self._salvar_produtos(dados)

        print(f'O produto {produto} foi adicionado com sucesso')
        print('Retornando para o menu de estoque...')
        sleep(2)
        return

    def editar_produto(self):
        Validador.limpa_terminal()
        dados = self._carregar_produtos()

        if not dados:
            print("O estoque está vazio.")
            input("Pressione Enter para voltar...")
            return

        print('\033[1;34mLista de produtos: \033[m')
        produtos = list(dados.keys())
        for i, p in enumerate(produtos, start=1):
            print(f"{i} - {p}")

        while True:
            escolha = input('Digite o número do produto que deseja editar: ').strip()
            if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(produtos):
                print("Opção inválida. Digite um número da lista.")
                continue
            produto = produtos[int(escolha)-1]
            break

        print(f"\nDados atuais de {produto}:")
        for chave, valor in dados[produto].items():
            print(f"{chave}: {valor}")

        print("\nO que deseja alterar?")
        print("1 - Quantidade e data de validade")
        print("2 - Valor")
        print("3 - Cancelar")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == '1':
            print(f"A quantidade atual é {dados[produto]['Quantidade no estoque']}")
            nova_quantidade = Validador.valida_qtd()
            dados[produto]['Quantidade no estoque'] = str(nova_quantidade)

            nova_data = Validador.valida_data()
            dados[produto]['Data de validade'] = nova_data.strftime('%d/%m/%Y')

            print(f"Quantidade de '{produto}' atualizada para {nova_quantidade} e data de validade para {nova_data.strftime('%d/%m/%Y')}.")

        elif opcao == '2':
            print(f"Valor atual: {dados[produto]['Valor do produto']}")
            novo_valor = Validador.valida_valor()
            dados[produto]['Valor do produto'] = novo_valor
            print(f"Valor de '{produto}' atualizado para {novo_valor}.")

        elif opcao == '3':
            print("Edição cancelada.")
            sleep(2)
            return
        else:
            print("Opção inválida.")
            return

        self._salvar_produtos(dados)

        print("\033[32mProduto atualizado com sucesso!\033[m")
        print("\033[32mRetornando para o menu de estoque...\033[m")
        sleep(2)
        return

    def deletar_produto(self):
        Validador.limpa_terminal()
        dados = self._carregar_produtos()

        if not dados:
            print("Nenhum produto cadastrado.")
            sleep(2)
            return

        print('\033[1;34mLista de produtos: \033[m')
        produtos = list(dados.keys())
        for i, p in enumerate(produtos, start=1):
            print(f"{i} - {p}")

        while True:
            escolha = input('Digite o número do produto que deseja excluir: ').strip()
            if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(produtos):
                print("Opção inválida. Digite um número da lista.")
                continue
            produto = produtos[int(escolha)-1]
            break

        confirma = input(f"Tem certeza que deseja excluir o produto '{produto}'? [s/n]: ").strip().lower()
        while confirma not in ['s', 'n']:
            print("\033[1;31mOpção inválida.\033[m")
            confirma = input("Digite apenas [s/n]: ").strip().lower()

        if confirma == 's':
            del dados[produto]
            self._salvar_produtos(dados)
            print(f"\033[32mProduto '{produto}' deletado com sucesso!\033[m")
        else:
            print("Exclusão cancelada.")

        sleep(2)
        return
    def verificar_estoque_baixo(self):
        """Verifica quais produtos estão abaixo do limite de estoque baixo."""
        
        produtos = self._carregar_produtos()
        
        if not produtos:
            return [] # Retorna lista vazia se não houver produtos
        
        # Lista para armazenar produtos em alerta
        produtos_em_alerta = []
        
        # O limite é uma constante da classe (AdminEstoque.LIMITE_ESTOQUE_BAIXO)
        limite = self.LIMITE_ESTOQUE_BAIXO 

        for nome, info in produtos.items():
            try:
                # É crucial converter a string de quantidade para int
                quantidade = int(info.get("Quantidade no estoque", 0))
                
                if quantidade <= limite:
                    produtos_em_alerta.append(
                        (nome, quantidade) # Armazena o nome e a quantidade atual
                    )
            except ValueError:
                # Trata o caso em que 'Quantidade no estoque' não é um número válido
                print(f"Aviso: Quantidade inválida para o produto '{nome}'.")
                continue 
        
        return produtos_em_alerta
    
    def mostrar_alerta_estoque(self):
        """Exibe os produtos que estão com estoque baixo e aguarda Enter."""
        
        produtos_alerta = self.verificar_estoque_baixo()
        
        Validador.limpa_terminal()

        print("\033[1;33m⚠️ ALERTA DE ESTOQUE BAIXO ⚠️\033[m")
        
        if not produtos_alerta:
            print(f"\033[32mNenhum produto está abaixo do limite de {self.LIMITE_ESTOQUE_BAIXO}.\033[m")
        else:
            print("\033[31mOs seguintes produtos precisam de atenção:\033[m")
            for nome, qtd in produtos_alerta:
                print(f"  - {nome}: {qtd} em estoque.")
            
        print("-" * 35)
        input("Pressione Enter para ir ao Menu de Estoque...")
        sleep(1)