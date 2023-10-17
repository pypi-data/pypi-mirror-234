from ..interface import searcher, messenger
from ..models.custom_errors import CommandError
from ..models.ansi_style import Color, Effect

# Pesquisando Mensagens de Ajuda na Base de Dados
help_messages = searcher.get_database('help_messages')

# Função de Inicialização
def start(command_name: str = 'default'):   
   # Coletando Dados da Mensagem de Ajuda com base nos Argumentos.
   try:
      message = help_messages[command_name]
   except KeyError:
      raise CommandError(f'There is no command named "{command_name}".')
   
   # Gerando Mensagem
   messenger.show(f"{Effect.bold}Usage:{Effect.reset} {message['usage']}\n")
   for title, points in message['topics'].items():
      # Exibindo Título do Tópico
      messenger.show(f"{Color.green + Effect.bold}{title}:{Effect.reset}")

      # Determinando Largura Máxima da Primera Coluna dos Pontos do Tópico
      max_width = 0
      for name in points.keys():
         len_name = len(name)
         if len_name > max_width:
            max_width = len_name
      max_width += 3

      # Exibindo Pontos do Tópico
      for name, description in points.items():
         # Dividindo Descrição em Linhas
         lines = description.split('. ')

         # Cortando Primeira Linha se Necessário
         max_size = 79 - (max_width + 5)
         first_line = lines.pop(0)
         
         if (first_line_cropped := len(first_line) > max_size):
            crop_index = first_line[:max_size].rfind(' ')
            lines.insert(0, first_line[crop_index + 1:])
            first_line = first_line[:crop_index]
         
         # Exibindo a Primeira Linha
         first_line = f"\n{name:<{max_width}}|   {first_line}"
         if not first_line_cropped:
            first_line += '.'
         messenger.show(first_line)

         # Exibindo Demais Linhas
         for line in lines:
            # Quebrando Linhas para Terem 80 Caracteres
            offset = ' ' * max_width
            while len(line) > max_size:
               crop_index = line[:max_size].rfind(' ')
               cropped_line = line[:crop_index]
               line = line[crop_index + 1:]
               messenger.show(f"{offset}|   {cropped_line}")
            messenger.show(f"{offset}|   {line}.")

      # Quebra de Linha Final do Tópico
      messenger.show('')