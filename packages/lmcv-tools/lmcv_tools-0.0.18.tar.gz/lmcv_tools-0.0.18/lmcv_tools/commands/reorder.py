from subprocess import run
from platform import system as platform_system
from pathlib import Path
from itertools import combinations
from math import inf, floor
from ..interface import filer, messenger
from ..models.translation_components import DAT_Interpreter
from ..models.ansi_style import Color, Effect

# Funções de Grafos
def get_level_structure(node: int, graph: dict) -> list[dict]:
   # Variáveis Iniciais
   level_structure = list()
   max_level_length = 0
   leveled_nodes = {node}

   # Calculando Nível Inicial
   node_degree = len(graph[node])
   current_level = {node: node_degree}

   # Loop para cada Nível
   while 1:
      # Adicionando Nível Atual à Lista de Níveis
      level_structure.append(current_level)
      next_level = dict()

      # Verificando Adjacência do Nível Atual
      for n in current_level:
         adjacent_nodes = graph[n]
         for a in adjacent_nodes:
            if a not in leveled_nodes:
               leveled_nodes.add(a)
               next_level[a] = len(graph[a])
      
      # Verificando se o Nível Atual é Vazio
      if len(next_level) == 0:
         break

      # Verificando se o Comprimento do Nível é o Maior
      if len(next_level) > max_level_length:
         max_level_length = len(next_level)
      
      # Intercambiando Níveis
      current_level = next_level
   
   return level_structure, max_level_length

def get_pseudo_peripheral_node_pair(graph: dict) -> list[int]:
   # Encontrando Node de Menor Grau como Chute Inicial
   n_nodes = len(graph)
   pseudo_peripheral_node_1 = -1
   pseudo_peripheral_node_2 = -1
   min_degree = inf
   for node in range(n_nodes):
      degree = len(graph[node])
      if degree < min_degree:
         min_degree = degree
         pseudo_peripheral_node_1 = node

   # Construindo Estrutura de Nível do Node Chutado
   level_structure, _ = get_level_structure(pseudo_peripheral_node_1, graph)
   
   # Processo de Seleção (Só termina quando Tivermos um Node Inicial e Outro Final)
   while pseudo_peripheral_node_2 == -1:
      # Inicializando um Comprimento Mínimo para o Nível de Maior Comprimento
      min_level_length = inf

      # Ordenando Último Nível pelo Grau
      ordered_level = level_structure[-1]
      ordered_level = sorted(ordered_level.keys(), key = lambda k: ordered_level[k])

      # Avaliando Canditados
      level_structure_length = len(level_structure)
      n_candidates = floor(len(ordered_level) / 2) + 1
      for candidate_node in ordered_level[:n_candidates]:
         # Construindo Estrutura de Nível do Node Candidato
         candidate_level_structure, candidate_max_level_length = get_level_structure(candidate_node, graph)

         # Verificando se Canditado pode Substituir o Node Escolhido Atual
         if candidate_max_level_length < min_level_length:
               # Avaliando se o Node pode ser Inicial ou Final
               if len(candidate_level_structure) > level_structure_length:
                  level_structure = candidate_level_structure
                  pseudo_peripheral_node_1 = candidate_node
                  break
               else:
                  pseudo_peripheral_node_2 = candidate_node
                  min_level_length = candidate_max_level_length

   return pseudo_peripheral_node_1, pseudo_peripheral_node_2

def get_bandwidth(graph: dict) -> list[int]:
   bandwidth = [0] * len(graph)
   for node, adjacent_nodes in graph.items():
      min_node = min(adjacent_nodes)
      bandwidth[node] = node - min_node if min_node < node else 0
   return bandwidth

# Funções de Reordenação 
def reorder_rcm(graph: dict) -> list[int]:
   # Variáveis Iniciais
   n_nodes = len(graph)
   new_order = [0] * n_nodes

   # Encontrando Node de Menor Grau como Node Pseudo-Periférico
   pseudo_peripheral_node = 0
   min_degree = len(graph[0])
   for node in range(1, n_nodes):
      degree = len(graph[node])
      if degree < min_degree:
         min_degree = degree
         pseudo_peripheral_node = node

   # Construindo Estrutura de Nível do Node Pseudo-Periférico
   level_structure, _ = get_level_structure(pseudo_peripheral_node, graph)
   
   # Percorrendo Níveis
   order = n_nodes - 1
   for level in level_structure:
      # Ordenando Nodes do Nível por Grau
      level = sorted(level.keys(), key = lambda k: level[k], reverse = True)

      # Registrando Nova Ordem
      for node in level:
         new_order[node] = order
         order -= 1
   
   return new_order

