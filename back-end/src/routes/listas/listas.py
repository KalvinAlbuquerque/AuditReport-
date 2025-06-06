from flask import Blueprint, jsonify, request, send_file
from flask_cors import cross_origin

import time

from ...utils.config import Config
from ...api.tenable_api import TenableApi
from ...database.database import Database
import os

from ...analysis.vulnerability_handler import *
from ...report.report_generator import terminar_relatorio_preprocessado, compilar_latex
from ...plot.plot import gerar_Grafico_Quantitativo_Vulnerabilidades_Por_Site
from bson import ObjectId
import shutil

tenable_api = TenableApi()
config = Config("config.json")

listas_bp = Blueprint('listas', __name__, url_prefix='/listas')

@listas_bp.route('/criarLista/', methods=['POST'])
@cross_origin(origins=["http://localhost:5173", "127.0.0.1"])
def criarLista():
    try:
        data = request.get_json()

        if not data:
            return 'Sem dados no request', 520

        nomeLista = data.get("nomeLista")

        if not nomeLista:
            return 'Campo "nomeLista" é obrigatório.', 400

        db = Database()

        # Verifica se já existe uma lista com esse nome
        lista_existente = db.find_one("listas", {"nomeLista": nomeLista})

        if lista_existente:
            db.close()
            return f'Já existe uma lista com o nome "{nomeLista}".', 409

        # Criação da nova lista
        id_lista = db.insert_one("listas", {
            "nomeLista": nomeLista,
            "pastas_scans_webapp": None,
            "id_scan": None,
            "historyid_scanservidor": None,
            "nomeScanStoryId": None,
            "scanStoryIdCriadoPor": None,
            "relatorioGerado": False
        }).inserted_id

        pasta_scan = f"{config.caminho_shared_jsons}/{id_lista}/"

        db.update_one("listas", {"_id": id_lista}, {"pastas_scans_webapp": pasta_scan})

        os.makedirs(pasta_scan, exist_ok=True)

        db.close()

        return "OK", 200

    except Exception as e:
        return str(e), 520
    
# @listas_bp.route('/adicionarWAPPScanALista/', methods=['POST'])
# @cross_origin(origins=["http://localhost:5173", "127.0.0.1"])
# def adicionarWAPPScanALista():

#     try:
#         data = request.get_json()

#         if not data:
#             return 'Sem dados', 520

#         nome_lista = data.get("nomeLista")
#         scans = data.get("scans")

#         print(scans)

#         if not nome_lista or not scans:
#             return 'Erro dados incompletos', 520

#         if not isinstance(scans, dict):
#             return 'Erro instancia', 520
        
#         db = Database()

#         documento = db.find_one("listas", {"nomeLista": nome_lista})

#         if not documento:
#             return "Documento não encontrado", 404
        
#         tenable_api.download_scans_results_json(
#             documento["pastas_scans_webapp"],
#             scans
#         )
        
#         db.close()

#         return '', 200

#     except Exception as e:
#         return str(e), 520

@listas_bp.route('/getScansDeLista/', methods=['POST'])
@cross_origin(origins=["http://localhost:5173", "127.0.0.1"])
def getScansDeLista():
    try:
        data = request.get_json()

        if not data:
            return 'Sem dados', 520

        nome_lista = data.get("nomeLista")

        if not nome_lista:
            return 'Nome da lista não fornecido', 520

        db = Database()

        documento = db.find_one("listas", {"nomeLista": nome_lista})

        db.close()

        if not documento:
            return "Lista não encontrada", 404
        
        scans = []

        pasta_scans = documento["pastas_scans_webapp"]

        if not os.path.exists(pasta_scans):
            return "Pasta de scans não encontrada", 404

        for arquivo in os.listdir(pasta_scans):
            if arquivo.endswith(".json"):
                caminho_arquivo = os.path.join(pasta_scans, arquivo)
                with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                    conteudo = json.load(f)
                    nome_scan = conteudo.get("config", {}).get("name")
                    if nome_scan:
                        scans.append(nome_scan)

        return scans, 200

    except Exception as e:
        return str(e), 520
    

