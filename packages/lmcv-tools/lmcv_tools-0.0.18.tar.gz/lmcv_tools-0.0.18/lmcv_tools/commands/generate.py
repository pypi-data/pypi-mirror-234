from inspect import signature
from ..interface import filer
from ..models.generation_artifacts import (
   VirtualLaminas,
   ElementConfiguration,
   MicromechanicalModel,
   Material
)
from ..models.graphical_interfaces import PromptGenerateVirtualLaminas
from ..models.custom_errors import CommandError

# Funções de Geração de Artefatos
def generate_virtual_laminas(
   laminas_count: int,
   element_type: str,
   thickness: float,
   number_integration_points: int,
   power_law_exponent: float,
   micromechanical_model: str,
   E1: float,
   E2: float,
   nu1: float,
   nu2: float,
   pho1: float,
   pho2: float,
   smart: bool
) -> VirtualLaminas:
   # Instanciando Configuração do Elemento
   element = ElementConfiguration(element_type, number_integration_points)

   # Instanciando Materiais
   materials = list()
   materials.append(Material(E1, nu1, pho1))
   materials.append(Material(E2, nu2, pho2))

   # Instanciando Modelo Micromecânico
   model = MicromechanicalModel(micromechanical_model, materials)
   
   # Instanciando Artefato de Lâminas Virtuais
   virtual_laminas = VirtualLaminas(
      laminas_count,
      thickness,
      power_law_exponent,
      element,
      model,
      smart
   )
   virtual_laminas.generate()

   return virtual_laminas

# Funções de Parâmetros de Artefatos
def params_virtual_laminas(args: list[str]) -> dict:
   # Iniciando Parâmetros
   params = dict()
   
   # Exibindo Interface Gráfica para Preencher Parâmetros (Se não Houver Parâmetros)
   if len(args) == 0:
      window = PromptGenerateVirtualLaminas(params)
      window.start()

      # Conferindo se Há um Caminho
      if params.get('path') is not None:
         if params['path'] != '':
            args = [params['path']]
         del params['path']

   # Tentando Coletar Parâmetros Dados 
   else:
      try:
         reference = dict(signature(generate_virtual_laminas).parameters)
         index = 0
         for name, param_obj in reference.items():
            type_class = param_obj.annotation
            if type_class is bool:
               params[name] = False if args.pop(0) == 'False' else True
            else:   
               params[name] = type_class(args.pop(0))
            index += 1
      except IndexError:
         raise CommandError('Invalid number of arguments.', help=True)
   
   return params, args

# Relação Artefato/Funções
artifacts = {
   'virtual_laminas': {
      'params': params_virtual_laminas,
      'generate': generate_virtual_laminas
   }
}

# Funções de Inicialização
def start(artifact_name: str, args: list[str]) -> str:
   try:
      # Coletando Parâmetros
      params_function = artifacts[artifact_name]['params']
      params, args = params_function(args)

      # Gerando Artefato
      generate_function = artifacts[artifact_name]['generate']
      artifact = generate_function(**params)

   except KeyError:
      raise CommandError(f'Unknown Artifact "{artifact_name}"')
   except TypeError:
      raise CommandError('Not all arguments were correctly passed.')

   # Escrevendo Arquivo do Artefato
   try:
      path = args[0]
   except IndexError:
      path = artifact.file_name
   filer.write(path, artifact.data)
