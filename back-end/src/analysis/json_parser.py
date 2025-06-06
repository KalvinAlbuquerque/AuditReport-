"""
Arquivo destinado a armazenar funções relacionadas à extração e análise de dados 
de arquivos JSON, incluindo a formatação de URLs, a coleta de vulnerabilidades e 
informações associadas, além de manipulação de dados relacionados a relatórios de 
segurança.

Funções presentes:
- Extração de targets e domínios a partir dos arquivos JSON.
- Agrupamento de vulnerabilidades por nome e plugin_id.
- Contagem de vulnerabilidades por tipo de risco (Crítico, Alto, Médio, Baixo).
- Formatação de URIs relativas para URLs absolutas.
"""


##LIBS
from collections import defaultdict
import json
import re
from urllib.parse import urlparse, urljoin
import glob
import os
from typing import List
import json
from pathlib import Path

from ..utils.utils import contar_riscos, limpar_protocolos_url
from ..utils.json_utils import carregar_json, carregar_json_utf


CAMINHO_RELATORIOS_JSON = "data/arquivos_json"
CAMINHO_RELATORIOS_CSV = "data/arquivos_csv"


##FUNÇÕES

def localizar_arquivos(diretorio_path: str, formato: str) -> List[str]:
    """
    Função para encontrar todos os arquivos de terminada extensão em um diretório especificado.

    :param diretorio_path: O caminho para o diretório onde os arquivos estão localizados.
    :param formato: A extensão dos arquivos a serem encontrados (ex: 'json', 'txt', 'csv').
    :return: Lista de caminhos completos para os arquivos encontrados.
    """
    # Verifica se o diretório existe
    if not os.path.exists(diretorio_path):
        print(f"O diretório {diretorio_path} não existe.")
        return []
    
    # Encontrar todos os arquivos no diretório
    files = glob.glob(os.path.join(diretorio_path, "*." + formato))
    if not files:
        print(f"Nenhum arquivo com a extensão .{formato} encontrado no diretório {diretorio_path}.")
        return []
    
    # Converter os caminhos para o formato POSIX (com forward slashes)
    files_normalized = [Path(file).as_posix() for file in files]
    return files_normalized

def extrair_targets(json_files: List[str]) -> List[str]:
    """
    Extrai os targets (domínios) a partir dos arquivos JSON, retornando uma lista de targets únicos.

    Parâmetros:
    - json_files (List[str]): Lista com os caminhos dos arquivos JSON.

    Retorna:
    - List[str]: Lista com os targets extraídos dos arquivos JSON, sem duplicatas.
    """
    targets = set()  # Usando um conjunto para evitar duplicatas
    for json_file in json_files:
        
        data = carregar_json(json_file)
        target = data.get('scan', {}).get('target', 'Não disponível')
        
        if target != 'Não disponível':
            targets.add(target)  # Adiciona o target ao conjunto
            
    return list(targets)  # Retorna uma lista com os targets únicos

def obter_vulnerabilidades_comum(json_files: List[str]) -> dict:
    """
    Obtém as vulnerabilidades comuns entre os arquivos JSON, agrupando-as por nome e plugin_id.

    Parâmetros:
    - json_files (List[str]): Lista com os caminhos dos arquivos JSON.

    Retorna:
    - dict: Dicionário com vulnerabilidades agrupadas por (nome, plugin_id) e as URIs afetadas.
    """
    common_vulnerabilities = defaultdict(list)
    for json_file in json_files:
        data = carregar_json(json_file)
        target = data.get('scan', {}).get('target', 'Não disponível')
        
        for finding in data.get('findings', []):
            risk_factor = finding.get('risk_factor', 'Não disponível')
            uri = finding.get('uri', 'Não disponível')
            name = finding.get('name', 'Não disponível')
            plugin_id = finding.get('plugin_id', 'Não disponível')
            if "info" not in risk_factor:
                #Formatando as URI para possuir apenas o domínio e sem duplicatas
                formatted_uri = formatar_uri(target, uri)
                common_vulnerabilities[(name, plugin_id)].append(formatted_uri)
    return common_vulnerabilities

def extrair_dominio(target: str) -> str:
    """
    A função recebe um endereço URL (target) e retorna o domínio base, ou seja, o esquema (http/https) 
    e o nome do domínio (netloc) da URL.
    
    Parâmetros:
    target (str): A URL de onde se quer extrair o domínio.
    
    Retorna:
    str: O domínio da URL no formato 'http(s)://dominio.com'
    """
    parsed_url = urlparse(target)  # Faz o parsing da URL
    return f"{parsed_url.scheme}://{parsed_url.netloc}"  # Retorna o esquema e o domínio

def formatar_uri(target: str, uri: str) -> str:
    """
    A função recebe o target (uma URL base) e uma URI (um caminho ou URL relativa), 
    e retorna a URL completa, levando em conta se a URI é relativa ou já contém domínio.

    Parâmetros:
    target (str): A URL base (domínio) a ser usada caso a URI seja relativa.
    uri (str): A URI (caminho ou URL relativa) que será combinada com o target.
    
    Retorna:
    str: A URL formatada completa, seja absoluta ou uma combinação do target com a URI.
    """
    target_domain = extrair_dominio(target)  # Extrai o domínio base do target
    parsed_uri = urlparse(uri)  # Faz o parsing da URI para analisar seus componentes
    
    # Verifica se a URI não possui um domínio (netloc vazio), significando que é uma URI relativa
    if not parsed_uri.netloc:
        return urljoin(target_domain, uri)  # Combina a URL base com a URI para formar uma URL completa
    else:
        return target_domain  # Se a URI já for uma URL absoluta, retorna apenas o domínio do target
    