def reorder_sloan(graph: dict) -> list[int]:
   # Encontrando Nodes Pseudo-Periféricos Inicial e Final
   node_start, node_end = get_pseudo_peripheral_node_pair(graph)
   n_nodes = len(graph)
   new_order = [0] * n_nodes

   # Calculando Lista de Distância para Node Final
   level_structure_end, _ = get_level_structure(node_end, graph)
   distances_to_end = [0] * n_nodes
   degrees = [0] * n_nodes
   for level_order, level in enumerate(level_structure_end):
      for node in level.keys():
         distances_to_end[node] = level_order
         degrees[node] = level[node]
   del level_structure_end

   # Atribuindo Status aos Nodes
   # 0 - posactive
   # 1 - active
   # 2 - preactive
   # 3 - inactive
   status = [3] * n_nodes

   # Atribuindo Prioridades
   W1 = 2
   W2 = 1
   priorities = list()
   for i in range(n_nodes):
      current_degree = degrees[i] + 1
      p = (n_nodes - current_degree) * W1 + distances_to_end[i] * W2
      priorities.append(p)
   
   # Iniciando Pilha de Nodes Elegíveis
   eligible_nodes = [node_start]
   status[node_start] = 2
   
   # Processo de Reordenação
   order = 0
   while len(eligible_nodes) != 0:
      # Ordenando Nodes por Prioridade
      eligible_nodes = sorted(eligible_nodes, key = lambda k: priorities[k])

      # Selecionando Node de Maior Prioridade
      highest_priority_node = eligible_nodes.pop()

      # Verificando se Node de Maior Prioridade é Pré-ativo
      if status[highest_priority_node] == 2:
         # Examinando Nodes Adjacentes
         adjacent_nodes_level_1 = graph[highest_priority_node]
         for a1 in adjacent_nodes_level_1:
               # Alterando Prioridade
               priorities[a1] += W1

               # Adicionando Node à Lista de Nodes Elegíveis e Atualizando Status se é Inativo
               if status[a1] == 3:
                  status[a1] = 2
                  eligible_nodes.append(a1)

      # Adicionando Nova Ordem ao Node de Maior Prioridade
      status[highest_priority_node] = 0
      new_order[highest_priority_node] = order
      order += 1

      # Examinando Nodes Adjacentes
      adjacent_nodes_level_1 = graph[highest_priority_node]
      for a1 in adjacent_nodes_level_1:
         # Verificando se Node de Maior Prioridade é Pré-ativo
         if status[a1] == 2:
               # Alterando Prioridade e Status
               priorities[a1] += W1
               status[a1] = 1

               # Examinando Nodes Adjacentes
               adjacent_nodes_level_2 = graph[a1]
               for a2 in adjacent_nodes_level_2:
                  # Verificando se Node de Maior Prioridade é Ativo ou Pré-ativo
                  if (status[a2] == 1) or (status[a2] == 2):
                     # Alterando Prioridade
                     priorities[a2] += W1

                  # Verificando se Node de Maior Prioridade é Inativo
                  elif status[a2] == 3:
                     # Alterando Prioridade, Status e Adicionando à Lista de Nodes Elegíveis
                     priorities[a2] += W1
                     status[a2] = 2
                     eligible_nodes.append(a2)

   return new_order

def reorder_boost_sloan(graph: dict) -> list[int]:
   # Tentando Importar Módulo
   try:
      from ..resources.shared.boost import reorder_sloan as rs
   except ModuleNotFoundError:
      raise OSError('Your Operational System has no support for this Reordering Method.')
   
   # Gerando Reordenação
   new_order = [0] * len(graph)
   rs(graph, new_order)
   
   return new_order

# Métodos de Reordenação Suportados
supported_methods = {
   'rcm': reorder_rcm,
   'sloan': reorder_sloan,
   'boost_sloan': reorder_boost_sloan
}

# Função de Inicialização
def start(method: str, dat_path: str, flags: list[str] = []):
   # Verificando se o Método de Reordenação é Suportado
   try:
      reordering_function = supported_methods[method]
   except KeyError:
      raise KeyError(f'The method "{method}" is not supported.')

   # Lendo Arquivo .dat
   dat_data = filer.read(dat_path)

   # Interpretando Informações
   dat_interpreter = DAT_Interpreter()
   dat_interpreter.read(dat_data)
   model = dat_interpreter.model

   # Criando Matriz do Grafo para Reordenação
   n = len(model.nodes)
   graph = {i: set() for i in range(n)}
   for group in model.element_groups.values():
      for element in group.elements.values():
         for i, j in combinations(element.node_ides, 2):
            i -= 1
            j -= 1
            graph[i].add(j)
            graph[j].add(i)

   # Reordenando
   new_order = reordering_function(graph)

   # Adicionando Reordenação ao Modelo de Simulação
   new_order = [n + 1 for n in new_order]
   dat_interpreter.model.node_solver_order = new_order

   # Gerando e Incluindo Codificação da Ordem no Arquivo .dat
   order_data = dat_interpreter.write_node_solver_order()
   dat_data = dat_data.replace('%ELEMENT\n', order_data[1:] + '\n%ELEMENT\n')
   filer.write(dat_path, dat_data)

   # Verificando Flags
   if ('-i' in flags) or ('--info' in flags):
      # Calculando Informações Adiconais sobre a Reordenação
      # Gerando Novo Grafo com a Reordenação
      new_graph = {i: set() for i in range(n)}
      for node, adjacent_nodes in graph.items():
         new_graph[new_order[node] - 1] = {new_order[a] - 1 for a in adjacent_nodes}

      # Calculando Larguras de Banda
      old_bandwidth = get_bandwidth(graph)
      new_bandwidth = get_bandwidth(new_graph)

      # Calculando PercentuaL de Redução de Largura de Banda Máxima
      old_max_bandwidth = max(old_bandwidth)
      new_max_bandwidth = max(new_bandwidth)
      max_bandwidth_reduction = (old_max_bandwidth - new_max_bandwidth) / old_max_bandwidth
      result_color = Color.green if max_bandwidth_reduction > 0 else Color.red
      messenger.info(f'Max Bandwidth Reduction = {result_color}{max_bandwidth_reduction:.2%}{Effect.reset}')

      # Calculando PercentuaL de Redução de Largura de Banda Média
      old_avg_bandwidth = sum(old_bandwidth) / n
      new_avg_bandwidth = sum(new_bandwidth) / n
      avg_bandwidth_reduction = (old_avg_bandwidth - new_avg_bandwidth) / old_avg_bandwidth
      result_color = Color.green if avg_bandwidth_reduction > 0 else Color.red
      messenger.info(f'Average Bandwidth Reduction = {result_color}{avg_bandwidth_reduction:.2%}{Effect.reset}')