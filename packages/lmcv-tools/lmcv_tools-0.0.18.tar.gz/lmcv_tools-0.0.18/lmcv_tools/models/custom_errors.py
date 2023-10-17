class CommandError(Exception):
   def __init__(self, message: str, help: bool = False):
      # Verificando se é Necessário Informar o Comando de Ajuda
      if help:
         message += '\nPlease, use help command (lmcv_tools help).'
      super().__init__(message)