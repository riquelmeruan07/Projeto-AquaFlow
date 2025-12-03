# ranking.py
import json
from datetime import datetime, timedelta
from valida import Validador


class GerenciadorRanking:
    ARQ_USUARIOS = 'nome.json'

    def __init__(self, email): 
        self.email = email

    def _carregar_dados(self):
        with open(self.ARQ_USUARIOS, 'r', encoding='utf-8') as arq:
            return json.load(arq)

    def _salvar_dados(self, dados):
        with open(self.ARQ_USUARIOS, 'w', encoding='utf-8') as arq:
            json.dump(dados, arq, ensure_ascii=False, indent=4)

    # ------------------------------
    # RANKING DE CLIENTES
    # ------------------------------
    def mostrar_ranking_clientes(self):
        Validador.limpa_terminal()
        dados = self._carregar_dados()

        ranking = []
        mes_atual = datetime.now().strftime('%Y-%m')
        data_atual = datetime.now().strftime('%d/%m/%Y')

        for email, info in dados.items():
            if "compras" in info and info["compras"]:
                total_gasto_mes = 0
                for compra in info["compras"]:
                    try:
                        data_compra = datetime.strptime(compra["Data"], "%d/%m/%Y")
                        if data_compra.strftime("%Y-%m") == mes_atual:
                            valor = float(compra["Valor Total"].replace("R$", "").replace(",", "."))
                            total_gasto_mes += valor
                    except ValueError:
                        continue

                if total_gasto_mes > 0:
                    ranking.append((email, info["Nome"], total_gasto_mes))

        ranking.sort(key=lambda x: x[2], reverse=True)

        print("\n\033[1;34m=== Ranking de Clientes que Mais Compraram no Mês ===\033[m")
        print("\n\033[34mNo término do mês o cliente que mais comprou, ganhará 2 Santa Joanas como bonificação\033[m")
        for posicao, (email, nome, gasto) in enumerate(ranking, start=1):
            print(f"{posicao}º - {nome} | Total gasto: R${gasto:.2f}")

        # Bonificação: apenas no último dia do mês
        hoje = datetime.now().date()
        ultimo_dia_mes = (datetime(hoje.year, hoje.month, 28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

        if hoje == ultimo_dia_mes.date() and ranking:
            vencedores = []
            max_gasto = ranking[0][2]
            for r in ranking:
                if r[2] == max_gasto:
                    vencedores.append(r)

            for email_top, nome_top, _ in vencedores:
                if "Bonificacoes" not in dados[email_top]:
                    dados[email_top]["Bonificacoes"] = []

                ja_recebeu = False
                for bonif in dados[email_top]["Bonificacoes"]:
                    try:
                        data_bonif = bonif.split(" - ")[1]
                        if datetime.strptime(data_bonif, "%d/%m/%Y").strftime("%Y-%m") == mes_atual:
                            ja_recebeu = True
                            break
                    except IndexError:
                        continue

                if not ja_recebeu:
                    bonificacao = f"2 Santa Joana - {data_atual}"
                    dados[email_top]["Bonificacoes"].append(bonificacao)
                    print(f"\033[32m{nome_top} recebeu a bonificação: {bonificacao}!\033[m")

            self._salvar_dados(dados)

        input("\nPressione Enter para voltar...")
        

    # ------------------------------
    # RANKING DE ENTREGADORES
    # ------------------------------
    def mostrar_ranking_entregadores(self):
        Validador.limpa_terminal()
        dados = self._carregar_dados()

        entregadores = []
        mes_atual = datetime.now().strftime('%Y-%m')
        data_atual = datetime.now().strftime('%d/%m/%Y')

        for email_ent, info in dados.items():
            if info.get("Status") == "Entregador":
                entregas = info.get("Entregas", [])
                entregas_mes = []

                for e in entregas:
                    try:
                        data_entrega = datetime.strptime(e["Data"], "%d/%m/%Y")
                        if data_entrega.strftime("%Y-%m") == mes_atual:
                            entregas_mes.append(e)
                    except ValueError:
                        continue

                total_entregas = len(entregas_mes)

                if "Ultimo Mês bonificado" not in info:
                    info["Ultimo Mês bonificado"] = ""

                entregadores.append((email_ent, info["Nome"], total_entregas))

        entregadores.sort(key=lambda x: x[2], reverse=True)

        print("\n\033[1;34m=== Ranking de Entregadores do Mês ===\033[m")
        print("\n\033[34mNo término do mês o entregador que mais fez entregas, ganhará R$200\033[m")
        for pos, (email_ent, nome, total) in enumerate(entregadores, start=1):
            print(f"{pos}º - {nome} | Entregas: {total}")

        hoje = datetime.now().date()
        ultimo_dia_mes = (datetime(hoje.year, hoje.month, 28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

        if hoje == ultimo_dia_mes.date() and entregadores:
            max_entregas = entregadores[0][2]
            vencedores = []
            for e in entregadores:
                if e[2] == max_entregas and max_entregas > 0:
                    vencedores.append(e)

            for email_top, nome_top, _ in vencedores:
                if dados[email_top]["Ultimo Mês bonificado"] != mes_atual:
                    dados[email_top]["Ultimo Mês bonificado"] = mes_atual
                    if "Bonificacoes" not in dados[email_top]:
                        dados[email_top]["Bonificacoes"] = []
                    dados[email_top]["Bonificacoes"].append(f"R$200 - {data_atual}")

                    print(f"\033[32m{nome_top} recebeu uma bonificação de R$200!\033[m")

            self._salvar_dados(dados)

        input("\nPressione Enter para voltar...")
        
