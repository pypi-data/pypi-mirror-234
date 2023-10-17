from sys import exit
from ..models.ansi_style import Color, Effect

# Funções Globais
def show(message: str):
   print(message)

def error(message: str, name: str = 'CommandError'):
   # Exibindo Mensagem de Erro
   print(f'{Color.red}| {name} | :{Effect.reset} {message}')

   # Terminando Processo (Se não Estiver no Modo Interativo)
   from .core import in_interactive_mode
   if not in_interactive_mode:
      exit(1)

def warning(message: str):
   # Exibindo Mensagem de Alerta
   print(f'{Color.yellow}| Warning | :{Effect.reset} {message}')

def info(message: str):
   # Exibindo Mensagem de Informativa de Destaque
   print(f'{Color.blue}| Info | :{Effect.reset} {message}')