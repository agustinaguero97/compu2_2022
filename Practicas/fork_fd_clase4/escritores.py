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

class ToBig(Exception):
    def __init__(self,message):
        print(message)
        os._exit(0)

class NoPath(Exception):
    def __init__(self,message):
        print(message)
        os._exit(0)

class InvalidFormat(Exception):
    def __init__(self,message):
        print(message)
        os._exit(0)
    
    

class Escritores():
    def __init__(self,number,verbose,amount,path_dir):
        self.number = number
        self.verbose = verbose
        self.amount = amount
        self.path_dir = path_dir
        self.letters = ['A','B','C','D','E','F','G',
                        'H','I','J','K','L','M','N',
                        'O','P','Q','R','S','T','U',
                        'V','W','X','Y','Z']
        

    def file_writter(self,letter_of_this_process):
        #'a' allow me to append new content, and not overwrit it
        #also mode will allow me to create a file if it does not exits with the path given
        mode = 'a' if os.path.exists(self.path_dir) else 'w'
        with open(self.path_dir, mode) as f:
            f.write(letter_of_this_process)
            #flush will clear the buffer every time a write its done
            f.flush()
            f.close()
            time.sleep(1)

    def child_process(self,letter_of_this_process):
        pid = os.getpid()
        for am in range(0,self.amount):
            if self.verbose:
                print(f"PPID: {os.getppid()} ,Process {pid} writing {letter_of_this_process} ")
            else:
                print(f"{letter_of_this_process}")
            escritores.file_writter(letter_of_this_process)
    
    #behavior of the child process and the parent process
    def creator(self):
        #create the amount of childs 
        for _x in range(1,self.number+1):
            retVal = os.fork()

            # Separate logic for parent and child
            #child logic
            if retVal == 0:
                #assing the first letter of the list letters, the parent will handle the list itself
                letter_of_this_process = self.letters[0]
                escritores.child_process(letter_of_this_process)
                #close the process child
                os._exit(0)
            
            #parent logic
            else:
                #if the parent does not pop the element of the list, the childs with only use 'A'
                letter_of_this_process = self.letters.pop(0)
        #parent wait for all the childs to end 
        os.waitpid(retVal,0)

def main():
    #Define the arguments
    parser = argparse.ArgumentParser(usage="\nescritores.py [-h HELP] [-n NUMBER] [-f PATH] [-r AMOUNT] [-v VERBOSE]")
    parser.add_argument('-n', '--number', 
                        metavar='NUMBER',
                        type=int, 
                        default=1,
                        help="amount of child process to create")
    
    parser.add_argument('-f', '--path', 
                        metavar='PATH', 
                        type=str, 
                        help='Path of the file that storage the letters, must be a .txt')
    
    parser.add_argument('-r', '--amount',
                        metavar='AMOUNT', 
                        type=int,
                        default=1,
                        help='Amount of times that the process repeats the letter')
    
    parser.add_argument('-v', '--verbose',
                        action='store_true', 
                        help="Activate verbose mode, no value requiered")

    args = parser.parse_args()
    number = args.number
    path_dir = args.path
    amount = args.amount
    verbose = args.verbose
    
    #if a put a number greater that 26, cant assing a letter to each process
    if number > 26:
        raise ToBig(f"\nError: cant assing one letter to every process: letters:26 , process:{number}, check -h ")
    
    #check if a path was entered
    if not path_dir:
        raise NoPath("\nError: No path entered, check -h")

    #this blocks me from putting a file that is not a txt
    if not path_dir.endswith(".txt"):
        raise InvalidFormat("\nError: file is an invalid format, must be .txt, check -h")
    
    #this clean the file if there is any content in it
    if os.path.isfile(path_dir):
        open(path_dir, 'w').close()
        
    return number , verbose , amount , path_dir
            
if __name__ == "__main__":
    number, verbose, amount, path_dir = main()
    escritores = Escritores(number, verbose, amount, path_dir)
    escritores.creator()