import valida
import json
from datetime import datetime, timedelta
import menu

def Rankings(email_usuario):
    #Ranking de maiores compradores do mês 
    valida.limpaTerminal()
    with open('nome.json', 'r', encoding='utf-8') as arq:
        dados = json.load(arq)
        
    ranking = []
    mes_atual = datetime.now().strftime('%Y-%m')
    data_atual = datetime.now().strftime('%d/%m/%Y')
    
    # Percorre todos os usuários
    for email, info in dados.items():
        if "compras" in info and info["compras"]:
            total_gasto_mes = 0
            for compra in info["compras"]:
                try:
                    # Considera apenas as compras do mês atual
                    data_compra = datetime.strptime(compra["Data"], "%d/%m/%Y")
                    if data_compra.strftime("%Y-%m") == mes_atual:
                        valor = float(compra["Valor Total"].replace("R$", "").replace(",", "."))
                        total_gasto_mes += valor
                except ValueError:
                    continue  # ignora compras com data inválida

            if total_gasto_mes > 0:
                ranking.append((email, info["Nome"], total_gasto_mes))

    # Ordena do maior para o menor gasto
    ranking.sort(key=lambda x: x[2], reverse=True)

    print("\n\033[1;34m=== Ranking de Clientes que Mais Compraram no Mês ===\033[m")
    for posicao, (email, nome, gasto) in enumerate(ranking, start=1):
        print(f"{posicao}º - {nome} | Total gasto: R${gasto:.2f}")

    # Bonificação: apenas no último dia do mês
    hoje = datetime.now().date()
    # Calcula o último dia do mês
    ultimo_dia_mes = (datetime(hoje.year, hoje.month, 28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    
    if hoje == ultimo_dia_mes.date() and ranking:
        # Descobre o(s) primeiro(s) colocado(s)
        max_gasto = ranking[0][2]
        vencedores = [r for r in ranking if r[2] == max_gasto]

        for email_top, nome_top, _ in vencedores:
            if "Bonificacoes" not in dados[email_top]:
                dados[email_top]["Bonificacoes"] = []

            # Verifica se já recebeu bonificação neste mês
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

        # Salva alterações
        with open('nome.json', 'w', encoding='utf-8') as arq:
            json.dump(dados, arq, ensure_ascii=False, indent=4)

    input("\nPressione Enter para voltar...")
    menu.MenuPrincipal(email_usuario)

def RankingEntregadores(email):
    #Ranking dos entregadores que mais fizeram entregas no Mês
    valida.limpaTerminal()
    with open('nome.json', 'r', encoding='utf-8') as arq:
        dados = json.load(arq)

    entregadores = []
    mes_atual = datetime.now().strftime('%Y-%m')
    data_atual = datetime.now().strftime('%d/%m/%Y')

    # Monta lista de entregadores e quantidade de entregas do mês
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
                    continue  # ignora se o formato da data estiver incorreto

            total_entregas = len(entregas_mes)

            if "Ultimo Mês bonificado" not in info:
                info["Ultimo Mês bonificado"] = ""

            entregadores.append((email_ent, info["Nome"], total_entregas))

    # Ordena pelo maior número de entregas
    entregadores.sort(key=lambda x: x[2], reverse=True)

    print("\n\033[1;34m=== Ranking de Entregadores do Mês ===\033[m")
    for pos, (email_ent, nome, total) in enumerate(entregadores, start=1):
        print(f"{pos}º - {nome} | Entregas: {total}")

    # Bonificação (somente no último dia do mês)
    ultimo_dia_mes = (datetime.now().replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    hoje = datetime.now().date()

    if hoje == ultimo_dia_mes.date() and entregadores:
        # Pega o maior número de entregas
        max_entregas = entregadores[0][2]

        # Pega todos empatados em primeiro lugar
        vencedores = [e for e in entregadores if e[2] == max_entregas and max_entregas > 0]

        for email_top, nome_top, _ in vencedores:
            if dados[email_top]["Ultimo Mês bonificado"] != mes_atual:
                # Registra bonificação no novo formato
                dados[email_top]["Ultimo Mês bonificado"] = mes_atual
                if "Bonificacoes" not in dados[email_top]:
                    dados[email_top]["Bonificacoes"] = []
                dados[email_top]["Bonificacoes"].append(f"R$200 - {data_atual}")

                print(f"\033[32m{nome_top} recebeu uma bonificação de R$200!\033[m")

        # Salva alterações
        with open('nome.json', 'w', encoding='utf-8') as arq:
            json.dump(dados, arq, ensure_ascii=False, indent=4)

    input("\nPressione Enter para voltar...")
    menu.MenuEntregas(email)