@listas_bp.route('/getVMScansDeLista/', methods=['POST'])
@cross_origin(origins=["http://localhost:5173", "127.0.0.1"])
def getVMScansDeLista():
    try:
        data = request.get_json()

        if not data:
            return 'Sem dados', 520

        nome_lista = data.get("nomeLista")

        if not nome_lista:
            return 'Nome da lista não fornecido', 520

        db = Database()

        documento = db.find_one("listas", {"nomeLista": nome_lista})

        db.close()

        if not documento:
            return "Lista não encontrada", 404

        nomeScanStoryId = documento["nomeScanStoryId"]
        criadoPor = documento["scanStoryIdCriadoPor"]
        id_scan = documento["id_scan"]

        if not nomeScanStoryId or not criadoPor:
            return "Não existem dados de VM para esta lista.", 404

        return [nomeScanStoryId, criadoPor, id_scan], 200

    except Exception as e:
        return str(e), 520

@listas_bp.route('/limparScansDeLista/', methods=['POST'])
@cross_origin(origins=["http://localhost:5173", "127.0.0.1"])
def limparScansDeLista():
    try:
        data = request.get_json()

        if not data:
            return 'Sem dados', 520

        nome_lista = data.get("nomeLista")

        if not nome_lista:
            return 'Nome da lista não fornecido', 520

        db = Database()

        documento = db.find_one("listas", {"nomeLista": nome_lista})

        db.close()

        if not documento:
            return "Lista não encontrada", 404
        
        pasta_scans = documento["pastas_scans_webapp"]

        if os.path.exists(pasta_scans):
            for arquivo in os.listdir(pasta_scans):
                caminho_arquivo = os.path.join(pasta_scans, arquivo)
                if os.path.isfile(caminho_arquivo) or os.path.islink(caminho_arquivo):
                    os.unlink(caminho_arquivo)
                elif os.path.isdir(caminho_arquivo):
                    shutil.rmtree(caminho_arquivo)

        return 'OK', 200

    except Exception as e:
        return str(e), 520
    
@listas_bp.route('/limparVMScansDeLista/', methods=['POST'])
@cross_origin(origins=["http://localhost:5173", "127.0.0.1"])
def limparVMScansDeLista():
    try:
        data = request.get_json()

        if not data:
            return 'Sem dados', 520

        nome_lista = data.get("nomeLista")

        if not nome_lista:
            return 'Nome da lista não fornecido', 520

        db = Database()

        documento = db.find_one("listas", {"nomeLista": nome_lista})

        if not documento:
            return "Lista não encontrada", 404
        
        db.update_one(
            "listas",
            {"_id": ObjectId(documento["_id"])},
            {"id_scan": None}
        )
        
        db.update_one(
            "listas",
            {"_id": ObjectId(documento["_id"])},
            {"historyid_scanservidor": None}
        )

        db.update_one(
            "listas",
            {"_id": ObjectId(documento["_id"])},
            {"nomeScanStoryId": None}
        )

        db.update_one(
            "listas",
            {"_id": ObjectId(documento["_id"])},
            {"scanStoryIdCriadoPor": None}
        )

        db.close()

        return 'OK', 200

    except Exception as e:
        return str(e), 520

@listas_bp.route('/editarNomeLista/', methods=['POST'])
@cross_origin(origins=["http://localhost:5173", "127.0.0.1"])
def editar_nome_lista():
    try:
        data = request.get_json()

        if not data:
            return 'Sem dados', 520

        lista_id = data.get("id")
        novo_nome = data.get("novoNome")

        if not lista_id or not novo_nome:
            return 'ID ou novo nome não fornecido', 520

        db = Database()

        resultado = db.update_one(
            "listas",
            {"_id": ObjectId(lista_id)},
            {"nomeLista": novo_nome}
        )

        db.close()

        if resultado.modified_count == 0:
            return "Nenhuma modificação realizada. Caso o erro persista, contate o administrador do sistema.", 404

        return 'OK', 200

    except Exception as e:
        return str(e), 520
    
@listas_bp.route('/adicionarWAPPScanALista/', methods=['POST'])
@cross_origin(origins=["http://localhost:5173", "127.0.0.1"])
def adicionarWAPPScanALista():  
    try:
        data = request.get_json()

        if not data:
            return 'Sem dados', 520

        nome_lista = data.get("nomeLista")
        scans = data.get("scans")

        if not nome_lista:
            return 'Nome da lista não fornecido', 520

        db = Database()

        documento = db.find_one("listas", {"nomeLista": nome_lista})

        db.close()

        if not documento:
            return "Lista não encontrada", 404
        
        tenable_api.download_scans_results_json(
            documento["pastas_scans_webapp"],
            scans
        )

        return 'OK', 200

    except Exception as e:
        return str(e), 520

