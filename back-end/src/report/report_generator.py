import json
from typing import List
from plasTeX.TeX import TeX
from plasTeX.Base import Text
from babel.dates import format_date
from datetime import datetime, date
import re
import subprocess
import os
import matplotlib.pyplot as plt
import os
import shutil

from ..analysis.json_parser import montar_conteudo_latex
from ..analysis.csv_parser import montar_conteudo_latex_csv


def gerar_relatorio_txt(output_file: str, risk_factor_counts: dict, common_vulnerabilities: dict, targets: List[str]):
    """
    Gera um relatório de texto com as vulnerabilidades e as informações coletadas.

    Parâmetros:
    - output_file (str): Caminho do arquivo onde o relatório será salvo.
    - risk_factor_counts (dict): Dicionário com a contagem das vulnerabilidades por tipo.
    - common_vulnerabilities (dict): Dicionário com as vulnerabilidades comuns entre os sites/URI.
    - targets (List[str]): Lista com os domínios analisados.
    """
    with open(output_file, 'w', encoding='utf-8') as output:
        output.write("Resumo das Vulnerabilidades por Risk Factor:\n\n")
        output.write(f"Critical: {risk_factor_counts['Critical']}\n")
        output.write(f"High: {risk_factor_counts['High']}\n")
        output.write(f"Medium: {risk_factor_counts['Medium']}\n")
        output.write(f"Low: {risk_factor_counts['Low']}\n")

        total = sum(risk_factor_counts.values())
        output.write(f"Total de Vulnerabilidades:{total}\n\n")

        output.write("\nDomínios analisados:\n")
        output.write(f"\nTotal de sites:{len(targets)}\n")
        output.write("\n".join(targets))

        output.write("\n\nVulnerabilidades em comum, entre os sites/URI:\n\n")
        sorted_vulnerabilities = sorted(common_vulnerabilities.items(), key=lambda x: len(set(x[1])), reverse=True)
        for (name, plugin_id), uris in sorted_vulnerabilities:
            if len(uris) > 1:
                unique_uris = set(uris)
                output.write(f"\nVulnerabilidade:{name}\n")
                output.write(f"Plugin ID:{plugin_id}\n")
                output.write(f"Total de URI Afetadas:{len(unique_uris)}\n")
                output.write(f"URI Afetadas:\n")
                for url in unique_uris:
                    output.write(f"{url}\n")
                    
                    
def gerar_relatorio_txt_csv(output_file: str, risk_factor_counts: dict, common_vulnerabilities: dict, targets: List[str]):
    """
    Gera um relatório de texto com as vulnerabilidades e as informações coletadas.

    Parâmetros:
    - output_file (str): Caminho do arquivo onde o relatório será salvo.
    - risk_factor_counts (dict): Dicionário com a contagem das vulnerabilidades por tipo.
    - common_vulnerabilities (dict): Dicionário com as vulnerabilidades comuns entre os sites/URI.
    - targets (List[str]): Lista com os domínios analisados.
    """
    with open(output_file, 'w', encoding='utf-8') as output:
        output.write("Resumo das Vulnerabilidades por Risk Factor:\n\n")
        output.write(f"Critical: {risk_factor_counts.get('critical', 0)}\n")
        output.write(f"High: {risk_factor_counts.get('high', 0)}\n")
        output.write(f"Medium: {risk_factor_counts.get('medium', 0)}\n")
        output.write(f"Low: {risk_factor_counts.get('low', 0)}\n")

        total = sum(risk_factor_counts.values())
        output.write(f"\nTotal de Vulnerabilidades: {total}\n\n")

        output.write("Hosts analisados:\n")
        output.write(f"Total de Hosts: {len(targets)}\n")
        output.write("\n".join(targets))

        output.write("\n\nVulnerabilidades em comum entre os Hosts:\n\n")
        # Ordenar pela quantidade de hosts afetados (em ordem decrescente)
        sorted_vulnerabilities = sorted(
            common_vulnerabilities.items(),
            key=lambda item: len(item[1]['hosts']),
            reverse=True
        )

        for name, data in sorted_vulnerabilities:
            hosts_afetados = data['hosts']
            riscos = data['risks']
            output.write(f"\nVulnerabilidade: {name}\n")
            output.write(f"Severidade: {', '.join(riscos)}\n")
            output.write(f"Total de Hosts Afetados: {len(hosts_afetados)}\n")
            output.write("Hosts Afetados:\n")
            for host in hosts_afetados:
                output.write(f"{host}\n")
                

