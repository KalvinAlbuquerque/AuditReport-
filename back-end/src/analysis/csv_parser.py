from collections import defaultdict
import json
import os
import re
from typing import List
import pandas as pd
from json_parser import carregar_descritivo_vulnerabilidades
from utils.json_utils import carregar_json_utf


def obter_vulnerabilidades_comum_csv(csv_files: List[str]) -> dict:
    """
    Obtém as vulnerabilidades comuns entre os arquivos CSV, agrupando-as por Name,
    listando os hosts afetados e a severidade (Risk).

    Parâmetros:
    - csv_files (List[str]): Lista com os caminhos dos arquivos CSV.

    Retorna:
    - dict: Dicionário com vulnerabilidades agrupadas por Name, contendo os hosts afetados (sem repetição)
            e a severidade (risk).
    """
    # Utiliza defaultdict para agrupar vulnerabilidades por nome
    common_vulnerabilities = defaultdict(lambda: {"hosts": set(), "risks": set()})

    # Itera sobre cada arquivo CSV
    if not csv_files:
        return {}
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file, usecols=['Name', 'Host', 'Risk'])
            df = df.dropna(subset=['Name', 'Host', 'Risk'])

            for _, row in df.iterrows():
                name = str(row['Name']).strip()
                host = str(row['Host']).strip()
                risk = str(row['Risk']).strip().lower()

                if risk in {'critical', 'high', 'medium', 'low'}:
                    common_vulnerabilities[name]["hosts"].add(host)
                    common_vulnerabilities[name]["risks"].add(risk)
        except Exception as e:
            print(f"Erro ao processar {csv_file}: {e}")

    # Converte sets para listas para facilitar exportação ou exibição
    return {
        name: {
            "hosts": list(data["hosts"]),
            "risks": list(data["risks"])
        }
        for name, data in common_vulnerabilities.items()
    }
    
def contar_vulnerabilidades_csv(vulnerabilidades: dict) -> dict:
    """
    Conta a quantidade total de vulnerabilidades por nível de risco, considerando
    quantos hosts foram afetados por cada vulnerabilidade.

    Parâmetros:
    - vulnerabilidades (dict): Dicionário retornado pela função obter_vulnerabilidades_comum_csv.

    Retorna:
    - dict: Dicionário com as contagens totais de vulnerabilidades por nível de risco.
    """
    contagem = {"critical": 0, "high": 0, "medium": 0, "low": 0}

    for dados in vulnerabilidades.values():
        hosts_afetados = dados["hosts"]
        riscos = dados["risks"]

        if len(riscos) == 1:
            risco = riscos[0]  # Pega a única severidade existente
            if risco in contagem:
                contagem[risco] += len(hosts_afetados)
        else:
            print(f"Atenção: múltiplos níveis de risco encontrados para uma vulnerabilidade: {riscos}")

    return contagem

def extrair_hosts_csv(csv_files: List[str]) -> List[str]:
    """
    Extrai os hosts únicos a partir dos arquivos CSV exportados do Tenable.

    Parâmetros:
    - csv_files (List[str]): Lista com os caminhos dos arquivos CSV.

    Retorna:
    - List[str]: Lista com os hosts únicos encontrados nos arquivos.
    """
    hosts = set()  # Usando um conjunto para evitar duplicatas

    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file, usecols=['Host'])
            df['Host'] = df['Host'].astype(str).str.strip()

            for host in df['Host'].dropna():
                if host:
                    hosts.add(host)
        except Exception as e:
            print(f"Erro ao processar {csv_file}: {e}")

    return list(hosts)

