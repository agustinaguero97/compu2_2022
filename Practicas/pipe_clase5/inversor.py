"""Escriba un programa que abra un archvo de texto pasado por argumento utilizando el modificador -f.

El programa deberá generar tantos procesos hijos como líneas tenga el archivo de texto.
El programa deberá enviarle, vía pipes (os.pipe()), cada línea del archivo a un hijo.
Cada hijo deberá invertir el orden de las letras de la línea recibida, y se lo enviará al proceso padre nuevamente, 
también usando os.pipe().
El proceso padre deberá esperar a que terminen todos los hijos,
y mostrará por pantalla las líneas invertidas que recibió por pipe.

Ejemplo:
Contenido del archivo /tmp/texto.txt

Hola Mundo
que tal
este es un archivo
de ejemplo.

Ejecución:

python3 inversor.py -f /tmp/texto.txt
ovihcra nu se etse
.olpmeje ed
lat euq
odnuM aloH"""

#DOES NOT WORK CORRECTLY, THE PARENT SHOULD SEND THE LINE TO THE CHILD TROUGH A PIPE. THEN THE CHILD RECEIVES IT,PROCESS THAT LINE, AND SEND IT BACK
#PROBABLY WITH TWO PIPES
#ONE WHERE THE PARENT SEND DATA(this one is not done)
#OTHER WHERE THE PARENT RECEIVES DATA(this one is done)

import os,argparse,time

class InvalidFormat(Exception):
    def __init__(self,message):
        print(message)
        os._exit(0)
        
class NoContent(Exception):
    def __init__(self,message):
        print(message)
        os._exit(0)

class Inversor():
    def __init__(self,dir_path):
        self.dir_path = dir_path
        self.file_content_to_list = []
        self.r_parent,self.w_child = os.pipe()
        
        #other pipe
        #self.w_parent,self.r_child = os.pipe()
        
    def data_harvest(self):
        with open(self.dir_path, 'r') as f:
            # read an store all lines into list
            self.file_content_to_list = f.readlines()
            print(self.file_content_to_list)
    
    def parent_n_child(self):
        
        for line in self.file_content_to_list:
            
            #for every element of the list, create a child process    
            retval = os.fork()
            
            if retval == 0:
                
                print("__child__")
                os.close(self.r_parent)
                self.w_child = os.fdopen(self.w_child,'w')
                line_inverted = line.strip('\n')[::-1]
                self.w_child.write(f"\n{line_inverted}")
                time.sleep(1)
                self.w_child.close()
                os._exit(0)
                
            
        print("__parent__")
        os.close(self.w_child)
        self.r_parent = os.fdopen(self.r_parent)
        
        #parent process wait here until all the childs finish writing
        line_inverted = self.r_parent.read() 
            
        print(line_inverted)  


def main():
    parser = argparse.ArgumentParser(usage="\ninversor.py [-h HELP] [-f PATH]")
    parser.add_argument('-f', '--path', 
                        metavar='PATH', 
                        type=str,
                        required= True, 
                        help='Path of the file that will get his content inverted, must be a .txt')    
    args = parser.parse_args()
    dir_path = args.path
    

    #this blocks me from putting a file that is not a txt
    if not dir_path.endswith(".txt"):
        raise InvalidFormat("\nError: file is an invalid format, must be .txt, check -h")
    
    #the program wont read an empty file
    if os.path.getsize(dir_path) == 0:
        raise NoContent("The file does not have any content  to invert")
    
    
    return dir_path

if __name__ == '__main__':
    dir_path = main()
    inversor = Inversor(dir_path)
    inversor.data_harvest()
    inversor.parent_n_child()