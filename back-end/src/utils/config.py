import json

class Config:
    """
    Classe responsável por carregar e fornecer os dados de configuração.

    Esta classe lê um arquivo JSON de configuração e fornece as configurações de forma segura 
    através de propriedades.
    """

    _instance = None
    _inicializado = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, arquivo_config: str):

        """
        Inicializa a classe Config carregando as configurações do arquivo JSON.

        :param arquivo_config: Caminho do arquivo JSON que contém as configurações.
        """

        if not self._inicializado:
            if arquivo_config is None:
                raise ValueError("arquivo_config deve ser fornecido na primeira inicialização.")
            with open(arquivo_config, 'r', encoding='utf-8') as f:
                self._config_data = json.load(f)
            self._inicializado = True
        
        self._arquivo_config = json.load(open(arquivo_config, 'r', encoding='utf8'))

        # Carregando as configurações individuais
        self._caminho_shared_relatorios = self._arquivo_config["caminho_shared_relatorios"]
        self._caminho_shared_jsons = self._arquivo_config["caminho_shared_jsons"]
        self._caminho_shared_relatorios_exemplo = self._arquivo_config["caminho_shared_relatorios_exemplo"]
    
    @property
    def caminho_shared_relatorios(self) -> str:
        """
        Retorna o caminho da pasta shared de relatorios.

        :return: Caminho da pasta shared de relatorios.
        """
        return self._caminho_shared_relatorios
    
    @property
    def caminho_shared_jsons(self) -> str:
        """
        Retorna o caminho da pasta shared de arquivos json.

        :return: Caminho da pasta shared de arquivos json.
        """
        return self._caminho_shared_jsons
    
    @property
    def caminho_shared_relatorios_exemplo(self) -> str:
        """
        Retorna o caminho da pasta shared de exemplo de relatorios.

        :return: Caminho da pasta shared de exemplo de relatorios.
        """
        return self._caminho_shared_relatorios_exemplo
