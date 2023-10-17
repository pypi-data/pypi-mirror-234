from . import messenger
from ..models.custom_errors import CommandError

# Constantes Globais
version = '0.0.18'
in_interactive_mode = False
message_welcome = '''
LMCV Tools is a command line tool that provides a series of useful functionali-
ties for the day-to-day simulations of the "Laboratório de Mecânica Computacio-
nal e Visualização" of the "Universidade Federal do Ceará" (UFC). 

Since a command was not typed, interactive mode was started. Here, you can type
multiple commands in sequence interactively:

To get help | type the command "help"
To exit     | type the command "exit"
'''

# Funções Pré-processamento de Comandos
def show_version(args: list[str] = [], flags: list[str] = []):
   messenger.show(f'LMCV Tools - v{version}')

def pre_help(args: list[str] = [], flags: list[str] = []):   
   from ..commands import help
   
   if len(args) > 0:
      help.start(args[0])
   else:
      help.start()

def pre_translate(args: list[str], flags: list[str] = []):
   from ..commands import translate

   # Verificando Path do Input
   try:
      input_path = args[0]
   except IndexError:
      raise CommandError('An Input File Path is required.')

   # Verificando Extensão do Output
   try:
      if 'to' != args[1]:
         raise CommandError('"to" keyword after Input File Path is required.')
   except IndexError:
      raise CommandError('"to" keyword after Input File Path is required.')
   try:
      output_extension = args[2]
   except IndexError:
      raise CommandError('An Extension for Output File after "to" keyword is required.')
   
   # Iniciando Tradução
   translate.start(input_path, output_extension, args[3:])

def pre_extract(terms: list[str], flags: list[str] = []):
   from ..commands import extract

   # Verificando Sintaxe Básica da Sentença
   if 'from' not in terms:
      raise CommandError('The keyword "from" is required.', help=True)
   
   # Verificando se ao menos 1 Atributo foi fornecido
   index = terms.index('from')
   attributes = terms[:index]
   if len(attributes) == 0:
      raise CommandError('At least one attribute before "from" is required.')

   # Verificando se o Path do Arquivo .pos foi fornecido
   try:
      pos_path = terms[index + 1]
   except IndexError:
      raise CommandError('The path to .pos file after "from" is required.')
   
   # Verificando se um Path para o .csv foi fornecido
   csv_path = pos_path[:-3] + 'csv'
   index_to = 0
   if 'to' in terms[index + 1:]:
      index_to = terms.index('to')
      try:
         csv_path = terms[index_to + 1]
      except IndexError:
         raise CommandError('The Syntax "to [path/to/.csv]" is optional, but it is incomplete.')
   
   # Verificando se uma Condição foi fornecida
   condition = None
   if 'where' in terms[index + 1:]:
      index_where = terms.index('where')
      if index_to > index_where:
         condition = terms[index_where + 1:index_to]
      else:
         condition = terms[index_where + 1:]
      if len(condition) == 0:
         raise CommandError('The Syntax "where [condition]" is optional, but it is incomplete.')
      condition = ' '.join(condition)

   # Extraindo Itens do Arquivo .pos
   extract.start(attributes, pos_path, condition, csv_path)

def pre_generate(args: list[str], flags: list[str] = []):
   from ..commands import generate
   
   # Verificando se um Artefato foi Dado
   if len(args) == 0:
      raise CommandError('An Artifact must be given.', help=True)

   # Iniciando Comando
   artifact = args[0]
   generate.start(artifact, args[1:])

def pre_reorder(args: list[str], flags: list[str] = []):
   from ..commands import reorder
   
   # Verificando se um Método de Reordenação foi Fornecido
   try:
      method = args[0]
   except IndexError:
      raise CommandError('A reorder method is required.')
   
   # Verificando se um Caminho de Arquivo foi Fornecido
   try:
      dat_path = args[1]
   except IndexError:
      raise CommandError('A path to .dat file is required.')
   
   # Executando Reordenação
   reorder.start(method, dat_path, flags)

# Relação Comando/Função
commands = {
   'version': show_version,
   'help': pre_help,
   'translate': pre_translate,
   'extract': pre_extract,
   'generate': pre_generate,
   'reorder': pre_reorder
}

# Funções de Inicialização
def execute_command(name: str, args: list[str]):
   # Encapsulando Execução para Tratamento Padrão de Erros
   try:
      # Tentando Identificar o Comando
      try:
         command_function = commands[name]
      except KeyError:
         raise CommandError('Unknown command.', help=True)

      # Processando Flags
      flags = list()
      for index, arg in enumerate(args):
         if arg.startswith('--'):
            flags.append(args.pop(index))
         elif arg.startswith('-') and (len(arg) == 2) and arg[1].isalpha():
            flags.append(args.pop(index))

      # Executando Comando
      command_function(args, flags)

   except Exception as exc:
      # Exibindo Mensagem de Erro com o Contexto da Exceção
      name = exc.__class__.__name__
      message = exc.args[0]
      messenger.error(message, name)

def show_welcome():
   show_version()
   messenger.show(message_welcome)

def start_interactive_mode():
   # Informando que o Modo Interativo foi Iniciado
   global in_interactive_mode
   in_interactive_mode = True

   # Exibindo Mensagem de Boas-Vindas
   show_welcome()

   # Iniciando Loop
   while True:
      # Lendo Argumentos
      args = input('>> ').split()

      # Executando Comando
      if len(args) == 0:
         continue
      command_name = args[0]
      if command_name == 'exit':
         break
      execute_command(command_name, args[1:])

def start(args: list[str]):
   # Iniciando Modo Interativo (Se não houver Argumentos)
   if len(args) == 0:
      start_interactive_mode()

   # Executando Comando Único
   else:
      execute_command(args[0], args[1:])