@listas_bp.route('/adicionarVMScanALista/', methods=['POST'])
@cross_origin(origins=["http://localhost:5173", "127.0.0.1"])
def adicionarVMScanALista():  
    try:
        data = request.get_json()

        if not data:
            return 'Sem dados', 520

        nome_lista = data.get("nomeLista")
        id_scan = data.get("idScan")
        nome_scan = data.get("nomeScan")
        criado_por = data.get("criadoPor")
        idNmr = str(data.get("idNmr"))

        if not nome_lista:
            return 'Nome da lista não fornecido', 520

        db = Database()

        documento = db.find_one("listas", {"nomeLista": nome_lista})

        if not documento:
            return "Lista não encontrada", 404
        
        db.update_one(
            "listas",
            {"_id": ObjectId(documento["_id"])},
            {"id_scan": idNmr}
        )
        
        db.update_one(
            "listas",
            {"_id": ObjectId(documento["_id"])},
            {"historyid_scanservidor": id_scan}
        )

        db.update_one(
            "listas",
            {"_id": ObjectId(documento["_id"])},
            {"nomeScanStoryId": nome_scan}
        )

        db.update_one(
            "listas",
            {"_id": ObjectId(documento["_id"])},
            {"scanStoryIdCriadoPor": criado_por}
        )

        db.close()

        tenable_api.download_vmscans_csv(
            documento["pastas_scans_webapp"],
            documento["id_scan"],
            documento["historyid_scanservidor"]
        )

        return 'OK', 200

    except Exception as e:
        return str(e), 520

@listas_bp.route('/getTodasAsListas/', methods=['GET'])
@cross_origin(origins=["http://localhost:5173", "127.0.0.1"])
def getTodasAsListas():

    try:
        db = Database()

        listas = db.find("listas")

        listas_json = []

        for lista in listas:
            listas_json.append({
                "idLista": str(lista["_id"]),
                "nomeLista": lista["nomeLista"]
            })

        db.close()

        return listas_json, 200

    except Exception as e:
        return str(e), 520
    
@listas_bp.route('/gerarRelatorioDeLista/', methods=['POST'])
@cross_origin(origins=["http://localhost:5173", "127.0.0.1"])
def gerarRelatorioDeLista():

    try:

        data = request.get_json()

        if not data:
            return 'dasdasdasd', 520
        
        id_lista = data.get("idLista")
        nome_secretaria = data.get("nomeSecretaria")
        sigla_secretaria = data.get("siglaSecretaria")
        data_inicio = data.get("dataInicio")
        data_fim = data.get("dataFim")
        ano = data.get("ano")
        mes = data.get("mes")
        google_drive_link = data.get("linkGoogleDrive")

        db = Database()

        # =================================

        try:
            objeto_id = ObjectId(id_lista)
        except Exception as e:
            return f"ID inválido: {e}", 520
        
        lista = db.find_one("listas", {"_id": objeto_id})

        # =================================

        json_webapp_vulnerabilidades = lista["pastas_scans_webapp"]

        novo_relatorio = db.insert_one("relatorios", {"nome": nome_secretaria, "id_lista": id_lista, "destino_relatorio_preprocessado" : None}).inserted_id

        # ===========================================

        pasta_destino_relatorio_preprocessado = f"{config.caminho_shared_relatorios}/{novo_relatorio}/relatorio_preprocessado/"

        db.update_one("relatorios", {"_id": novo_relatorio}, {"destino_relatorio_preprocessado": pasta_destino_relatorio_preprocessado})

        # ===========================================

        destino = Path(pasta_destino_relatorio_preprocessado)
        destino.mkdir(parents=True, exist_ok=True)

        processar_relatorio_json(json_webapp_vulnerabilidades, pasta_destino_relatorio_preprocessado, config.caminho_shared_relatorios_exemplo)
        processar_relatorio_csv(json_webapp_vulnerabilidades, pasta_destino_relatorio_preprocessado, config.caminho_shared_relatorios_exemplo)

        extrair_quantidades_vulnerabilidades_por_site(f"{pasta_destino_relatorio_preprocessado}/vulnerabilidades_agrupadas_por_site.csv", json_webapp_vulnerabilidades)

        terminar_relatorio_preprocessado(
            nome_secretaria, 
            sigla_secretaria, 
            data_inicio, 
            data_fim, 
            ano, 
            mes, 
            pasta_destino_relatorio_preprocessado, 
            f"{pasta_destino_relatorio_preprocessado}/relatorio_pronto.tex", 
            config.caminho_shared_relatorios_exemplo,
            google_drive_link)


        pasta_front = f"../front-end/downloads/{novo_relatorio}/"

        destino = Path(pasta_front)
        destino.mkdir(parents=True, exist_ok=True)

        gerar_Grafico_Quantitativo_Vulnerabilidades_Por_Site(
                    f"{pasta_destino_relatorio_preprocessado}/vulnerabilidades_agrupadas_por_site.csv", f"{pasta_destino_relatorio_preprocessado}/RelatorioPronto/assets/images-was/Vulnerabilidades_x_site.png", "decrescente"
                )
        
        compilar_latex(f"{pasta_destino_relatorio_preprocessado}/RelatorioPronto/main.tex", f"{pasta_destino_relatorio_preprocessado}/RelatorioPronto/")
        compilar_latex(f"{pasta_destino_relatorio_preprocessado}/RelatorioPronto/main.tex", f"{pasta_destino_relatorio_preprocessado}/RelatorioPronto/")
    
        shutil.copy(
            f"{pasta_destino_relatorio_preprocessado}/RelatorioPronto/main.pdf",
            f"{pasta_front}/main.pdf"
        )

        db.update_one("listas", {"_id": id_lista}, {"relatorioGerado": True})
        db.close()
        db.close()

        return str(novo_relatorio), 200

    except Exception as e:
        return str(e), 520