def montar_conteudo_latex_csv(caminho_arquivo, vulnerabilidades_dados, caminho_relatorio_exemplo: str):
    """
    Monta o conteúdo LaTeX para um relatório de vulnerabilidades a partir de um arquivo de relatório e dados adicionais.

    Parâmetros:
    - caminho_arquivo (str): O caminho completo do arquivo de relatório contendo as vulnerabilidades.
    - vulnerabilidades_dados (list): Lista de dicionários contendo informações adicionais sobre as vulnerabilidades 
      (como categoria, subcategoria, descrição, solução e imagem).

    Retorno:
    - str: Conteúdo completo em LaTeX, pronto para ser inserido em um relatório.
    """

    # Carregar as vulnerabilidades do arquivo de relatório
    vulnerabilidades = carregar_vulnerabilidades_do_relatorio_csv(caminho_arquivo)
    
    descritivos_vulnerabilidade = carregar_descritivo_vulnerabilidades_csv(f"{caminho_relatorio_exemplo}/descritivo_vulnerabilidades_servidores.json")
    
    # Gerar o conteúdo LaTeX para as vulnerabilidades carregadas
    conteudo_latex = gerar_conteudo_latex_para_vulnerabilidades_csv(vulnerabilidades, vulnerabilidades_dados, descritivos_vulnerabilidade)
    
    return conteudo_latex  # Retorna o conteúdo LaTeX completo

def carregar_descritivo_vulnerabilidades_csv(caminho_arquivo):
    """
    Carrega e organiza as informações de categorias e subcategorias de vulnerabilidades 
    a partir de um arquivo JSON.

    Parâmetros:
    - caminho_arquivo (str): O caminho completo do arquivo JSON contendo as descrições.

    Retorno:
    - list: Uma lista de dicionários contendo as descrições de categorias e subcategorias.
    """
    descritivo = []

    dados = carregar_json_utf(caminho_arquivo)
        
    for categoria in dados["vulnerabilidades"]:
        print(categoria)
        categoria_nome = categoria["categoria"]
        categoria_descricao = categoria["descricao"]
        
        # Adiciona a categoria principal
        descritivo.append({
            "categoria": categoria_nome,
            "descricao": categoria_descricao
        })

        # Adiciona as subcategorias, se existirem
        for subcategoria in categoria.get("subcategorias", []):
            descritivo.append({
                "categoria": categoria_nome,
                "subcategoria": subcategoria["subcategoria"],
                "descricao": subcategoria["descricao"]
            })

    return descritivo  # Retorna a lista com descrições organizadas



def carregar_vulnerabilidades_do_relatorio_csv(caminho_arquivo):
    """
    Carrega e extrai informações de vulnerabilidades e hosts afetados a partir de um arquivo de relatório.

    Parâmetros:
    - caminho_arquivo (str): O caminho completo do arquivo de relatório contendo as vulnerabilidades.

    Retorno:
    - list: Uma lista de dicionários com dados de cada vulnerabilidade.
    """
    vulnerabilities = []

    with open(caminho_arquivo, 'r', encoding="utf-8") as file:
        vulnerability = None
        severity = None
        collecting_hosts = False
        affected_hosts = []

        for line in file:
            line = line.strip()

            # Identifica nova vulnerabilidade
            match_vuln = re.match(r'^Vulnerabilidade:\s*(.+)', line)
            if match_vuln:
                # Salva a anterior
                if vulnerability:
                    vulnerabilities.append({
                        "Vulnerabilidade": vulnerability,
                        "Severidade": severity,
                        "Total de Hosts Afetados": len(affected_hosts),
                        "Hosts": affected_hosts
                    })
                vulnerability = match_vuln.group(1).strip()
                severity = None
                affected_hosts = []
                collecting_hosts = False
                continue

            # Captura a severidade
            match_sev = re.match(r'^Severidade:\s*(.+)', line)
            if match_sev:
                severity = match_sev.group(1).strip().lower()
                collecting_hosts = False
                continue

            # Detecta início da lista de hosts
            if line.startswith("Hosts Afetados:"):
                collecting_hosts = True
                continue

            # Coleta os hosts após o título
            if collecting_hosts and line and not line.startswith("Vulnerabilidade:"):
                affected_hosts.append(line.strip())

        # Adiciona a última vulnerabilidade
        if vulnerability:
            vulnerabilities.append({
                "Vulnerabilidade": vulnerability,
                "Severidade": severity,
                "Total de Hosts Afetados": len(affected_hosts),
                "Hosts": affected_hosts
            })

    return vulnerabilities



