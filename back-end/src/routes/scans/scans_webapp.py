from flask import Blueprint, request
from flask_cors import cross_origin

from utils.config import Config
from api.tenable_api import TenableApi
import os

tenable_api = TenableApi()
config = Config("config.json")

scans_bp = Blueprint('scans', __name__, url_prefix='/scans/webapp')

@scans_bp.route('/scansfromfolderofuser/', methods=['POST'])
@cross_origin(origins=["http://localhost:5173", "127.0.0.1"])
def scansfromfolderofuser():
    try:
        data = request.get_json()

        if not data:
            return '', 520

        nome_usuario = data.get("nomeUsuario")
        nome_pasta = data.get("nomePasta")

        if not nome_usuario or not nome_pasta:
            return '', 520

        scans = tenable_api.get_web_app_scans_from_folder_of_user(nome_pasta, nome_usuario)

        print(scans)

        if scans['pagination']['total'] == 0:
            return 'Não foi possível encontrar scans nesta pasta. Verifique o usuário e o nome da pasta e tente novamente.', 520

        return scans, 200

    except Exception:
        return '', 520
    
@scans_bp.route('/downloadscans/', methods=['POST'])
@cross_origin(origins=["http://localhost:3000/", "127.0.0.1"])
def downloadscans():

    try:
        data = request.get_json()

        if not data:
            return '', 520
        
        scans = data.get("scans")
        usuario = data.get("usuario")
        nome_pasta = data.get("nomePasta")

        if not scans or not usuario or not nome_pasta:
            return '', 520
        
        # Check if the folder exists, if not, create it
        folder_path = f"{config.caminho_shared_jsons}/{usuario}/{nome_pasta}"
        counter = 0

        if os.path.exists(folder_path):
            counter = 1
            while True:
                new_folder_path = f"{folder_path}_{counter}"
                if not os.path.exists(new_folder_path):
                    print(new_folder_path)
                    folder_path = new_folder_path
                    break
                counter += 1

        os.makedirs(folder_path)

        tenable_api.download_scans_results_json(folder_path, scans)

        return str(counter), 200
    
    except Exception:
        return '', 520
    
