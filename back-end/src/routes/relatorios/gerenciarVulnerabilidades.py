from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import os
import json
from werkzeug.utils import secure_filename # Importar secure_filename para segurança

# Importe suas funções auxiliares
# Certifique-se de que 'utils/json_utils.py' existe e está acessível
from utils.json_utils import _load_data, _save_data, add_vulnerability, \
                             get_all_vulnerabilities, update_vulnerability, delete_vulnerability, _load_data_

# Obtenha o diretório base do script atual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminhos dos arquivos JSON e pasta de upload
# A lógica de '..' é para subir na árvore de diretórios até a raiz do projeto 'relatorios-vuln'
# BASE_DIR (gerenciarVulnerabilidades.py) está em:
# C:/Users/kalvi/Code/relatorios-vuln/back-end/src/routes/gerenciar_vulnerabilidades/
# Precisamos subir 4 níveis para chegar em:
# C:/Users/kalvi/Code/relatorios-vuln/
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', '..', '..', '..'))
SHARED_DIR = os.path.join(PROJECT_ROOT, 'shared')

VULN_SITES_FILE = os.path.join(SHARED_DIR, "relatorios", "Exemplo", "vulnerabilidades.json")
VULN_SERVERS_FILE = os.path.join(SHARED_DIR, "relatorios", "Exemplo", "vulnerabilidades_servidores.json")

# NOVOS CAMINHOS para os arquivos de descrição
DESCRITIVO_SITES_FILE = os.path.join(SHARED_DIR, "relatorios", "Exemplo", "descritivo_vulnerabilidades.json")
DESCRITIVO_SERVERS_FILE = os.path.join(SHARED_DIR, "relatorios", "Exemplo", "descritivo_vulnerabilidades_servidores.json")


# Caminho base para o upload de imagens
# As imagens serão salvas em:
# C:/Users/kalvi/Code/relatorios-vuln/shared/relatorios/Exemplo/RelatorioExemplo/assets
UPLOAD_FOLDER = os.path.join(SHARED_DIR, "relatorios", "Exemplo", "RelatorioExemplo", "assets")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} # Extensões de arquivo permitidas

# Garante que a pasta de upload base exista quando o Flask iniciar
# É crucial que o Flask tenha permissão de escrita neste diretório
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Crie uma instância do Blueprint para gerenciar_vulnerabilidades
gerenciar_vulnerabilidades_bp = Blueprint('gerenciar_vulnerabilidades', __name__, url_prefix='/vulnerabilidades')

# --- Função Auxiliar para Obter o Caminho do Arquivo JSON ---
def _get_vuln_file_path(vuln_type: str):
    """Retorna o caminho do arquivo JSON com base no tipo de vulnerabilidade."""
    if vuln_type == "sites":
        return VULN_SITES_FILE
    elif vuln_type == "servers":
        return VULN_SERVERS_FILE
    else:
        raise ValueError(f"Tipo de vulnerabilidade inválido: '{vuln_type}'. Use 'sites' ou 'servers'.")

# --- Função Auxiliar para Obter o Caminho do Arquivo Descritivo ---
def _get_descritivo_file_path(vuln_type: str):
    """Retorna o caminho do arquivo JSON descritivo com base no tipo de vulnerabilidade."""
    if vuln_type == "sites":
        return DESCRITIVO_SITES_FILE
    elif vuln_type == "servers":
        return DESCRITIVO_SERVERS_FILE
    else:
        raise ValueError(f"Tipo de vulnerabilidade inválido para descritivo: '{vuln_type}'. Use 'sites' ou 'servers'.")

