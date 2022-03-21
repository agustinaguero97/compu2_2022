"""
Ejercicio 1 - Getopt
Crear una calculadora, donde se pase como argumentos luego de la opción -o el operador que se va a ejecutar (+,-,*,/),
luego de -n el primer número de la operación, y de -m el segundo número.

Ejemplo:
python3 calc.py -o + -n 5 -m 6
5 + 6 = 11
Considerar que el usuario puede ingresar los argumentos en cualquier orden.
El programa deberá verificar que los argumentos sean válidos (no repetidos, números enteros, y operaciones válidas.
"""

import sys
import getopt
def calculadora(opts,args):
    for op,arg in opts:
        if op == '-n':
            num_uno = float(arg)
        elif op == '-m':
            num_dos = float(arg)
    for op, arg in opts:
        
        if op == '-o' and arg == '+':
            suma = num_uno+num_dos
            print(f'suma: {num_uno}+{num_dos}={suma}' )
        elif op == '-o' and arg == '-':
            resta = num_uno-num_dos
            print(f'resta: {num_uno}-{num_dos}={resta}' )
        elif op == '-o' and arg == '/':
            division = num_uno/num_dos
            print(f'division: {num_uno}/{num_dos}={division}' )
        elif op == '-o' and arg == '++':                                    #no se porque si pongo * me toma el nombre del archivo, calc.py
            mul = num_uno*num_dos
            print(f'multiplicacion: {num_uno}*{num_dos}={mul}' )

        
    """for op, arg in opts:
        print(arg)
        if arg == '+':
            suma = op in ['-n']
            print(f"aca {suma}")
        elif arg == '-':
            print("rest")
        elif arg == 'mul':
            print("multi")
        elif arg == '/':
            print("div")"""
def main():
    try:
        (opts,args) = getopt.getopt(sys.argv[1:], 'o:n:m:', ["opciones","numero uno","numero dos"])
        if len(opts) != 3:
            print("erronea cantidad de argumentos")
            sys.exit(1)
        calculadora(opts,args)
    except getopt.GetoptError as err:
        print(err)

if __name__ == '__main__':
    main()
    #a mi parecer esta re mal hecho que se yo