def gerar_latex_vulnerabilidades(vulnerabilidades, json_path='data/vulnerabilidades_servidores.json'):
    # Garante que o diretório existe
    pasta_destino = 'data/relatoriosprontos'
    os.makedirs(pasta_destino, exist_ok=True)

    # Carrega descrições e soluções do arquivo JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        dados_vulnerabilidades = json.load(f)
    
    # Mapeia cada vulnerabilidade por nome
    mapa_vuln = {v['Vulnerabilidade']: v for v in dados_vulnerabilidades}

    # Agrupa por categoria
    categorias = defaultdict(list)
    for v in vulnerabilidades:
        nome = v['Vulnerabilidade']
        info = mapa_vuln.get(nome, {})
        categoria = info.get('Categoria', 'Categoria Desconhecida')
        categorias[categoria].append(v)

    # Início do conteúdo LaTeX
    conteudo = r'''
\section{Análise de Vulnerabilidades}
\noindent Este capítulo apresenta as vulnerabilidades identificadas, organizadas por categorias temáticas. Para cada vulnerabilidade, são fornecidas informações descritivas, sugestões de mitigação e os hosts afetados.

\vspace{1cm}
'''

    for categoria, vulns in categorias.items():
        conteudo += f'''
%===============================
\\subsection{{{categoria}}}
%===============================
'''

        for v in vulns:
            titulo = v['Vulnerabilidade']
            total = v['Total de Hosts Afetados']
            hosts = v['Hosts']
            imagem = v.get('Imagem', None)

            # Recupera descrição e solução
            dados = mapa_vuln.get(titulo, {})
            descricao = dados.get('Descrição', 'Descrição não fornecida.')
            solucao = dados.get('Solução', 'Solução não fornecida.')

            conteudo += f'''
%--------------------------------
\\subsubsection*{{\\textbf{{{titulo}}}}}
%--------------------------------
\\vspace{{0.3em}}

\\textbf{{Descrição}}\\\\
{descricao}


\\textbf{{Solução}}\\\\
{solucao}

\\vspace{{0.5em}}

\\textbf{{Total de Hosts Afetados:}} {total}

\\vspace{{0.5em}}

\\textbf{{Instâncias Afetadas:}}
\\begin{{itemize}}
'''
            for host in hosts:
                conteudo += f'    \\item \\url{{{host}}}\n'

            conteudo += '\\end{itemize}\n\\vspace{1.5em}\n\\hrule\n\\vspace{1em}\n'

    # Final do documento
    conteudo += r'\end{document}'

    return conteudo



