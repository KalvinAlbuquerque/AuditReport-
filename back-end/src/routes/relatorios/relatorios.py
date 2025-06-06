from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from utils.config import Config
from api.tenable_api import TenableApi # Se não for usado, pode remover
from database.database import Database
import os
from pathlib import Path
import shutil
from bson.objectid import ObjectId

tenable_api = TenableApi() # Se não for usado, pode remover
config = Config("config.json")

relatorios_bp = Blueprint('relatorios', __name__, url_prefix='/relatorios')

@relatorios_bp.route('/getRelatoriosGerados/', methods=['GET'])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def getRelatoriosGerados():
    try:
        db = Database()
        relatorios = db.find("relatorios")
        relatorios_list = []
        for relatorio in relatorios:
            relatorios_list.append({
                "nome": relatorio["nome"],
                "id": str(relatorio["_id"])
            })
        db.close()
        return jsonify(relatorios_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 520

@relatorios_bp.route('/deleteRelatorio/<string:relatorio_id>', methods=['DELETE'])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def deleteRelatorio(relatorio_id):
    try:
        db = Database()
        
        delete_result = db.delete_one("relatorios", {"_id": db.get_object_id(relatorio_id)})
        
        if delete_result.deleted_count == 0:
            db.close()
            return jsonify({"message": "Relatório não encontrado no banco de dados."}), 404

        report_folder_path = Path(config.caminho_shared_relatorios) / relatorio_id
        
        if report_folder_path.exists() and report_folder_path.is_dir():
            shutil.rmtree(report_folder_path)
            print(f"DEBUG: Pasta do relatório excluída: {report_folder_path}")
        else:
            print(f"DEBUG: Pasta do relatório não encontrada ou não é um diretório: {report_folder_path}")

        db.close()
        return jsonify({"message": "Relatório excluído com sucesso."}), 200

    except Exception as e:
        print(f"Erro ao excluir relatório {relatorio_id}: {str(e)}")
        return jsonify({"error": f"Erro interno ao excluir relatório: {str(e)}"}), 500

# --- NOVO ENDPOINT PARA EXCLUIR TODOS OS RELATÓRIOS ---
@relatorios_bp.route('/deleteAllRelatorios/', methods=['DELETE'])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def deleteAllRelatorios():
    try:
        db = Database()
        
        # 1. Recuperar todos os relatórios para obter seus IDs (necessário para excluir as pastas)
        all_relatorios = db.find("relatorios") # Pega todos os documentos
        
        # 2. Excluir todos os documentos do banco de dados
        delete_db_result = db.delete_many("relatorios", {}) # Query vazia para deletar tudo
        
        # 3. Excluir todas as pastas de relatórios do sistema de arquivos
        deleted_folders_count = 0
        for relatorio in all_relatorios:
            relatorio_id = str(relatorio["_id"]) # Converte ObjectId para string
            report_folder_path = Path(config.caminho_shared_relatorios) / relatorio_id
            
            if report_folder_path.exists() and report_folder_path.is_dir():
                try:
                    shutil.rmtree(report_folder_path)
                    deleted_folders_count += 1
                    print(f"DEBUG: Pasta do relatório excluída: {report_folder_path}")
                except Exception as folder_e:
                    print(f"ATENÇÃO: Não foi possível excluir a pasta {report_folder_path}: {str(folder_e)}")
            else:
                print(f"DEBUG: Pasta {report_folder_path} não encontrada ou não é um diretório.")

        db.close()
        return jsonify({
            "message": f"Todos os {delete_db_result.deleted_count} relatórios foram excluídos do banco de dados e {deleted_folders_count} pastas foram removidas do sistema de arquivos."
        }), 200

    except Exception as e:
        print(f"Erro ao excluir todos os relatórios: {str(e)}")
        return jsonify({"error": f"Erro interno ao excluir todos os relatórios: {str(e)}"}), 500