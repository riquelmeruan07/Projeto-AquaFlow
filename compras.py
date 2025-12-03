import json
from time import sleep
from datetime import datetime
from valida import Validador  # sua classe nova de validação


class GerenciadorCompras:
    ARQ_USUARIOS = 'nome.json'
    ARQ_PRODUTOS = 'produtos.json'

    def __init__(self, email):
        self.email = email

    # -------------------------
    # Utilitários de arquivo
    # -------------------------
    def _carregar_usuarios(self):
        with open(self.ARQ_USUARIOS, 'r', encoding='utf-8') as arq:
            return json.load(arq)

    def _salvar_usuarios(self, dados):
        with open(self.ARQ_USUARIOS, 'w', encoding='utf-8') as arq:
            json.dump(dados, arq, ensure_ascii=False, indent=4)

    def _carregar_produtos(self):
        with open(self.ARQ_PRODUTOS, 'r', encoding='utf-8') as arq:
            return json.load(arq)

    def _salvar_produtos(self, produtos):
        with open(self.ARQ_PRODUTOS, 'w', encoding='utf-8') as arq:
            json.dump(produtos, arq, ensure_ascii=False, indent=4)

    # -------------------------
    # Registrar compra
    # -------------------------
    def registrar_compra(self):
        """Permite ao cliente registrar uma compra e atualiza o estoque."""
        Validador.limpa_terminal()

        dados = self._carregar_usuarios()
        produtos = self._carregar_produtos()

        print('\033[1;34mLista de produtos: \033[m')
        nomes_produtos = list(produtos.keys())
        for i, p in enumerate(nomes_produtos, start=1):
            print(f"{i} - {p}")

        # Escolha do produto
        while True:
            escolha = input('Digite o número do produto que você comprou: ').strip()
            if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(nomes_produtos):
                print('\033[1;31mOpção inválida. Digite um número da lista\033[m')
                continue
            produto_escolhido = nomes_produtos[int(escolha) - 1]
            break

        estoque_atual = int(produtos[produto_escolhido]["Quantidade no estoque"])

        # Quantidade comprada
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
        
        print('\n\033[1;34mEnviando código de confirmação de pagamento... \033[m')
        codigo_enviado = Validador.enviar_codigo(self.email)
        
        if not codigo_enviado:
            print('\033[1;31mErro ao enviar código. Compra cancelada. \033[m')
            sleep(2)
            return
        
        tentativas = 3
        while tentativas > 0:
            cod = input("Código: ").strip()
            if cod == codigo_enviado:
                print("\033[32mPagamento confirmado!\033[m")
                break
            tentativas -= 1
            print(f"\033[31mCódigo incorreto. Tentativas restantes: {tentativas}\033[m")

            if tentativas == 0:
                print("\033[31mFalha ao confirmar pagamento. Compra cancelada.\033[m")
                return
            
        
        valor_unit = produtos[produto_escolhido]["Valor do produto"].replace("R$", "").strip()
        valor_unit = float(valor_unit)
        valor_total = valor_unit * qtd

        compra = {
            "Produto": produto_escolhido,
            "Quantidade": qtd,
            "Valor Unitário": produtos[produto_escolhido]["Valor do produto"],
            "Valor Total": f"R${valor_total:.2f}",
            "Data": datetime.now().strftime("%d/%m/%Y"),
            "Status" : "Em trânsito"
        }

        if "compras" not in dados[self.email]:
            dados[self.email]["compras"] = []

        dados[self.email]["compras"].append(compra)

        # Salvar no nome.json
        self._salvar_usuarios(dados)

        # Atualizar estoque no produtos.json
        produtos[produto_escolhido]["Quantidade no estoque"] = str(estoque_atual - qtd)
        self._salvar_produtos(produtos)

        print("\033[1;32mCompra registrada e estoque atualizado com sucesso! Retornando para o menu de compras...\033[m")
        sleep(2)

    # -------------------------
    # Histórico de compras
    # -------------------------
    def historico_compras(self):
        """Mostra o histórico de compras do cliente."""
        Validador.limpa_terminal()

        dados = self._carregar_usuarios()

        if "compras" not in dados[self.email] or not dados[self.email]["compras"]:
            print("\033[33mVocê ainda não realizou nenhuma compra. Voltando para o Menu de Compras...\033[m")
            sleep(2)
            return

        print("\033[1;34m=== Histórico de Compras ===\033[m")

        for i, compra in enumerate(dados[self.email]["compras"], start=1):
            print(f"\nCompra {i}:")
            print(f"Produto: {compra['Produto']}")
            print(f"Quantidade: {compra['Quantidade']}")
            print(f"Valor Unitário: {compra['Valor Unitário']}")
            print(f"Valor Total: {compra['Valor Total']}")
            print(f"Data: {compra['Data']}")

        input("\nPressione Enter para voltar ao Menu de Compras...")
        sleep(1)
