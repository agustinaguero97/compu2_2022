"""
    Escribir un programa en Python que reciba los siguientes argumentos por línea de comandos:

-n <numero>
-h
-v
El programa debe generar <numero> procesos hijos, 
y cada proceso calculará la suma de todos los números enteros pares entre 0 y su número de PID.

El programa deberá mostrar por pantalla:

PID – PPID : <suma_pares>
El proceso padre debe esperar a que todos sus hijos terminen.

La opción -h mostrará ayuda de uso, y la opción -v habilitará el modo verboso de la aplicación. 
El modo verboso debe mostrar, además de la suma, un mensaje al inicio y al final de la ejecución de cada proceso hijo, 
que indique su inicio y fin.

Ejemplos 1:

./sumapares.py -n 2
32803 – 4658: 269009202
32800 – 4658: 268943600

Ejemplos 2:

./sumapares.py -n 2 -v
Starting process 32800
Starting process 32803
Ending process 32803
32803 – 4658: 269009202
Ending process 32800
32800 – 4658: 268943600
"""

import os,argparse,time


def ChildProcess(verboso):

    child =os.getpid()
    if verboso:
        print(f"starting process {child}")
        suma = sumador()
        print(f"PID {child} - PPID {os.getppid()}: {suma}")
        print(f"ending process: {child}")
        
    else:
        suma = sumador()
        print(f"PID {child} - PPID {os.getppid()}: {suma}")
            

def sumador():
    suma = 0
    for par in range(0,int(os.getpid())+1,2):
        suma = suma + par
    return suma

def creator(numero,verboso):
    #crea la cantidad de hijos solicitados
    for x in range(1,numero+1):
        #creation(verboso)
        retVal = os.fork()

        # Separate logic for parent and child
        #child logic
        if retVal == 0:
            #inicio la rutina del proceso hijo
            ChildProcess(verboso)
            #cierro el proceso hijo, sino tendre un hijo que haga mas hijos
            os._exit(0)
        
        #parent logic
        else:
            pass
    #parent wait for all the childs to end 
    os.waitpid(retVal,0)
    
        
def main():
    #Defino el parseo de argumentos
    parser = argparse.ArgumentParser(usage="\nsumapartes.py [-h HELP] [-n NUMERO] [-v VERBOSO]")
    parser.add_argument('-n',
                        '--numero', 
                        metavar='NUMERO',
                        type=int,
                        default=1,
                        help="Cantidad de procesos hijos a crear")
    
    parser.add_argument('-v', '--verboso', 
                        action='store_true', 
                        help="Activa modo verboso, no requiere argumentos")
    
    args = parser.parse_args()
    numero = args.numero
    verboso = args.verboso
    creator(numero,verboso)

if __name__ == "__main__":
    main()