def gerar_relatorio_latex(caminho_saida_latex, caminho_relatorios_preprocessados, caminho_relatorio_exemplo):
    """
    Gera o relatório LaTeX a partir das vulnerabilidades comuns e do arquivo de vulnerabilidades JSON.

    Parâmetros:
    - vulnerabilidades_comuns (dict): Dicionário com vulnerabilidades e sites associados.
    """

    with open(f"{caminho_relatorio_exemplo}/vulnerabilidades.json", 'r', encoding='utf-8') as file:
        vulnerabilidades_dados= json.load(file)

    conteudo_latex = montar_conteudo_latex(f"{caminho_relatorios_preprocessados}/Sites_agrupados_por_vulnerabilidades.txt", vulnerabilidades_dados, caminho_relatorio_exemplo)

    with open(caminho_saida_latex, 'w', encoding='utf-8') as file:
        file.write(conteudo_latex)
        
    print(f"Relatório LaTeX gerado em {caminho_saida_latex}.")

def terminar_relatorio_preprocessado(nome_secretaria: str, sigla_secretaria: str, inicio_data: str, fim_data: str, ano_conclusao: str, mes_conclusao: str, caminho_relatorio_preprocessado: str, caminho_saida_relatorio_pronto: str, caminho_relatorio_exemplo: str, google_drive_link: str):

    caminho_relatorio_pronto = f"{caminho_relatorio_preprocessado}/RelatorioPronto/"
    copiar_relatorio_exemplo(f"{caminho_relatorio_exemplo}/RelatorioExemplo/", caminho_relatorio_pronto)

    # Leitura do LaTeX de exemplo (main.tex base)
    with open(f'{caminho_relatorio_pronto}/main.tex', 'r', encoding='utf-8') as f:
        latex_code = f.read()

    # --- Leitura do conteúdo de vulnerabilidades de sites ---
    relatorio_sites_conteudo = []
    caminho_sites_vulnerabilidades_latex = f"{caminho_relatorio_preprocessado}/(LATEX)Sites_agrupados_por_vulnerabilidades.txt"
    if os.path.exists(caminho_sites_vulnerabilidades_latex):
        with open(caminho_sites_vulnerabilidades_latex, "r", encoding='utf-8') as file:
            for linha in file:
                # O limite parece ser para cortar a parte "Vulnerabilidades sem Categoria" de sites
                # Se você quiser que essa parte vá para o RELATORIO GERADO, mantenha a condição
                limite_sites = "%-------------- INÍCIO DAS VULNERABILIDADES SEM CATEGORIA --------------"
                if limite_sites in linha:
                    break
                relatorio_sites_conteudo.append(linha)
    else:
        print(f"Aviso: Arquivo '{caminho_sites_vulnerabilidades_latex}' não encontrado.")
    relatorio_sites_final = ''.join(relatorio_sites_conteudo)

    # --- Leitura do conteúdo de vulnerabilidades de servidores ---
    relatorio_servidores_conteudo = []
    caminho_servidores_vulnerabilidades_latex = f"{caminho_relatorio_preprocessado}/(LATEX)Servidores_agrupados_por_vulnerabilidades.txt"
    if os.path.exists(caminho_servidores_vulnerabilidades_latex):
        with open(caminho_servidores_vulnerabilidades_latex, "r", encoding='utf-8') as file:
            # Agora, o limite para servidores é aplicado aqui também
            limite_servidores = "%-------------- INÍCIO DAS VULNERABILIDADES SEM CATEGORIA --------------"
            for linha in file:
                if limite_servidores in linha:
                    break # Interrompe a leitura ao encontrar a linha de "Vulnerabilidades sem Categoria"
                relatorio_servidores_conteudo.append(linha)
    else:
        print(f"Aviso: Arquivo '{caminho_servidores_vulnerabilidades_latex}' não encontrado.")
    relatorio_servidores_final = ''.join(relatorio_servidores_conteudo)

    # Leitura do relatório em texto para extrair totais
    # ATENÇÃO: Verifique a fonte desses totais. Se a soma dos hosts/vulnerabilidades
    # for diferente entre sites e servidores, ou se você precisar de totais combinados,
    # esta lógica precisará de ajuste. Por enquanto, mantém como está.
    caminho_agrupados_sites_txt = f"{caminho_relatorio_preprocessado}/Sites_agrupados_por_vulnerabilidades.txt"
    agrupados_vulnerabilidades = ""
    if os.path.exists(caminho_agrupados_sites_txt):
        with open(caminho_agrupados_sites_txt, "r", encoding='utf-8') as file:
            agrupados_vulnerabilidades = file.read()
    else:
        print(f"Erro: Arquivo '{caminho_agrupados_sites_txt}' não encontrado para extração de totais.")
    
    caminho_agrupados_sites_txt = f"{caminho_relatorio_preprocessado}/Servidores_agrupados_por_vulnerabilidades.txt"
    agrupados_vulnerabilidades_servidores = ""
    if os.path.exists(caminho_agrupados_sites_txt):
        with open(caminho_agrupados_sites_txt, "r", encoding='utf-8') as file:
            agrupados_vulnerabilidades_servidores = file.read()
    else:
        print(f"Erro: Arquivo '{caminho_agrupados_sites_txt}' não encontrado para extração de totais.")
        
    #WEB
    total_sites = re.search(r'Total de sites:*\s*(\d+)', agrupados_vulnerabilidades).group(1) if re.search(r'Total de sites:*\s*(\d+)', agrupados_vulnerabilidades) else '0'
    total_vulnerabilidades_web = re.search(r'Total de Vulnerabilidades:\s*(\d+)', agrupados_vulnerabilidades).group(1) if re.search(r'Total de Vulnerabilidades:\s*(\d+)', agrupados_vulnerabilidades) else '0'
    total_vulnerabilidades_criticas_web = re.search(r'Critical:\s*(\d+)', agrupados_vulnerabilidades).group(1) if re.search(r'Critical:\s*(\d+)', agrupados_vulnerabilidades) else '0'
    total_vulnerabilidades_alta_web = re.search(r'High:\s*(\d+)', agrupados_vulnerabilidades).group(1) if re.search(r'High:\s*(\d+)', agrupados_vulnerabilidades) else '0'
    total_vulnerabilidades_media_web = re.search(r'Medium:\s*(\d+)', agrupados_vulnerabilidades).group(1) if re.search(r'Medium:\s*(\d+)', agrupados_vulnerabilidades) else '0'
    total_vulnerabilidades_baixa_web = re.search(r'Low:\s*(\d+)', agrupados_vulnerabilidades).group(1) if re.search(r'Low:\s*(\d+)', agrupados_vulnerabilidades) else '0'
    
    # SERVIDORES
    total_vulnerabilidade_vm = re.search(r'Total de Vulnerabilidades:\s*(\d+)', agrupados_vulnerabilidades_servidores).group(1) if re.search(r'Total de Vulnerabilidades:\s*(\d+)', agrupados_vulnerabilidades) else '0'
    total_vulnerabilidades_criticas_servidores = re.search(r'Critical:\s*(\d+)', agrupados_vulnerabilidades_servidores).group(1) if re.search(r'Critical:\s*(\d+)', agrupados_vulnerabilidades_servidores) else '0'
    total_vulnerabilidades_alta_servidores = re.search(r'High:\s*(\d+)', agrupados_vulnerabilidades_servidores).group(1) if re.search(r'High:\s*(\d+)', agrupados_vulnerabilidades_servidores) else '0'
    total_vulnerabilidades_baixa_servidores = re.search(r'Low:\s*(\d+)', agrupados_vulnerabilidades_servidores).group(1) if re.search(r'Low:\s*(\d+)', agrupados_vulnerabilidades_servidores) else '0'
    total_vulnerabilidades_media_servidores = re.search(r'Medium:\s*(\d+)', agrupados_vulnerabilidades_servidores).group(1) if re.search(r'Medium:\s*(\d+)', agrupados_vulnerabilidades_servidores) else '0'
    
    #TOTAL
    total_vulnerabilidades = int(total_vulnerabilidade_vm) + int(total_vulnerabilidades_web)
    total_vulnerabilidades = str(total_vulnerabilidades)  # Convertendo para string para manter o tipo consistente
    # Substituições globais
    substituicoes_globais = {
        'TOTAL_SITES' : total_sites,
        'NOME SECRETARIA': nome_secretaria,
        'SIGLA': sigla_secretaria,
        'INICIO DATA': inicio_data,
        'FIM DATA': fim_data,
        'RELATORIO GERADO': relatorio_sites_final, # Placeholder para sites
        'RELATORIO SERVIDORES': relatorio_servidores_final, # NOVO Placeholder para servidores
        'TOTAL VULNERABILIDADES': total_vulnerabilidades,
        'TOTAL VULNERABILIDADES WEB': total_vulnerabilidades_web,
        'TOTAL VULNERABILIDADES VM': total_vulnerabilidade_vm, # Ajustar se for total de hosts VM
        'TOTAL VULNERABILIDADES WAS CRITICA': total_vulnerabilidades_criticas_web,
        'TOTAL VULNERABILIDADES WAS ALTA': total_vulnerabilidades_alta_web,
        'TOTAL VULNERABILIDADES WAS MEDIA': total_vulnerabilidades_media_web,
        'TOTAL VULNERABILIDADES WAS BAIXA': total_vulnerabilidades_baixa_web,
        'MES CONCLUSAO': mes_conclusao,
        'ANO CONCLUSAO': ano_conclusao,
        'GOOGLE DRIVE LINK': google_drive_link
    }

    # Aplicar substituições no LaTeX
    latex_editado = substituir_placeholders(
        conteudo=latex_code,
        substituicoes_globais=substituicoes_globais
    )

    # Salvar o arquivo final .tex
    with open(f"{caminho_relatorio_pronto}/main.tex", "w", encoding="utf-8") as f:
        f.write(latex_editado)

    gerar_grafico(total_vulnerabilidades_criticas_web, total_vulnerabilidades_alta_web, total_vulnerabilidades_media_web, total_vulnerabilidades_baixa_web, f"{caminho_relatorio_pronto}/assets/images-was")
    gerar_grafico(total_vulnerabilidades_criticas_servidores, total_vulnerabilidades_alta_servidores, total_vulnerabilidades_media_servidores, total_vulnerabilidades_baixa_servidores, f"{caminho_relatorio_pronto}/assets/images-vmscan")

