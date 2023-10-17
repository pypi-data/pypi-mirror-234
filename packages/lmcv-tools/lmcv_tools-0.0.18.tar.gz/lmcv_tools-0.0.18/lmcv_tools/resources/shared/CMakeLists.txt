cmake_minimum_required(VERSION 3.4...3.18)
project(example LANGUAGES CXX)

# Definindo Caminho da Arquivos de Configuração do CMake para o pybind11
set(pybind11_DIR ../../../share/cmake/pybind11)

# Criando Módulo do "boost"
find_package(pybind11)
pybind11_add_module(boost boost.cpp)

# Incluindo Caminho dos Headers do Boost C++
target_include_directories(boost PUBLIC "C:/Program Files/Boost/boost_1_83_0")
target_include_directories(boost PUBLIC "/mnt/c/Program Files/Boost/boost_1_83_0")