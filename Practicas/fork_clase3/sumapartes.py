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


import multiprocessing as mp
import argparse,os

def main():
    
    #Defino el parseo de argumentos
    parser = argparse.ArgumentParser(usage="\nsumapartes.py [-h HELP] [-n NUMERO] [-v VERBOSO]")
    parser.add_argument('-n', '--numero', metavar='NUMERO', type=int, default=1, help="Cantidad de procesos hijos a crear")
    parser.add_argument('-v', '--verboso', action = 'store_true' , help="Activa modo verboso , no requiere argumentos")
    args = parser.parse_args()
    numero = args.numero
    verboso = args.verboso
    
    #lanzo el metodo que creara los procesos
    process_handler(numero,verboso)

def process_handler(numero,verboso):
    pid_padre = os.getpid()
    process_list = []
    n = 0
    
    #crea la cantidad de hijos indicada en "numero" los inicializa y los mete en una lista para su futura ejecucion
    while n < numero:
        n += 1
        p = mp.Process(target=sentencia_hijo,args=(verboso,pid_padre))
        p.start()
        process_list.append(p)
        
    #ejecuta todos los procesos hijos de la lista process_list
    for p in process_list:
        p.join()

    #mata a todos los procesos hijos en ejecucion de la lista process_list
    for p in process_list:
        p.terminate()
    
def sentencia_hijo(verboso,pid_padre):
    
    #averiguo el id del proceso hijo
    #el print de esto no tiene orden especifico, depende de como maneje subprocesos el sistema operativo
    pid_hijo =  int(os.getpid())
    if verboso:
        print(f"starting process {pid_hijo}")
        suma = sumador(pid_hijo)
        print(f"hijo {pid_hijo} de padre {pid_padre}: suma = {suma}")
        print(f"ending process: {pid_hijo}")
    else:
        suma = sumador(pid_hijo)
        print(f"{pid_hijo} - {pid_padre}: {suma}")
    
#calcula la suma de todos los numeros pares desde 2 hasta el id_del hijo si es par sino queda en uno anterior
def sumador(pid_hijo):
    suma = 0
    for par in range(0,pid_hijo+1,2):
        suma = suma + par
    return suma


if __name__ == '__main__':
    main()

    

