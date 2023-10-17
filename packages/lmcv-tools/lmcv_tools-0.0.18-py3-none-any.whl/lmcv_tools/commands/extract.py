from ..interface import filer, messenger
from ..models.extraction_components import (
   ResultTable,
   Condition,
   Attribute
)

# Funções Globais
def extract(attributes: list[str], pos_data: str, condition: str = None) -> tuple[ResultTable, list]:
   # Instanciando Tabela de Resultado e Condição de Atributos
   result_table = ResultTable([])
   attributes_condition = Condition(condition)
   failed_atributes = list()
   
   # Analisando cada Atributo
   for attribute_name in attributes:
      # Instanciando Atributo
      attribute = Attribute(attribute_name)
      
      # Extraindo Dados Relativos ao Atributo dos Dados do .pos
      table = attribute.extract_from(pos_data, attributes_condition)

      # Cruzando Novos Dados com a Tabela de Resultado Final
      result_table = result_table.join(table)
      
      # Verificando se há Atributos não Cruzados
      if result_table.join_fail:
         failed_atributes.append(attribute_name)
   
   # Reordenando Dados (Não Falhos Apenas)
   valid_attributes = [a for a in attributes if a not in failed_atributes]
   result_table.reorder(valid_attributes)
   
   return result_table, failed_atributes

def start(attributes: list[str], pos_path: str, condition: str, csv_path: str):
   # Lendo Arquivo .pos
   pos_data = filer.read(pos_path)

   # Extraindo Dados e Convertendo para o Formato CSV
   table, failed_attributes = extract(attributes, pos_data, condition)
   csv_data = table.to_csv()

   # Informando Atributos não Cruzados
   if len(failed_attributes) > 0:
      messenger.warning('The following attributes could not be related to the others considering the attributes order informed:')
      messenger.show(','.join(failed_attributes))

   # Escrevendo Extração no .csv
   filer.write(csv_path, csv_data)