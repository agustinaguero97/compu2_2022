"""Escribir un programa en Python que reciba los siguientes argumentos por línea de comandos:

-n <N>
-r <R>
-h
-f <ruta_archivo>
-v
El programa deberá abrir (crear si no existe) un archivo de texto cuyo path ha sido pasado por argumento con -f.

El programa debe generar <N> procesos hijos. Cada proceso estará asociado a una letra del alfabeto 
(el primer proceso con la "A", el segundo con la "B", etc). 
Cada proceso almacenará en el archivo su letra <R> veces con un delay de un segundo entre escritura y escritura 
(realizar flush() luego de cada escritura).

El proceso padre debe esperar a que los hijos terminen, 
luego de lo cual deberá leer el contenido del archivo y mostrarlo por pantalla.

La opción -h mostrará ayuda. La opción -v activará el modo verboso, 
en el que se mostrará antes de escribir cada letra en el archivo: Proceso <PID> escribiendo letra 'X'.

Ejemplo 1:
./escritores.py -n 3 -r 4 -f /tmp/letras.txt

ABCACBABCBAC
Ejemplo 2:
./escritores.py -n 3 -r 5 -f /tmp/letras.txt -v
Proceso 401707 escribiendo letra 'A'
Proceso 401708 escribiendo letra 'B'
Proceso 401709 escribiendo letra 'C'
Proceso 401708 escribiendo letra 'B'
Proceso 401707 escribiendo letra 'A'
Proceso 401709 escribiendo letra 'C'
Proceso 401707 escribiendo letra 'A'
Proceso 401708 escribiendo letra 'B'
Proceso 401709 escribiendo letra 'C'
Proceso 401707 escribiendo letra 'A'
Proceso 401708 escribiendo letra 'B'
Proceso 401709 escribiendo letra 'C'
Proceso 401707 escribiendo letra 'A'
Proceso 401708 escribiendo letra 'B'
Proceso 401709 escribiendo letra 'C'
ABCBACABCABCABC
"""
import argparse, os, time

#this method write to the file the letter
def file_writter(path_dir,letter_of_this_process):
    mode = 'a' if os.path.exists(path_dir) else 'w'
    with open(path_dir, mode) as f:
        f.write(letter_of_this_process)
        f.flush()
        f.close()
        time.sleep(1)

        

#logic of the child process
def child_process(verbose,amount,path_dir,letter_of_this_process):
    pid = os.getpid()
    for am in range(0,amount):
        if verbose:
            print(f"Process {pid} writing {letter_of_this_process}")
            file_writter(path_dir,letter_of_this_process)
        else:
            print(f"{letter_of_this_process}")
            file_writter(path_dir,letter_of_this_process)
        
            

def creator(number,verbose,amount,path_dir,letters):
    #create the amount of childs 
    for x in range(1,number+1):
        retVal = os.fork()

        # Separate logic for parent and child
        #child logic
        if retVal == 0:

            letter_of_this_process = letters.pop(0)
            child_process(verbose,amount,path_dir,letter_of_this_process)
            #close the process child
            os._exit(0)
        
        #parent logic
        else:
            letter_of_this_process = letters.pop(0)
    #parent wait for all the childs to end 
    os.waitpid(retVal,0)
    

def main():
    #Defino el parseo de argumentos
    parser = argparse.ArgumentParser(usage="\nescritores.py [-h HELP] [-n NUMBER] [-f PATH] [-r AMOUNT] [-v VERBOSE]")
    parser.add_argument('-n', '--number', metavar='NUMBER', type=int, default=1, help="amount of child process to create")
    parser.add_argument('-f', '--path', metavar='PATH', type=str, help='Path of the file that storage the letters')
    parser.add_argument('-r', '--amount',metavar='AMOUNT', type=int,default=1,help='Amount of times that the letter repeats itself')
    parser.add_argument('-v', '--verbose',action='store_true', help="Activate verbose mode")
    letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    args = parser.parse_args()
    number = args.number
    path_dir = args.path
    amount = args.amount
    verbose = args.verbose
    #this clean the file if there is any
    open(path_dir, 'w').close()
    creator(number,verbose,amount,path_dir,letters)
    

    
    
if __name__ == "__main__":
    main()