# --- Função Auxiliar para Verificar Extensão do Arquivo ---
def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- NOVA Rota: Upload de Imagem ---
@gerenciar_vulnerabilidades_bp.route('/uploadImage/', methods=['POST'])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def upload_image_api():
    try:
        # Verifica se o arquivo de imagem foi enviado na requisição
        if 'image' not in request.files:
            return jsonify({"error": "Nenhum arquivo de imagem fornecido."}), 400

        file = request.files['image']
        
        # Se o usuário não selecionar um arquivo, o navegador envia um arquivo vazio sem nome.
        if file.filename == '':
            return jsonify({"error": "Nenhum arquivo selecionado para upload."}), 400

        if file and allowed_file(file.filename):
            # Obtém os dados da categoria, subcategoria e nome da vulnerabilidade do formulário
            # Estes são enviados junto com o arquivo (FormData)
            category = request.form.get('categoria')
            subcategory = request.form.get('subcategoria')
            vulnerability_name = request.form.get('vulnerabilidade')

            if not all([category, subcategory, vulnerability_name]):
                return jsonify({"error": "Categoria, subcategoria e nome da vulnerabilidade são obrigatórios para o upload da imagem."}), 400

            # Constrói o caminho completo da pasta onde a imagem será salva
            # Ex: UPLOAD_FOLDER/images-was/Outras Vulnerabilidades Críticas e Explorações/Desafios de Configuração de Segurança/
            image_folder = os.path.join(UPLOAD_FOLDER, 'images-was', category, subcategory)
            os.makedirs(image_folder, exist_ok=True) # Cria as pastas se não existirem

            # Sanitiza o nome do arquivo para evitar problemas de segurança e define o nome final
            # O nome do arquivo será baseado no nome da vulnerabilidade
            filename_base = secure_filename(vulnerability_name)
            file_extension = os.path.splitext(file.filename)[1] # Obtém a extensão original
            final_filename = f"{filename_base}{file_extension}"
            file_path = os.path.join(image_folder, final_filename)
            
            # Salva o arquivo na pasta
            file.save(file_path)

            # Retorna o caminho relativo que será salvo no JSON da vulnerabilidade
            # Este caminho deve ser relativo à pasta 'RelatorioExemplo' para ser usado corretamente pelo LaTeX ou frontend
            relative_image_path = f"assets/images-was/{category}/{subcategory}/{final_filename}"
            return jsonify({"message": "Imagem enviada com sucesso!", "imagePath": relative_image_path}), 200
        else:
            return jsonify({"error": "Tipo de arquivo não permitido. Apenas PNG, JPG, JPEG e GIF são aceitos."}), 400
    except Exception as e:
        # Loga o erro completo para depuração no console do Flask
        print(f"Erro no upload_image_api: {e}")
        return jsonify({"error": f"Erro interno ao fazer upload da imagem: {str(e)}"}), 500

# --- Rota para obter categorias e subcategorias descritivas ---
@gerenciar_vulnerabilidades_bp.route('/getDescritivos/', methods=['GET'])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def get_descritivos_api():
    try:
        vuln_type = request.args.get('type')
        if not vuln_type:
            return jsonify({"error": "Parâmetro 'type' é obrigatório (sites ou servers)."}), 400

        file_path = _get_descritivo_file_path(vuln_type)
        
        # Carrega os dados do arquivo descritivo
        # Supondo que _load_data retorna o dicionário {"vulnerabilidades": [...]}
        full_data_from_file = _load_data_(file_path)
        
        # **Ajuste aqui:** Acesse a chave 'vulnerabilidades' do dicionário carregado.
        # Se 'full_data_from_file' já é a lista, então 'full_data_from_file' já é o que você precisa.
        if isinstance(full_data_from_file, dict) and "vulnerabilidades" in full_data_from_file:
            data_to_return = full_data_from_file.get("vulnerabilidades", [])
        elif isinstance(full_data_from_file, list):
            # Isso significa que _load_data já retornou a lista diretamente.
            # O warning "não é uma lista JSON" é enganoso ou a mensagem de erro da função load.
            data_to_return = full_data_from_file
        else:
            # Caso o JSON não seja um dicionário com "vulnerabilidades" nem uma lista
            print(f"Aviso: Conteúdo de '{file_path}' não é um dicionário com 'vulnerabilidades' ou uma lista. Retornando lista vazia.")
            data_to_return = []

        return jsonify(data_to_return), 200 # Retorna a lista (que é o valor de "vulnerabilidades")
    except ValueError as ve:
        print(f"ValueError em get_descritivos_api: {ve}")
        return jsonify({"error": str(ve)}), 400
    except FileNotFoundError:
        print(f"Erro: Arquivo descritivo não encontrado em {file_path}")
        return jsonify({"error": "Arquivo descritivo não encontrado."}), 404
    except Exception as e:
        print(f"Erro em get_descritivos_api: {e}")
        return jsonify({"error": str(e)}), 500

# --- Rotas Existentes (GET, POST, PUT, DELETE) ---
# As funções auxiliares (add_vulnerability, update_vulnerability, delete_vulnerability)
# já estão preparadas para lidar com o campo 'Imagem' como um caminho de string.

