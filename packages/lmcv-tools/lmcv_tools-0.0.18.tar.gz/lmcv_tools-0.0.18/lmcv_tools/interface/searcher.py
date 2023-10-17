import json
from importlib.resources import files

# Constantes Globais
databases_files = files('lmcv_tools.resources.databases')

# Funções Globais
def get_database(json_name: str) -> dict:
   # Abrindo Arquivo JSON da Base de Dados
   json_file = databases_files.joinpath(json_name + '.json')
   json_file = json_file.open('r')
   json_data = json.load(json_file)
   return json_data