def gerar_conteudo_latex_para_vulnerabilidades_csv(vulnerabilidades, vulnerabilidades_dados, descritivo_vulnerabilidades):
    """
    Gera o conteúdo em LaTeX para as vulnerabilidades, corrigindo duplicações, preservando a capitalização,
    e ordenando categorias e subcategorias em ordem alfabética. A categoria "Outras Vulnerabilidades Críticas e Explorações"
    é sempre exibida por último.

    Parâmetros:
    - vulnerabilidades (list): Lista de vulnerabilidades extraídas do arquivo.
    - vulnerabilidades_dados (list): Dados adicionais sobre as vulnerabilidades.
    - descritivo_vulnerabilidades (list): Descrições de categorias e subcategorias.

    Retorno:
    - str: Conteúdo formatado em LaTeX.
    """
    def padronizar(texto):
        """Remove espaços extras e converte para lowercase para padronizar."""
        return texto.strip().lower() if texto else ""

    conteudo = ""  # Inicializa o conteúdo LaTeX
    anexo_conteudo = ""  # Inicializa o conteúdo do Anexo A
    categorias = {}  # Dicionário para organizar as vulnerabilidades por categoria e subcategoria
    categorias_formatadas = {}  # Para armazenar os nomes originais (com capitalização correta)
    vulnerabilidades_sem_categoria = []  # Lista para vulnerabilidades sem categoria

    
    # %-------------- INÍCIO DO AGRUPAMENTO DE VULNERABILIDADES --------------
    for v in vulnerabilidades:
        vulnerabilidade_nome = v["Vulnerabilidade"]
        total_affected_uris = v["Total de Hosts Afetados"]
        affected_uris = v["Hosts"]

        # Busca os dados adicionais da vulnerabilidade
        dados_vuln = next((vuln for vuln in vulnerabilidades_dados if vuln["Vulnerabilidade"] == vulnerabilidade_nome), None)
        
        if dados_vuln:
            categoria = padronizar(dados_vuln["Categoria"])
            subcategoria = padronizar(dados_vuln["Subcategoria"])
            descricao = dados_vuln["Descrição"]
            solucao = dados_vuln["Solução"]
            imagem = dados_vuln.get("Imagem", "")

            # Salva a versão formatada correta das categorias/subcategorias
            categorias_formatadas[categoria] = dados_vuln["Categoria"]
            categorias_formatadas[subcategoria] = dados_vuln["Subcategoria"]

            # Organiza as categorias e subcategorias
            if categoria not in categorias:
                categorias[categoria] = {}

            if subcategoria not in categorias[categoria]:
                categorias[categoria][subcategoria] = []

            categorias[categoria][subcategoria].append({
                "Vulnerabilidade": vulnerabilidade_nome,
                "Descricao": descricao,
                "Solucao": solucao,
                "Imagem": imagem,
                "Total de URI Afetadas": total_affected_uris,
                "URI Afetadas": affected_uris,
            })
        else:
            vulnerabilidades_sem_categoria.append(vulnerabilidade_nome)
    # %-------------- FIM DO AGRUPAMENTO DE VULNERABILIDADES --------------

    # %-------------- ORDENAR CATEGORIAS --------------
    categorias_ordenadas = sorted(categorias.keys(), key=lambda x: categorias_formatadas[x])
    if "outras vulnerabilidades críticas e explorações" in categorias_ordenadas:
        categorias_ordenadas.remove("outras vulnerabilidades críticas e explorações")
        categorias_ordenadas.append("outras vulnerabilidades críticas e explorações")

    # %-------------- INÍCIO DA GERAÇÃO DO CONTEÚDO LATEX --------------
    for categoria_padronizada in categorias_ordenadas:
        categoria_formatada = categorias_formatadas[categoria_padronizada]
        
        # Busca a descrição da categoria no descritivo
        descricao_categoria = next(
            (item["descricao"] for item in descritivo_vulnerabilidades 
             if padronizar(item.get("categoria")) == categoria_padronizada), 
            "Descrição não disponível."
        )
        conteudo += f"%-------------- INÍCIO DA CATEGORIA {categoria_formatada} --------------\n"
        conteudo += f"\\subsection{{{categoria_formatada}}}\n{descricao_categoria}\n\n"

        # Ordenar subcategorias
        subcategorias = categorias[categoria_padronizada]
        for subcategoria_padronizada in sorted(subcategorias.keys(), key=lambda x: categorias_formatadas[x]):
            subcategoria_formatada = categorias_formatadas[subcategoria_padronizada]

            # Busca a descrição da subcategoria no descritivo
            descricao_subcategoria = next(
                (item["descricao"] for item in descritivo_vulnerabilidades 
                 if padronizar(item.get("subcategoria")) == subcategoria_padronizada), 
                "Descrição não disponível."
            )
            conteudo += f"%-------------- INÍCIO DA SUBCATEGORIA {subcategoria_formatada} --------------\n"
            conteudo += f"\\subsubsection{{{subcategoria_formatada}}}\n{descricao_subcategoria}\n\n"
            conteudo += "\\begin{enumerate}\n"

            for v in subcategorias[subcategoria_padronizada]:
                conteudo += f"%-------------- INÍCIO DA VULNERABILIDADE {v['Vulnerabilidade']} --------------\n"
                conteudo += f"\\item \\textbf{{{v['Vulnerabilidade']}}}\\\\\n"
                if v["Imagem"]:
                    conteudo += (
                        r"""
                        \begin{figure}[h!]
                        \centering
                        \includegraphics[width=0.8\textwidth]{""" + v["Imagem"] + r"""}
                        \end{figure}
                        \FloatBarrier
                        """
                    )
                conteudo += f"\\textbf{{Descrição:}} {v['Descricao']}\n\n"
                conteudo += f"\\textbf{{Solução:}} {v['Solucao']}\n\n"
                conteudo += f"\\textbf{{Total de URIs Afetadas:}} {v['Total de URI Afetadas']}\n\n"

                # Lida com a exibição de instâncias afetadas
                if len(v["URI Afetadas"]) > 10:
                    conteudo += "\\textbf{Instâncias Afetadas (parcial):}\n\\begin{itemize}\n"
                    for uri in v["URI Afetadas"][:10]:
                        conteudo += f"    \\item \\url{{{uri}}}\n"
                    conteudo += "\\end{itemize}\n"
                    conteudo += (
                        "A lista completa das aplicações que possuem esta vulnerabilidade pode ser "
                        f"encontrada no \\hyperref[anexoA]{{Anexo A}}.\n\n"
                    )

                    # Adiciona o restante ao anexo
                    anexo_conteudo += f"%-------------- INÍCIO DO ANEXO PARA {v['Vulnerabilidade']} --------------\n"
                    anexo_conteudo += f"\\subsubsection*{{{v['Vulnerabilidade']}}}\n"
                    anexo_conteudo += "\\begin{multicols}{3}\n\\small\n\\begin{itemize}\n"
                    for uri in v["URI Afetadas"]:
                        anexo_conteudo += f"    \\item \\url{{{uri}}}\n"
                    anexo_conteudo += "\\end{itemize}\n\\end{multicols}\n\n"
                else:
                    conteudo += "\\textbf{Instâncias Afetadas:}\n\\begin{itemize}\n"
                    for uri in v["URI Afetadas"]:
                        conteudo += f"    \\item \\url{{{uri}}}\n"
                    conteudo += "\\end{itemize}\n\n"
                conteudo += f"%-------------- FIM DA VULNERABILIDADE {v['Vulnerabilidade']} --------------\n"

            conteudo += "\\end{enumerate}\n"
            conteudo += f"%-------------- FIM DA SUBCATEGORIA {subcategoria_formatada} --------------\n"

        conteudo += f"%-------------- FIM DA CATEGORIA {categoria_formatada} --------------\n"

    # Adiciona as vulnerabilidades sem categoria, se existirem
    if vulnerabilidades_sem_categoria:
        conteudo += "%-------------- INÍCIO DAS VULNERABILIDADES SEM CATEGORIA --------------\n"
        conteudo += "\\section{Vulnerabilidades sem Categoria}\n\\begin{itemize}\n"
        for vuln in vulnerabilidades_sem_categoria:
            conteudo += f"    \\item {vuln}\n"
        conteudo += "\\end{itemize}\n"
        conteudo += "%-------------- FIM DAS VULNERABILIDADES SEM CATEGORIA --------------\n"

    # Adiciona o Anexo A, se necessário
    if anexo_conteudo:
        conteudo += "%-------------- INÍCIO DO ANEXO A --------------\n"
        conteudo += "\\section*{Anexo A}\n\\label{anexoA}\n"
        conteudo += anexo_conteudo
        conteudo += "%-------------- FIM DO ANEXO A --------------\n"

    return conteudo