def gerar_relatorio_latex_csv(caminho_saida_latex, caminho_relatorios_preprocessados, caminho_relatorio_exemplo):
    """
    Gera o relatório LaTeX a partir das vulnerabilidades comuns e do arquivo de vulnerabilidades JSON.

    Parâmetros:
    - vulnerabilidades_comuns (dict): Dicionário com vulnerabilidades e sites associados.
    """

    with open("data/vulnerabilidades_servidores.json", 'r', encoding='utf-8') as file:
        vulnerabilidades_dados= json.load(file)

    conteudo_latex = montar_conteudo_latex_csv(f"{caminho_relatorios_preprocessados}/Servidores_agrupados_por_vulnerabilidades.txt", vulnerabilidades_dados, caminho_relatorio_exemplo)

    with open(caminho_saida_latex, 'w', encoding='utf-8') as file:
        file.write(conteudo_latex)
        
    print(f"Relatório LaTeX gerado em {caminho_saida_latex}.")

def gerar_grafico(critical, high, medium, low, caminho_salvar):
    # Create a list of (label, size, color) tuples,
    # filtering out any categories with a size of 0.
    data = []
    if int(critical) > 0:
        data.append(('Critical', int(critical), '#8B0000'))
    if int(high) > 0:
        data.append(('High', int(high), '#FF3030'))
    if int(medium) > 0:
        data.append(('Medium', int(medium), '#FFE066'))
    if int(low) > 0:
        data.append(('Low', int(low), '#87F1FF'))

    # If no data, exit the function to avoid an empty chart
    if not data:
        print("No vulnerabilities to display.")
        return

    labels = [item[0] for item in data]
    sizes = [item[1] for item in data]
    colors = [item[2] for item in data]
    explode = (0,) * len(labels) # Explode tuple should match the number of labels

    # Function to return the absolute value
    def mostrar_valor(pct, allvals):
        absolute = int(round(pct / 100. * sum(allvals)))
        return f"{absolute}"

    # Criar gráfico de rosca
    fig, ax = plt.subplots(figsize=(8, 8)) # Aumenta o tamanho da figura
    wedges, texts, autotexts = ax.pie(
        sizes,
        # labels=labels, # REMOVIDO: Para remover os nomes em cima das cores
        colors=colors,
        explode=explode,
        startangle=90,
        wedgeprops=dict(width=0.4),
        autopct=lambda pct: mostrar_valor(pct, sizes), # Valores dentro da fatia
        pctdistance=0.85 # Posiciona os números mais próximos do centro da fatia
    )

    # Melhorar legibilidade do texto
    # Os 'texts' são os labels externos que você pediu para remover, então não precisamos mais iterar sobre eles
    # for text in texts:
    #     text.set_fontsize(12)

    for autotext in autotexts: # Valores dentro da fatia
        autotext.set_fontsize(14) # AUMENTADO: Tamanho da fonte dos números
        autotext.set_color('black') # Garante que o número seja visível

    # Posicionamento da legenda
    plt.legend(wedges, labels, title="Severidade", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    # Formatar como círculo
    ax.axis('equal')

    # Ajusta o layout para evitar que a legenda se sobreponha ao gráfico
    plt.tight_layout()

    plt.savefig(f"{caminho_salvar}/Total_Vulnerabilidades.png", dpi=300, bbox_inches='tight')

def copiar_relatorio_exemplo(caminho_relatorio_exemplo: str, caminho_saida: str):

    src = r'\\?\\' + os.path.abspath(caminho_relatorio_exemplo)
    dst = r'\\?\\' + os.path.abspath(caminho_saida)

    shutil.copytree(src, dst)

def compilar_latex(caminho_arquivo_tex: str, pasta_saida: str):
    try:
        # Use pdflatex diretamente (assumindo que o PATH foi configurado na instalação do MiKTeX)
        subprocess.run([
            'pdflaTeX',
            '-interaction=nonstopmode',
            '-output-directory', pasta_saida,
            caminho_arquivo_tex
        ], check=True)
        print("✅ PDF compilado com sucesso.")
    except FileNotFoundError:
        print("❌ Erro: 'pdflatex' não encontrado. Verifique se o MiKTeX está instalado e no PATH.")
    except subprocess.CalledProcessError as e:
        print("❌ Erro ao compilar o PDF:")
        print(e)


def substituir_placeholders(conteudo, substituicoes_por_secao=None, substituicoes_globais=None):
    if substituicoes_por_secao:
        padrao_secao = r'(\\(sub)?section\{([^\}]*)\})(.*?)(?=(\\(sub)?section\{|\Z))'

        def substituir_secao(match):
            cabecalho = match.group(1)
            titulo = match.group(3).strip()
            corpo = match.group(4)

            if titulo in substituicoes_por_secao:
                for alvo, novo in substituicoes_por_secao[titulo].items():
                    corpo = corpo.replace(f'[{alvo}]', novo)
            return cabecalho + corpo

        conteudo = re.sub(padrao_secao, substituir_secao, conteudo, flags=re.DOTALL)

    if substituicoes_globais:
        for alvo, novo in substituicoes_globais.items():
            conteudo = conteudo.replace(f'[{alvo}]', novo)

    return conteudo


def gerar_relatorio_csv(dados: list, output_path: str) -> None:
    """
    Gera o relatório de vulnerabilidades agrupadas por site.
    
    Parâmetros:
    - dados (list): Lista de dicionários contendo os dados de vulnerabilidades.
    - output_path (str): Caminho onde o relatório será salvo.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        for dado in dados:
            f.write(f"Site: {dado['Site']}\n")
            f.write(f"Critical: {dado['Critical']}\n")
            f.write(f"High: {dado['High']}\n")
            f.write(f"Medium: {dado['Medium']}\n")
            f.write(f"Low: {dado['Low']}\n")
            f.write(f"Total: {dado['Total']}\n")
            f.write("\n")
