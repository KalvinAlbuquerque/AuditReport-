import pandas as pd
import matplotlib.pyplot as plt

import pandas as pd
import matplotlib.pyplot as plt

def gerar_Grafico_Quantitativo_Vulnerabilidades_Por_Site(input_file: str, graph_output_path: str, ordem: str = "descendente"):
    """
    Gera um gráfico de barras do quantitativo de vulnerabilidades por site e salva em um arquivo PNG.

    Args:
        input_file (str): Caminho do arquivo de entrada (CSV não usado no momento, mas reservado).
        graph_output_path (str): Caminho para salvar o arquivo PNG do gráfico.
    """
    # Carrega os dados do CSV em um DataFrame
    df = pd.read_csv(input_file)

    # Define se a ordenação será crescente ou decrescente
    ordem_crescente = True if ordem.lower() == "crescente" else False

    # Ordena os dados pela coluna 'Total' conforme especificado
    df_sorted = df.sort_values(by='Total', ascending=ordem_crescente)

    # Configura o gráfico
    plt.figure(figsize=(20, 10))
    plt.bar(df_sorted['Site'], df_sorted['Total'], color='skyblue')

    # Adiciona títulos e rótulos
    plt.title('Quantitativo de Vulnerabilidades por Site', fontsize=18)
    plt.xlabel('Sites', fontsize=16)
    plt.ylabel('Total de Vulnerabilidades', fontsize=16)

    plt.xticks(rotation=45, ha='right', fontsize=13)  # Rótulos a 45 graus e alinhamento à direita
    plt.yticks(fontsize=15)

    # Ajusta o layout para evitar cortes
    plt.tight_layout()

    # Salva o gráfico como arquivo PNG
    plt.savefig(graph_output_path)
    print(f"Gráfico salvo em: {graph_output_path}")
    
    
def gerar_grafico_donut(vulnerabilidades):
    """
    Gera um gráfico de pizza com buraco (donut) para as vulnerabilidades por tipo.

    Args:
        vulnerabilidades (dict): Dicionário com as contagens das vulnerabilidades por tipo.
    """
    # Labels e valores para o gráfico de pizza
    labels = vulnerabilidades.keys()
    sizes = vulnerabilidades.values()

    # Definir cores para os tipos de vulnerabilidade
    cores = ['#FF0000', '#FF4C4C', '#FFFF00', '#0000FF']  # Vermelho forte, vermelho normal, amarelo, azul

    # Configuração do gráfico de pizza (donut)
    fig, ax = plt.subplots(figsize=(8, 8))  # Tamanho da figura
    wedges, texts, autotexts = ax.pie(
        sizes, 
        labels=labels, 
        autopct='%d',  # Exibe valores inteiros, sem porcentagem
        startangle=90, 
        wedgeprops={'width': 0.4, 'edgecolor': 'black'},  # Cria o efeito donut com o "buraco"
        colors=cores  # Usando as cores definidas
    )

    # Ajuste no aspecto para garantir um gráfico circular
    ax.axis('equal')

    # Adiciona título
    plt.title("Distribuição de Vulnerabilidades por Tipo", fontsize=16)

    # Ajusta o espaçamento dos rótulos
    for text in texts:
        text.set_fontsize(12)
        text.set_horizontalalignment('center')  # Centraliza os rótulos

    # Exibe o gráfico
    plt.tight_layout()
    plt.show()