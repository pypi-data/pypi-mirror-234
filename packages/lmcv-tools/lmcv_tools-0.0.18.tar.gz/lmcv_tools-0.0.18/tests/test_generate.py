import unittest
import os

class DefaultTest(unittest.TestCase):
   def default_test(self, artifact_name: str, artifact_extension: str, test_id: str, args: list):
      # Definindo paths
      path = 'tests/benchmark/generate/'
      artifact_path = f'{path}{artifact_name}.{artifact_extension}'
      exp_path = f'{artifact_path[:-4]}_exp_{test_id}.{artifact_extension}'

      # Gerando Artefato
      args_joined = ' '.join(args)
      command = f'python -m lmcv_tools generate {artifact_name} {args_joined} {artifact_path}'
      code = os.system(command)
      self.assertEqual(code, 0, 'A geração falhou.')

      # Comparando Artefato com o Resultado Esperado
      artifact_file = open(artifact_path, 'r')
      exp_file = open(exp_path, 'r')
      artifact_data = artifact_file.read()
      exp_data = exp_file.read()
      artifact_file.close()
      exp_file.close()
      self.assertEqual(artifact_data, exp_data, 'O Artefato está incorreto.')

      # Removendo Arquivo .csv Gerado
      # os.remove(artifact_path)

class TestVirtualLaminas(DefaultTest):
   def test_shell_element(self):
      name = 'virtual_laminas'
      ext = 'inp'
      test_id = 'shell'
      args = ['2', 'Shell', '0.5', '3', '1.0', 'voigt', '90.0', '380.0', '0.27', '0.30', '2000', '1000', 'False']
      self.default_test(name, ext, test_id, args)

   def test_solid_element(self):
      name = 'virtual_laminas'
      ext = 'inp'
      test_id = 'solid'
      args = ['2', 'Solid', '0.5', '3', '1.0', 'voigt', '90.0', '380.0', '0.27', '0.30', '2000', '1000', 'False']
      self.default_test(name, ext, test_id, args)

   def test_voigt_model(self):
      name = 'virtual_laminas'
      ext = 'inp'
      test_id = 'voigt'
      args = ['40', 'Solid', '0.25', '3', '1.0', 'voigt', '90.0', '380.0', '0.27', '0.30', '2000', '1000', 'False']
      self.default_test(name, ext, test_id, args)
   
   def test_mori_tanaka_model(self):
      name = 'virtual_laminas'
      ext = 'inp'
      test_id = 'mori_tanaka'
      args = ['40', 'Solid', '0.25', '3', '1.0', 'mori_tanaka', '90.0', '380.0', '0.27', '0.30', '2000', '1000', 'False']
      self.default_test(name, ext, test_id, args)
   
   def test_hashin_shtrikman_upper_bound_model_1(self):
      name = 'virtual_laminas'
      ext = 'inp'
      test_id = 'hs_ub_1'
      args = ['40', 'Solid', '0.25', '3', '1.0', 'hashin_shtrikman_upper_bound', '90.0', '380.0', '0.27', '0.30', '2000', '1000', 'False']
      self.default_test(name, ext, test_id, args)
   
   def test_hashin_shtrikman_lower_bound_model_1(self):
      name = 'virtual_laminas'
      ext = 'inp'
      test_id = 'hs_lb_1'
      args = ['40', 'Solid', '0.25', '3', '1.0', 'hashin_shtrikman_lower_bound', '90.0', '380.0', '0.27', '0.30', '2000', '1000', 'False']
      self.default_test(name, ext, test_id, args)
   
   def test_hashin_shtrikman_upper_bound_model_2(self):
      name = 'virtual_laminas'
      ext = 'inp'
      test_id = 'hs_ub_2'
      args = ['40', 'Solid', '0.25', '3', '1.0', 'hashin_shtrikman_upper_bound', '380.0', '90.0', '0.30', '0.27', '1000', '2000', 'False']
      self.default_test(name, ext, test_id, args)
   
   def test_hashin_shtrikman_lower_bound_model_2(self):
      name = 'virtual_laminas'
      ext = 'inp'
      test_id = 'hs_lb_2'
      args = ['40', 'Solid', '0.25', '3', '1.0', 'hashin_shtrikman_lower_bound', '380.0', '90.0', '0.30', '0.27', '1000', '2000', 'False']
      self.default_test(name, ext, test_id, args)

   def test_smart_laminas_1(self):
      name = 'virtual_laminas'
      ext = 'inp'
      test_id = 'smart_1'
      args = ['100', 'Shell', '3.5', '3', '0.2', 'voigt', '90.0', '380.0', '0.27', '0.30', '2000', '1000', 'True']
      self.default_test(name, ext, test_id, args)
   
   def test_smart_laminas_2(self):
      name = 'virtual_laminas'
      ext = 'inp'
      test_id = 'smart_2'
      args = ['100', 'Shell', '3.5', '3', '5', 'voigt', '90.0', '380.0', '0.27', '0.30', '2000', '1000', 'True']
      self.default_test(name, ext, test_id, args)
