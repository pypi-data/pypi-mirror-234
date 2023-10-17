import sys
from .interface import core

def main():
   # Iniciando Interface com os Argumentos
   core.start(sys.argv[1:])

if __name__ == '__main__':
   main()