#!/usr/bin/env python
from datetime import datetime
from os.path import exists
import argparse

def crear_si_no_existe(file:str):
    """
    PRE: file es un string que contiene el nombre del archivo
    POS: Si file no existe lo crea, en caso contrario no hace nada
    """
    if not exists("./" + file):
        with open(file, "w") as f:
            pass

def annadir_fecha(file:str):
    """
    PRE: file es un string que contiene el nombre del archivo en el que queremos escribir
    POS: añade una entrada a file con la fecha y hora actual
    """
    with open(file, "a") as f:
        now = datetime.now()
        dt_now = now.strftime("%d-%m-%Y %H:%M:%S")
        f.write(dt_now + "\n")

def comparar_fechas(fecha1_string:str, fecha2_string:str):
    """
    PRE: fecha1, fecha2 fechas dadas como cadenas de caracteres con el format: dd-mm-yy
    POS: devuelve 2 si fecha1 es una fecha futura a fecha2, 1 si fecha1 = fecha2 y 0 en caso contrario
    """

    fecha1 = datetime.strptime(fecha1_string, '%d-%m-%Y')
    fecha2 = datetime.strptime(fecha2_string, '%d-%m-%Y')

    if fecha1 == fecha2:
        return 1
    elif fecha1 < fecha2:
        return 0
    else:
        return 2

def numero_de_entradas_desde(file, to_find):
    """
    PRE: file es un string que contiene el nombre del archivo del que queremos leer, to_find
         una string con la fecha a partir de la cual hay que empezar a contar
    POS: devuelve el numero de entradas en el archivo file
    """
    n = 0
    with open(file, "r") as f:
        line = f.readline()
        while comparar_fechas(line.split(" ")[0], to_find) < 1:
            line = f.readline()
        
        while line:
            n+=1
            line = f.readline()
    return n

def primera_fecha(file:str):
    """
    PRE: file es un string que contiene el nombre del archivo del que queremos leer
    POS: Devuelve como un string la fecha  del fichero de texto file
    """
    with open(file, "r") as f:
        return f.readline().split(" ")[0]
    

def main():
    FILE = "times.log"
    crear_si_no_existe(FILE)

    parser = argparse.ArgumentParser(description="Veces encendido el Sistema")
    parser.add_argument("--show-logs", dest="date",nargs="?", type=str,
             help="Mostrar inicios del sistema desde [DATE]", const=primera_fecha(FILE))
    parser.add_argument("-a", "--add-entry", dest="add",  
             help="Añade la fecha actual al fichero FILE", action="store_true")
    args = parser.parse_args()

    if args.add:
        # en el caso de que se añada el flag -a o --add-entry se añade la fecha y hora actual
        annadir_fecha(FILE)
    elif args.date is not None:
        # si se añade el flag --show-logs muestra los inicios del sistema a partir de la fecha especificada,
        # si ninguna fecha se especifica se como valor por defecto la primera entrada, es decir
        # se cuentan el numero total de inicios del sistema
        n_entradas = str(numero_de_entradas_desde(FILE, args.date))
        print("Se ha encendido el ordenador " + n_entradas + " veces desde " + args.date)


if __name__ == "__main__":
    main()