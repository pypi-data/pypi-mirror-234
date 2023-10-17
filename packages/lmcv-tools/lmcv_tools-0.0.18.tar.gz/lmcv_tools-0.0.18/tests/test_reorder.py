import unittest
import os

class DefaultTest(unittest.TestCase):
   def default_test(self, method: str, benchmark_name: str, benchmark_id: str = None):
      # Definindo paths
      dat_path = 'tests/benchmark/reorder/' + benchmark_name + '.dat'
      temp_path = dat_path[:-4] + '_temp.dat'
      exp_path = dat_path[:-4] + '_exp'
      if benchmark_id:
         exp_path += '_'+ benchmark_id
      exp_path += '.dat'

      # Copiando Dados para Arquivo Temporário de Teste
      dat_file = open(dat_path, 'r')
      dat_data = dat_file.read()
      dat_file.close()
      temp_file = open(temp_path, 'w')
      temp_file.write(dat_data)
      temp_file.close()
      del dat_data

      # Executando Reordenação
      command = f'python -m lmcv_tools reorder {method} {temp_path}'
      code = os.system(command)
      self.assertEqual(code, 0, 'A reordenação falhou.')

      # Comparando Reordenação com o Resultado Esperado
      exp_file = open(exp_path, 'r')
      exp_data = exp_file.read()
      exp_file.close()
      temp_file = open(temp_path, 'r')
      temp_data = temp_file.read()
      temp_file.close()
      self.assertEqual(temp_data, exp_data, 'A extração está incorreta.')

      # Removendo Arquivo Temporário Gerado
      os.remove(temp_path)

class TestMethods(DefaultTest):
   def test_rcm(self):
      benchmark = ('ComplexPipe', 'rcm')
      self.default_test('rcm', *benchmark)
   
   def test_sloan(self):
      benchmark = ('ComplexPipe', 'sloan')
      self.default_test('sloan', *benchmark)

   def test_boost_sloan(self):
      benchmark = ('ComplexPipe', 'boost_sloan')
      self.default_test('boost_sloan', *benchmark)

class TestBases(DefaultTest):
   def test_lagrange(self):
      self.default_test('rcm', 'SquareLagrange')
   
   def test_bezier_triangle(self):
      self.default_test('rcm', 'SquareBezierTriangle')

   def test_bezier_surface(self):
      self.default_test('rcm', 'SquareBezierSurface')
   
   def test_bspline_surface(self):
      self.default_test('rcm', 'SquareBsplineSurface')
   