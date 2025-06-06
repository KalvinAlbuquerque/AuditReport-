# back-end/src/main.py

from .utils.config import Config
config = Config("config.json")

from .api.tenable_api import TenableApi
from pathlib import Path
from .analysis.vulnerability_handler import *
from .report.report_generator import terminar_relatorio_preprocessado, compilar_latex
import time
from .plot.plot import gerar_Grafico_Quantitativo_Vulnerabilidades_Por_Site, gerar_grafico_donut


from .routes.scans.scans_webapp import scans_bp
from .routes.listas.listas import listas_bp
from .routes.relatorios.relatorios import relatorios_bp
from .routes.relatorios.gerenciarVulnerabilidades import gerenciar_vulnerabilidades_bp # Nova importação
from .routes.scans.scans_vm import scans_vm_bp
from flask import Flask

# --- Mova a criação da instância 'app' e o registro dos blueprints para o escopo global ---
app = Flask(__name__)

app.register_blueprint(scans_bp)
app.register_blueprint(listas_bp)
app.register_blueprint(scans_vm_bp)
app.register_blueprint(relatorios_bp)
app.register_blueprint(gerenciar_vulnerabilidades_bp)
# -----------------------------------------------------------------------------------------

# A função 'main' pode ser removida se não for usada para mais nada, ou mantida para outros propósitos.
# Mas a execução da app.run() deve ser no if __name__ == "__main__"
# def main():
#     print(app.url_map)
#     app.run(debug=True)

if __name__ == "__main__":
    print(app.url_map) # Opcional: para ver as rotas no terminal
    app.run(debug=True, host='0.0.0.0', port=5000) # <--- Use host e port aqui também para garantir execução local