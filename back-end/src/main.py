from utils.config import Config
config = Config("config.json")

from api.tenable_api import TenableApi
from pathlib import Path
from analysis.vulnerability_handler import *
from report.report_generator import terminar_relatorio_preprocessado, compilar_latex
import time
from plot.plot import gerar_Grafico_Quantitativo_Vulnerabilidades_Por_Site, gerar_grafico_donut


from routes.scans.scans_webapp import scans_bp
from routes.listas.listas import listas_bp
from routes.relatorios.relatorios import relatorios_bp
from routes.relatorios.gerenciarVulnerabilidades import gerenciar_vulnerabilidades_bp # Nova importação
from routes.scans.scans_vm import scans_vm_bp
from flask import Flask

def main():

    app = Flask(__name__)

    app.register_blueprint(scans_bp)
    app.register_blueprint(listas_bp)
    app.register_blueprint(scans_vm_bp)
    app.register_blueprint(relatorios_bp)
    app.register_blueprint(gerenciar_vulnerabilidades_bp)


    print(app.url_map)

    app.run(debug=True)



    # tenable_api = TenableApi()

    # nome_da_pasta = "GABP"
    # usuario = "kalvin.santos@salvador.ba.gov.br"

    # scans = tenable_api.get_web_app_scans_from_folder_of_user(nome_da_pasta, usuario)

    # print(scans)

    # pasta_destino_exports_json = f"{config.caminho_shared_jsons}/{usuario}/{nome_da_pasta}/"
    # pasta_destino_relatorio_preprocessado = f"{config.caminho_shared_relatorios}/{usuario}/{nome_da_pasta}/relatorio_preprocessado"

    # destino = Path(pasta_destino_exports_json)
    # destino.mkdir(parents=True, exist_ok=True)

    # destino = Path(pasta_destino_relatorio_preprocessado)
    # destino.mkdir(parents=True, exist_ok=True)

    # destino = Path(f"{pasta_destino_relatorio_preprocessado}/RelatorioPronto/")
    # destino.mkdir(parents=True, exist_ok=True)



    # tenable_api.download_scans_results_json(pasta_destino_exports_json, scans)

    # print(pasta_destino_exports_json)

    # extrair_dados_relatorios_json(pasta_destino_exports_json, pasta_destino_relatorio_preprocessado, config.caminho_shared_relatorios_exemplo)

    # extrair_quantidades_vulnerabilidades_por_site(f"{pasta_destino_relatorio_preprocessado}/vulnerabilidades_agrupadas_por_site.csv", pasta_destino_exports_json)

    # terminar_relatorio_preprocessado("Secretaria de Saúde", "SMS", "01 de Janeiro de 2023", "31 de Dezembro de 2023", "2023", "Dezembro", pasta_destino_relatorio_preprocessado, f"{pasta_destino_relatorio_preprocessado}/relatorio_pronto.tex", config.caminho_shared_relatorios_exemplo)

    # gerar_Grafico_Quantitativo_Vulnerabilidades_Por_Site(
    #             f"{pasta_destino_relatorio_preprocessado}/vulnerabilidades_agrupadas_por_site.csv", f"{pasta_destino_relatorio_preprocessado}/RelatorioPronto/assets/images-was/Vulnerabilidades_x_site.png", "decrescente"
    #         )

    # compilar_latex(f"{pasta_destino_relatorio_preprocessado}/RelatorioPronto/main.tex", f"{pasta_destino_relatorio_preprocessado}/RelatorioPronto/")
    # compilar_latex(f"{pasta_destino_relatorio_preprocessado}/RelatorioPronto/main.tex", f"{pasta_destino_relatorio_preprocessado}/RelatorioPronto/")

if __name__ == "__main__":
    
    main()



    