@gerenciar_vulnerabilidades_bp.route('/getVulnerabilidades/', methods=['GET'])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def get_all_vulnerabilities_api():
    try:
        vuln_type = request.args.get('type')
        if not vuln_type:
            return jsonify({"error": "Parâmetro 'type' é obrigatório (sites ou servers)."}), 400

        file_path = _get_vuln_file_path(vuln_type)
        data = get_all_vulnerabilities(file_path)
        return jsonify(data), 200
    except ValueError as ve:
        print(f"ValueError em get_all_vulnerabilities_api: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"Erro em get_all_vulnerabilities_api: {e}")
        return jsonify({"error": str(e)}), 500

@gerenciar_vulnerabilidades_bp.route('/addVulnerabilidade/', methods=['POST'])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def add_vulnerability_api():
    try:
        request_data = request.get_json()
        if not request_data:
            return jsonify({"error": "Dados não fornecidos."}), 400

        vuln_type = request_data.get('type')
        new_vuln_data = request_data.get('data')

        if not vuln_type or not new_vuln_data:
            return jsonify({"error": "Parâmetros 'type' e 'data' são obrigatórios no corpo da requisição."}), 400

        file_path = _get_vuln_file_path(vuln_type)
        success, message = add_vulnerability(file_path, new_vuln_data)
        
        if success:
            return jsonify({"message": message}), 201
        else:
            return jsonify({"error": message}), 409
    except ValueError as ve:
        print(f"ValueError em add_vulnerability_api: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"Erro em add_vulnerability_api: {e}")
        return jsonify({"error": str(e)}), 500

@gerenciar_vulnerabilidades_bp.route('/updateVulnerabilidade/', methods=['PUT'])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def update_vulnerability_api():
    try:
        request_data = request.get_json()
        if not request_data:
            return jsonify({"error": "Dados não fornecidos."}), 400

        vuln_type = request_data.get('type')
        old_name = request_data.get('oldName')
        new_data = request_data.get('data')

        if not vuln_type or not old_name or not new_data:
            return jsonify({"error": "Parâmetros 'type', 'oldName' e 'data' são obrigatórios no corpo da requisição."}), 400

        file_path = _get_vuln_file_path(vuln_type)
        success, message = update_vulnerability(file_path, old_name, new_data)
        
        if success:
            return jsonify({"message": message}), 200
        else:
            return jsonify({"error": message}), 404
    except ValueError as ve:
        print(f"ValueError em update_vulnerability_api: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"Erro em update_vulnerability_api: {e}")
        return jsonify({"error": str(e)}), 500

@gerenciar_vulnerabilidades_bp.route('/deleteVulnerabilidade/', methods=['DELETE'])
@cross_origin(origins=["http://localhost:5173", "http://127.0.0.1:5173"])
def delete_vulnerability_api():
    try:
        request_data = request.get_json()
        if not request_data:
            return jsonify({"error": "Dados não fornecidos."}), 400

        vuln_type = request_data.get('type')
        vuln_name = request_data.get('name')

        if not vuln_type or not vuln_name:
            return jsonify({"error": "Parâmetros 'type' e 'name' são obrigatórios no corpo da requisição."}), 400
        
        file_path = _get_vuln_file_path(vuln_type)
        
        # --- Lógica para deletar a imagem associada ---
        try:
            # 1. Carrega os dados para encontrar a vulnerabilidade a ser deletada
            all_vulnerabilities = _load_data(file_path)
            
            # 2. Encontra a vulnerabilidade pelo nome
            vuln_to_delete = next((v for v in all_vulnerabilities if v.get("Vulnerabilidade") == vuln_name), None)

            if vuln_to_delete and vuln_to_delete.get("Imagem"):
                # 3. Constrói o caminho absoluto da imagem
                # A Imagem é um caminho relativo a UPLOAD_FOLDER + 'RelatorioExemplo'
                # Ex: "assets/images-was/Categoria/Subcategoria/nome.png"
                # UPLOAD_FOLDER já aponta para '.../RelatorioExemplo/assets'
                
                # Extrai a parte da 'Imagem' que vem depois de 'assets/'
                relative_path_after_assets = vuln_to_delete["Imagem"].replace("assets/", "", 1)
                image_full_path = os.path.join(UPLOAD_FOLDER, relative_path_after_assets)

                if os.path.exists(image_full_path):
                    os.remove(image_full_path)
                    print(f"Imagem '{image_full_path}' deletada com sucesso.")
                else:
                    print(f"Aviso: Imagem '{image_full_path}' não encontrada no disco ao tentar deletar.")
            else:
                print(f"Nenhuma imagem associada ou vulnerabilidade '{vuln_name}' não encontrada para deletar.")
        except Exception as img_e:
            # Não impede a deleção do JSON, apenas loga o erro da imagem
            print(f"Erro ao tentar deletar a imagem para '{vuln_name}': {img_e}")
        # --- Fim da lógica para deletar a imagem ---

        # Procede com a deleção da vulnerabilidade no JSON
        success, message = delete_vulnerability(file_path, vuln_name)
        
        if success:
            return jsonify({"message": message}), 200
        else:
            return jsonify({"error": message}), 404
    except ValueError as ve:
        print(f"ValueError em delete_vulnerability_api: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"Erro em delete_vulnerability_api: {e}")
        return jsonify({"error": str(e)}), 500