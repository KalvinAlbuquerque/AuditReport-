#VARIÁVEIS GLOBAIS
CAMINHO_RELATORIOS_JSON = "data/arquivos_json"
from analysis.vulnerability_handler import processar_relatorio_csv,processar_relatorio_json
from utils.json_utils import *
# Executa a função para criar a interface
if __name__ == "__main__":
    
    processar_relatorio_csv("C:/Users/kalvi/Code/relatorios-vuln/back-end/data/arquivos_csv", "C:/Users/kalvi/Code/relatorios-vuln/back-end/data/relatórios_prontos", "../shared/relatorios/Exemplo/")
    #processar_relatorio_json("C:/Users/kalvi/Code/relatorios-vuln/back-end/data/arquivos_json", "C:/Users/kalvi/Code/relatorios-vuln/back-end/data/relatórios_prontos", "../shared/relatorios/Exemplo/")


