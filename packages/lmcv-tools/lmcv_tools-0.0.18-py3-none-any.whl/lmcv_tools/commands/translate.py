from ..interface import filer, searcher
from ..models.geometry import projection_isometric
from ..models.translation_components import (
   INP_Interpreter,
   DAT_Interpreter,
   SVG_Interpreter
)

# Funções de Tradução
def inp_to_dat(input_data: str, args: list[str] = []):
   # Instanciando Interpretadores
   inp_interpreter = INP_Interpreter()
   dat_interpreter = DAT_Interpreter()

   # Interpretando Input
   inp_interpreter.read(input_data)

   # Transferindo Modelo de Simulação Interpretado
   dat_interpreter.model = inp_interpreter.model

   # Reordenando Nodes
   reference = searcher.get_database('translation_reference')['inp_to_dat']
   for group_ide, group in dat_interpreter.model.element_groups.items():
      # Idenfiticando Geometria do Grupo
      geometry = dat_interpreter.model.element_geometries[group.geometry_ide]
      
      # Pegando Reordenação da Referência
      nodes_reordering = reference['nodes_reordering'][geometry.shape][str(geometry.grade)]

      # Sobescrevendo Ordem dos Nodes
      for ide, element in group.elements.items():
         node_ides = [element.node_ides[i - 1] for i in nodes_reordering ]
         dat_interpreter.model.add_element(group_ide, ide, node_ides)

   # Retornando Tradução
   return dat_interpreter.write()

def dat_to_svg(input_data: str, args: list[str] = []):
   # Instanciando Interpretadores
   dat_interpreter = DAT_Interpreter()
   svg_interpreter = SVG_Interpreter()

   # Interpretando Input
   dat_interpreter.read(input_data)

   # Transferindo Modelos de Simulação
   svg_interpreter.model = dat_interpreter.model

   # Identificando Sistema de Projeção
   supported_projections = ('plane_xy', 'plane_yz', 'plane_xz', 'isometric')
   projection = supported_projections[0]
   if len(args) > 0:
      if args[0] in supported_projections:
         projection = args[0]
      else:
         raise KeyError(f'The projection type "{args[0]}" is not supported.')

   # Projetando Coordenadas
   if projection in supported_projections[:3]:
      axis_1, axis_2 = projection.split('_')[1]
      coordinates = [
         (n.__getattribute__(axis_1), n.__getattribute__(axis_2)) 
         for n in dat_interpreter.model.nodes.values()
      ]
   elif projection == 'isometric':
      coordinates = [
         projection_isometric(n.x, n.y, n.z) 
         for n in dat_interpreter.model.nodes.values()
      ]
   u = [iso[0] for iso in coordinates]
   v = [iso[1] for iso in coordinates]

   # Ajustando Coordenadas ao Sistema SVG
   u_min = min(u)
   u_max = max(u)
   delta_u = u_max - u_min
   v_min = min(v)
   v_max = max(v)
   delta_v = v_max - v_min
   scale_coeff = (90 / delta_u) if delta_u > delta_v else (90 / delta_v)
   for (ide, node), u_i, v_i in zip(dat_interpreter.model.nodes.items(), u, v):
      # Ajustando Coordenadas para Eixo Padrão do SVG (Tudo Positivo | Eixo Vertical Invertido)
      x = u_i - u_min
      y = abs(v_i - v_max)

      # Ajustando Escala e Posição
      x = x * scale_coeff + 5
      y = y * scale_coeff + 5

      svg_interpreter.model.add_node(ide, x, y, 0, node.weight)

   # Retornando Tradução
   return svg_interpreter.write()

# Traduções Suportadas
supported_translations = {
   ('.inp', '.dat'): inp_to_dat,
   ('.dat', '.svg'): dat_to_svg
}

def start(input_path: str, output_extension: str, args: list[str] = []):
   # Lendo Arquivo de Input
   input_data = filer.read(input_path)

   # Verificando se a Tradução é Suportada
   last_dot_index = input_path.rfind('.')
   input_extension = input_path[last_dot_index:]
   format_pair = (input_extension, output_extension)
   try:
      translation_function = supported_translations[format_pair]
   except KeyError:
      raise KeyError(f'The translation of {input_extension} to {output_extension} is not supported.')
   
   # Traduzindo
   output_data = translation_function(input_data, args)

   # Escrevendo Tradução no Output
   output_path = input_path[:last_dot_index] + output_extension
   filer.write(output_path, output_data)
