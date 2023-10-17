# Funções Globais
def read(file_path: str) -> str:
   try:
      file = open(file_path, 'r')
      file_data = file.read()
   except OSError:
      raise OSError(f'Could not open or read the {file_path}')
   file.close()
   return file_data

def write(file_path: str, file_data: str):
   try:
      file = open(file_path, 'w')
      file.write(file_data)
   except OSError:
      raise OSError(f'Could not write the {file_path}')
   file.close()