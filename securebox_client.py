"""
    Prácticas de Redes de comunicaciones 2

    Autores:
        Miguel Arconada Manteca
        Mario García Pascual

    securebox_client:
        Este es el fichero que contiene el programa del cliente de SecureBox,
        el que se tiene que ejecutar.
"""

from securebox_options import parse_options, process_options

if __name__ == '__main__':
    opts = parse_options()
    process_options(opts)
