import unittest
import os

class DefaultTest(unittest.TestCase):
   def default_test(self, benchmark_name: str, input_extension: str, output_extension: str, projection: str = ''):
      # Definindo paths
      benchmark_name = 'tests/benchmark/translate/' + benchmark_name
      input_path = benchmark_name + input_extension
      output_path = benchmark_name + output_extension
      exp_path = input_path[:-4] + '_exp' + output_extension

      # Traduzindo Benchmark
      code = os.system(f'python -m lmcv_tools translate {input_path} to {output_extension} {projection}')
      self.assertEqual(code, 0, 'A tradução falhou.')

      # Comparando Tradução com o Resultado Esperado
      output_file = open(output_path, 'r')
      exp_file = open(exp_path, 'r')
      output_data = output_file.read()
      exp_data = exp_file.read()
      output_file.close()
      exp_file.close()
      self.assertEqual(output_data, exp_data, 'A tradução está incorreta.')

      # Removendo Arquivo Gerado
      os.remove(output_path)

class Test_inp_to_dat(DefaultTest):
   def default_test(self, benchmark_name: str):
      super().default_test('inp_to_dat/' + benchmark_name, '.inp', '.dat')

   def test_triangle_S3_1x1(self):
      self.default_test('Triangle_S3_1x1')

   def test_triangle_S3_2x2(self):
      self.default_test('Triangle_S3_2x2')

   def test_triangle_STRI65_1x1(self):
      self.default_test('Triangle_STRI65_1x1')

   def test_triangle_STRI65_2x2(self):
      self.default_test('Triangle_STRI65_2x2')

   def test_square_S4_1x1(self):
      self.default_test('Square_S4_1x1')
   
   def test_square_S4_2x2(self):
      self.default_test('Square_S4_2x2')

   def test_square_S8R_1x1(self):
      self.default_test('Square_S8R_1x1')
   
   def test_square_S8R_2x2(self):
      self.default_test('Square_S8R_2x2')
   
   def test_circle_S3_S4R_4x4(self):
      self.default_test('Circle_S3_S4R_4x4')

   def test_complex_part_S8R(self):
      self.default_test('ComplexPart_S8R')

   def test_cube_C3D4_12(self):
      self.default_test('Cube_C3D4_12')
   
   def test_cube_C3D10_12(self):
      self.default_test('Cube_C3D10_12')

   def test_cube_C3D8_1x1x1(self):
      self.default_test('Cube_C3D8_1x1x1')

   def test_cube_C3D8_2x2x2(self):
      self.default_test('Cube_C3D8_2x2x2')
   
   def test_cube_C3D20_1x1x1(self):
      self.default_test('Cube_C3D20_1x1x1')

   def test_cube_C3D20_2x2x2(self):
      self.default_test('Cube_C3D20_2x2x2')

   def test_complex_part_C3D20R(self):
      self.default_test('ComplexPart_C3D20R')
   
   def test_supported_square_S4(self):
      self.default_test('SupportedSquare_S4')

class Test_dat_to_svg(DefaultTest):
   def default_test(self, benchmark_name: str, projection: str = ''):
      super().default_test('dat_to_svg/' + benchmark_name, '.dat', '.svg', projection)

   def test_circle_T3_Q4_4x4(self):
      self.default_test('Circle_T3_Q4_4x4')

   def test_heart_plate_Q8_2x2(self):
      self.default_test('HeartPlate_Q8_2x2')

   def test_heart_plate_BT2_2x2(self):
      self.default_test('HeartPlate_BT2_2x2')

   def test_heart_plate_BT3_4x4(self):
      self.default_test('HeartPlate_BT3_4x4')

   def test_disform_BT2(self):
      self.default_test('Disform_BT2')
   
   def test_disform_BT4(self):
      self.default_test('Disform_BT4')

   def test_projection_plane_xy(self):
      self.default_test('CirclePlate_BT2_plane_xy', 'plane_xy')

   def test_projection_plane_yz(self):
      self.default_test('CirclePlate_BT2_plane_yz', 'plane_yz')

   def test_projection_plane_xz(self):
      self.default_test('CirclePlate_BT2_plane_xz', 'plane_xz')

   def test_projection_isometric(self):
      self.default_test('CirclePlate_BT2_isometric', 'isometric')