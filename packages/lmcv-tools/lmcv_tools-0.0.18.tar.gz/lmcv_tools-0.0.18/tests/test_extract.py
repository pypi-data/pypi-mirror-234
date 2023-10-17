import unittest
import os

class DefaultTest(unittest.TestCase):
   def default_test(self, benchmark_name: str, benchmark_id: str, attributes: list[str], condition: str):
      # Definindo paths
      pos_path = 'tests/benchmark/extract/' + benchmark_name + '.pos'
      csv_path = pos_path[:-3] + 'csv'
      exp_path = pos_path[:-4] + '_exp_'+ benchmark_id + '.csv'

      # Extraindo Dados
      attributes_joined = ' '.join(attributes)
      command = f'python -m lmcv_tools extract {attributes_joined} from {pos_path}'
      if condition:
         command += f' where {condition}'
      code = os.system(command)
      self.assertEqual(code, 0, 'A extração falhou.')

      # Comparando Extração com o Resultado Esperado
      csv_file = open(csv_path, 'r')
      exp_file = open(exp_path, 'r')
      csv_data = csv_file.read()
      exp_data = exp_file.read()
      csv_file.close()
      exp_file.close()
      self.assertEqual(csv_data, exp_data, 'A extração está incorreta.')

      # Removendo Arquivo .csv Gerado
      os.remove(csv_path)

class TestSingleAttributes(DefaultTest):
   def test_step_id(self):
      benchmark = ('CirclePlate_Plastic', 'step_id')
      attributes = ['step.id']
      condition = ''
      self.default_test(*benchmark, attributes, condition)
   
   def test_step_factor(self):
      benchmark = ('CirclePlate_Plastic', 'step_factor')
      attributes = ['step.factor']
      condition = ''
      self.default_test(*benchmark, attributes, condition)

   def test_node_id(self):
      benchmark = ('CirclePlate_Plastic', 'node_id')
      attributes = ['node.id']
      condition = ''
      self.default_test(*benchmark, attributes, condition)

   def test_node_x(self):
      benchmark = ('CirclePlate_Plastic', 'node_x')
      attributes = ['node.x']
      condition = ''
      self.default_test(*benchmark, attributes, condition)
   
   def test_node_y(self):
      benchmark = ('CirclePlate_Plastic', 'node_y')
      attributes = ['node.y']
      condition = ''
      self.default_test(*benchmark, attributes, condition)
   
   def test_node_z(self):
      benchmark = ('CirclePlate_Plastic', 'node_z')
      attributes = ['node.z']
      condition = ''
      self.default_test(*benchmark, attributes, condition)
   
   def test_step_node_u(self):
      benchmark = ('CirclePlate_Plastic', 'step_node_u')
      attributes = ['step.node.u']
      condition = ''
      self.default_test(*benchmark, attributes, condition)
   
   def test_step_node_v(self):
      benchmark = ('CirclePlate_Plastic', 'step_node_v')
      attributes = ['step.node.v']
      condition = ''
      self.default_test(*benchmark, attributes, condition)
   
   def test_step_node_w(self):
      benchmark = ('CirclePlate_Plastic', 'step_node_w')
      attributes = ['step.node.w']
      condition = ''
      self.default_test(*benchmark, attributes, condition)
   
   def test_buckling_id(self):
      benchmark = ('SquarePlate', 'buckling_id')
      attributes = ['buckling.id']
      condition = ''
      self.default_test(*benchmark, attributes, condition)
   
   def test_buckling_factor(self):
      benchmark = ('SquarePlate', 'buckling_factor')
      attributes = ['buckling.factor']
      condition = ''
      self.default_test(*benchmark, attributes, condition)
   
   def test_buckling_node_u(self):
      benchmark = ('SquarePlate', 'buckling_node_u')
      attributes = ['buckling.node.u']
      condition = ''
      self.default_test(*benchmark, attributes, condition)
   
   def test_buckling_node_v(self):
      benchmark = ('SquarePlate', 'buckling_node_v')
      attributes = ['buckling.node.v']
      condition = ''
      self.default_test(*benchmark, attributes, condition)
   
   def test_buckling_node_w(self):
      benchmark = ('SquarePlate', 'buckling_node_w')
      attributes = ['buckling.node.w']
      condition = ''
      self.default_test(*benchmark, attributes, condition)
   
   def test_vibration_id(self):
      benchmark = ('HeartPlate', 'vibration_id')
      attributes = ['vibration.id']
      condition = ''
      self.default_test(*benchmark, attributes, condition)
   
   def test_vibration_factor(self):
      benchmark = ('HeartPlate', 'vibration_factor')
      attributes = ['vibration.factor']
      condition = ''
      self.default_test(*benchmark, attributes, condition)
   
   def test_vibration_node_u(self):
      benchmark = ('HeartPlate', 'vibration_node_u')
      attributes = ['vibration.node.u']
      condition = ''
      self.default_test(*benchmark, attributes, condition)
   
   def test_vibration_node_v(self):
      benchmark = ('HeartPlate', 'vibration_node_v')
      attributes = ['vibration.node.v']
      condition = ''
      self.default_test(*benchmark, attributes, condition)
   
   def test_vibration_node_w(self):
      benchmark = ('HeartPlate', 'vibration_node_w')
      attributes = ['vibration.node.w']
      condition = ''
      self.default_test(*benchmark, attributes, condition)

