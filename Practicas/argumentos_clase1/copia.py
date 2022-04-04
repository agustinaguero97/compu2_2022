"""
Escribir un programa que reciba dos nombres de archivos por línea de órdenes utilizando los parámetros “-i” y “-o” procesados con argparse.
El programa debe verificar que el archivo pasado a “-i” exista en el disco. De ser así, lo abrirá en modo de solo lectura, leerá su contenido, 
y copiará dicho contenido en un archivo nuevo cuyo nombre será el pasado a “-o”. Si el archivo nuevo ya existe, deberá sobreescribirlo.
"""
import argparse,os,sys

class NoFile(Exception):
    def __init__(self, message):
        print(message)

def copia_a(arch_cop,data):
    with open(arch_cop, "a") as file:
        file.write(data)
    print("listo")


def main():
    parser = argparse.ArgumentParser(usage="\ncopia.py [-h] [-i ARCHI_ORIGINAL] [-o ARCHI_COPIA]")
    parser.add_argument('-i', '--archi_or', metavar='ARCHI_ORIGINAL', type=str, help="Archivo que vamos a copiar")
    parser.add_argument('-o', '--archi_cp', metavar='ARCHI_COPIA', type=str,help="Archivo al donde termina la copia")
    args = parser.parse_args()
    arch_ori = args.archi_or
    arch_cop = args.archi_cp
    try:
        file = open(arch_ori,"r")
        data = file.read()
        file.close()

    except NoFile:
        print(" No such file or directory: '"+ arch_ori +"'")
        sys.exit()
        
    copia_a(arch_cop,data)
        
    
if __name__ == '__main__':
    main()