@listas_bp.route('/getRelatorioMissingVulnerabilities/', methods=['GET'])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def get_report_missing_vulnerabilities():
    try:
        relatorio_id = request.args.get('relatorioId')
        report_type = request.args.get('type') 

        if not relatorio_id or not report_type:
            return jsonify({"error": "Parâmetros 'relatorioId' e 'type' são obrigatórios."}), 400

        caminho_base_preprocessado = Path(config.caminho_shared_relatorios) / str(relatorio_id) / "relatorio_preprocessado"
        
        file_name = ""
        if report_type == "sites":
            file_name = "vulnerabilidades_sites_ausentes.txt" 
        elif report_type == "servers":
            file_name = "vulnerabilidades_servidores_ausentes.txt"
        else:
            return jsonify({"error": "Tipo de relatório inválido. Use 'sites' ou 'servers'."}), 400

        caminho_completo_txt = caminho_base_preprocessado / file_name

        if os.path.exists(caminho_completo_txt) and os.path.isfile(caminho_completo_txt):
            with open(caminho_completo_txt, 'r', encoding='utf-8') as f:
                content = f.read()
            return jsonify({"content": content.splitlines()}), 200
        else:
            return jsonify({"message": f"Arquivo de vulnerabilidades ausentes não encontrado para o tipo '{report_type}' no caminho: {caminho_completo_txt}"}), 404

    except Exception as e:
        return jsonify({"error": f"Erro interno ao buscar vulnerabilidades ausentes: {str(e)}"}), 500

@listas_bp.route('/excluirLista/', methods=['POST'])
@cross_origin(origins=["http://localhost:5173", "127.0.0.1"])
def excluirLista():

    try:

        data = request.get_json()

        if not data:
            return 'Nenhum dado recebido.', 520
        
        id_lista = data.get("idLista")

        db = Database()

        print(db.find("listas"))

        try:
            objeto_id = ObjectId(id_lista)
        except Exception as e:
            return f"ID inválido: {e}", 520

        db.delete_one("listas", {"_id": objeto_id})

        pasta_lista = f"{config.caminho_shared_jsons}/{id_lista}/"
        if os.path.exists(pasta_lista):
            shutil.rmtree(pasta_lista)

        db.close()

        return 'OK', 200
        
    except Exception as e:
        return str(e), 520

@listas_bp.route('/baixarRelatorioPdf/', methods=['POST'])
@cross_origin(origins=["http://localhost:5173", "127.0.0.1"])
def baixar_relatorio_pdf():
    try:
        data = request.get_json()

        id_relatorio = data.get("idRelatorio")

        if not id_relatorio:
            return "ID do relatório não fornecido.", 400

        # Usando pathlib para garantir que o caminho esteja correto
        
        caminho_pdf = f"/app/shared/relatorios/{id_relatorio}/relatorio_preprocessado/RelatorioPronto/main.pdf"
        print(caminho_pdf)

        # Tentar enviar o arquivo
        return send_file(
            str(caminho_pdf),  # Passando o caminho como string
            as_attachment=True,
            download_name="Relatorio.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:
        # Logando o erro completo
        print(f"Erro interno: {str(e)}")
        return f"Erro interno: {str(e)}", 500