class TestMultipleAttributes(DefaultTest):
   def test_multiple_1(self):
      benchmark = ('CirclePlate_Plastic', 'multiple_1')
      attributes = ['step.id', 'step.factor']
      condition = ''
      self.default_test(*benchmark, attributes, condition)
   
   def test_multiple_2(self):
      benchmark = ('CirclePlate_Plastic', 'multiple_2')
      attributes = ['step.factor', 'step.node.u']
      condition = ''
      self.default_test(*benchmark, attributes, condition)
   
   def test_multiple_3(self):
      benchmark = ('CirclePlate_Plastic', 'multiple_3')
      attributes = ['step.node.u', 'node.id', 'node.x']
      condition = ''
      self.default_test(*benchmark, attributes, condition)
   
   def test_multiple_unrelated_1(self):
      benchmark = ('CirclePlate_Plastic', 'multiple_ur_1')
      attributes = ['node.id', 'step.id']
      condition = ''
      self.default_test(*benchmark, attributes, condition)
   
   def test_multiple_unrelated_2(self):
      benchmark = ('CirclePlate_Plastic', 'multiple_ur_2')
      attributes = ['node.id', 'step.id', 'node.x']
      condition = ''
      self.default_test(*benchmark, attributes, condition)
   
class TestCondition(DefaultTest):
   def test_condition_equal(self):
      benchmark = ('CirclePlate_Plastic', 'cond_eq')
      attributes = ['step.id', 'step.factor']
      condition = 'step.id = 5'
      self.default_test(*benchmark, attributes, condition)
   
   def test_condition_less(self):
      benchmark = ('CirclePlate_Plastic', 'cond_ls')
      attributes = ['step.id', 'step.factor']
      condition = 'step.id "<" 5'
      self.default_test(*benchmark, attributes, condition)
   
   def test_condition_greater(self):
      benchmark = ('CirclePlate_Plastic', 'cond_gt')
      attributes = ['step.id', 'step.factor']
      condition = 'step.id ">" 5'
      self.default_test(*benchmark, attributes, condition)
   
   def test_condition_less_or_equal(self):
      benchmark = ('CirclePlate_Plastic', 'cond_le')
      attributes = ['step.id', 'step.factor']
      condition = 'step.id "<=" 5'
      self.default_test(*benchmark, attributes, condition)
   
   def test_condition_greater_or_equal(self):
      benchmark = ('CirclePlate_Plastic', 'cond_ge')
      attributes = ['step.id', 'step.factor']
      condition = 'step.id ">=" 5'
      self.default_test(*benchmark, attributes, condition)
   
   def test_condition_different(self):
      benchmark = ('CirclePlate_Plastic', 'cond_df')
      attributes = ['step.id', 'step.factor']
      condition = 'step.id "!=" 5'
      self.default_test(*benchmark, attributes, condition)
   
   def test_condition_in_1(self):
      benchmark = ('CirclePlate_Plastic', 'cond_in_1')
      attributes = ['step.id', 'step.factor']
      condition = 'step.id in 1:4'
      self.default_test(*benchmark, attributes, condition)
   
   def test_condition_in_2(self):
      benchmark = ('CirclePlate_Plastic', 'cond_in_2')
      attributes = ['step.id', 'step.factor']
      condition = 'step.id in 1:11:2'
      self.default_test(*benchmark, attributes, condition)

   def test_condition_and(self):
      benchmark = ('CirclePlate_Plastic', 'cond_and')
      attributes = ['step.id', 'step.factor']
      condition = 'step.id "<" 9 and step.factor ">" 1.6'
      self.default_test(*benchmark, attributes, condition)
   
   def test_condition_or(self):
      benchmark = ('CirclePlate_Plastic', 'cond_or')
      attributes = ['step.id', 'step.factor']
      condition = 'step.factor "<" 0.5 or step.factor ">" 2.5'
      self.default_test(*benchmark, attributes, condition)