def contar_vulnerabilidades(json_files: List[str]) -> dict:
    """
    Conta o número de vulnerabilidades por tipo (Critical, High, Medium, Low) em arquivos JSON.

    Parâmetros:
    - json_files (List[str]): Lista com os caminhos dos arquivos JSON.

    Retorna:
    - dict: Dicionário com contagem das vulnerabilidades por tipo.
    """
    risk_factor_counts = {'High': 0, 'Critical': 0, 'Low': 0, 'Medium': 0}
    for json_file in json_files:
        data = carregar_json(json_file)
        for finding in data.get('findings', []):
            risk_factor = finding.get('risk_factor', 'Não disponível')
            if "info" not in risk_factor:
                if risk_factor.lower() == 'high':
                    risk_factor_counts['High'] += 1
                elif risk_factor.lower() == 'critical':
                    risk_factor_counts['Critical'] += 1
                elif risk_factor.lower() == 'low':
                    risk_factor_counts['Low'] += 1
                elif risk_factor.lower() == 'medium':
                    risk_factor_counts['Medium'] += 1
    return risk_factor_counts

def montar_conteudo_latex(caminho_arquivo, vulnerabilidades_dados, caminho_relatorio_exemplo: str):
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
    vulnerabilidades = carregar_vulnerabilidades_do_relatorio(caminho_arquivo)
    
    descritivos_vulnerabilidade = carregar_descritivo_vulnerabilidades(f"{caminho_relatorio_exemplo}/descritivo_vulnerabilidades.json")

    # Gerar o conteúdo LaTeX para as vulnerabilidades carregadas
    conteudo_latex = gerar_conteudo_latex_para_vulnerabilidades(vulnerabilidades, vulnerabilidades_dados, descritivos_vulnerabilidade)
    

    return conteudo_latex  # Retorna o conteúdo LaTeX completo

def carregar_vulnerabilidades_do_relatorio(caminho_arquivo):
    """
    Carrega e extrai informações de vulnerabilidades a partir de um arquivo de relatório.

    Parâmetros:
    - caminho_arquivo (str): O caminho completo do arquivo de relatório contendo as vulnerabilidades.

    Retorno:
    - list: Uma lista de dicionários, onde cada dicionário contém os dados de uma vulnerabilidade.
    """
    
    vulnerabilities = []  # Lista para armazenar as vulnerabilidades extraídas

    with open(caminho_arquivo, 'r', encoding="utf-8") as file:
        vulnerability = None  
        total_affected_uris = None  
        affected_uris = []  

        
        for line in file:
            line = line.strip()  # Remove espaços em branco no início e fim de cada linha
            
            match_vulnerability = re.match(r"^Vulnerabilidade:(.*)", line)
            if match_vulnerability:
                # Quando encontra uma nova vulnerabilidade, armazena a anterior (se houver) e reinicia os dados
                if vulnerability:
                    vulnerabilities.append({
                        "Vulnerabilidade": vulnerability,
                        "Total de URI Afetadas": total_affected_uris,
                        "URI Afetadas": affected_uris
                    })
                vulnerability = match_vulnerability.group(1).strip()  # Extrai o nome da vulnerabilidade
                affected_uris = []  # Reseta as URIs afetadas para a nova vulnerabilidade
                continue

            match_total_uris = re.match(r"^Total de URI Afetadas:(\d+)", line)
            if match_total_uris:
                total_affected_uris = int(match_total_uris.group(1))  # Extrai o número de URIs afetadas
                continue

            match_uris = re.match(r"^http(s)?://.*", line)
            if match_uris:
                affected_uris.append(line)  # Adiciona a URI à lista de afetadas

        # Ao final, adiciona a última vulnerabilidade lida
        if vulnerability:
            vulnerabilities.append({
                "Vulnerabilidade": vulnerability,
                "Total de URI Afetadas": total_affected_uris,
                "URI Afetadas": affected_uris
            })

    return vulnerabilities  # Retorna a lista de vulnerabilidades extraídas

def carregar_descritivo_vulnerabilidades(caminho_arquivo):
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

def gerar_conteudo_latex_para_vulnerabilidades(vulnerabilidades, vulnerabilidades_dados, descritivo_vulnerabilidades):
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
        total_affected_uris = v["Total de URI Afetadas"]
        affected_uris = v["URI Afetadas"]

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
                conteudo += f"\\item \\textbf{{{v['Vulnerabilidade']}}}\n"
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

def extrair_dados_vulnerabilidades(data: dict) -> dict:
    """
    Extrai os dados de vulnerabilidade de um arquivo JSON.
    
    Parâmetros:
    - data (dict): Dados do arquivo JSON.
    
    Retorno:
    - dict: Dados de vulnerabilidade extraídos, incluindo nome do site e contagem de riscos.
    """
    target = data.get('scan', {}).get('target', 'Não disponível')
    if target == 'Não disponível':
        return None

    risk_factor_counts = contar_riscos(data.get('findings', []))
    cleaned_target = limpar_protocolos_url(target)
    total = sum(risk_factor_counts.values())
    
    return {
        'Site': cleaned_target,
        'Critical': risk_factor_counts['Critical'],
        'High': risk_factor_counts['High'],
        'Medium': risk_factor_counts['Medium'],
        'Low': risk_factor_counts['Low'],
        'Total': total
    }