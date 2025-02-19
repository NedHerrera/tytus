from tkinter import * #importando tkinter
import tkinter as TK
import gramatica as g

import gramaticaF2 as g2

import Utils.TablaSimbolos as table
import Utils.Lista as l
import Librerias.storageManager.jsonMode as storage
from tkinter.filedialog import askopenfilename as files
import os
import webbrowser
from Utils.fila import fila
from Error import *
import Instrucciones.DML.select as select
import json

import optimizar as opt
#from select import *

##########################################################################

storage.dropAll()
datos = l.Lista({}, '')

##################################FUNCIONES#################################
def openFile():
    route = files(
        filetypes=[("TXT Files", "*.txt")]
    )
    if not route:
        salida.insert("end", "\nERROR AL ABRIR AL ARCHIVO")
        return
    editor.delete("1.0", TK.END)
    with open(route, "r") as input_file:
        text = input_file.read()
        editor.insert(TK.END, text)
    root.title(f"TYTUSDB_Parser - {route}")



def analisis():
    global datos

    salida.delete("1.0", "end")
    texto = editor.get("1.0", "end")

    #g2.tempos.restartTemp() #reinicia el contador de temporales.
    prueba = g2.parse(texto)
    try:
        escribirEnSalidaFinal(prueba['printList'])
    except:
        ''
    #print(prueba['text'])

    exepy = '''
#imports
import sys
sys.path.append('../G26/Librerias/goto')

from goto import *
import gramatica as g
import Utils.Lista as l
import Librerias.storageManager.jsonMode as storage
import Instrucciones.DML.select as select
from Error import *

#storage.dropAll()

heap = []
semerrors = []

datos = l.Lista({}, '')
l.readData(datos)
'''
    exepy += '''
#funcion intermedia
def mediador(value):
    global heap
    global semerrors
   # Analisis sintactico
    instrucciones = g.parse(heap.pop())
    for instr in instrucciones['ast'] :

        try:
            val = instr.execute(datos)
        except:
            val = (instr.execute(datos, {}))

        if isinstance(val, Error):
            'error semántico'
            print(val)
            semerrors.append(val)
        elif isinstance(instr, select.Select) :
            
            if value == 0:
                try:
                    print(val)
                    if len(val.keys()) > 1 :
                        print('El numero de columnas retornadas es mayor a 1')
                        return 0
                    for key in val:
                        if len(val[key]['columnas']) > 1 :
                            print('El numero de filas retornadas es mayor a 1')
                        else :
                            return val[key]['columnas'][0][0]
                        break
                except:
                    return 0
            else:
                print(instr.ImprimirTabla(val))
        else :
            try:
                return val.val
            except:
                print(val)

    l.writeData(datos)
'''

    exepy += '''
#funciones de plg-sql


'''
    l.readData(datos)
    optt = ""
    for val in datos.tablaSimbolos.keys():
        if val == 'funciones_':
            for func in datos.tablaSimbolos[val]:
                try:
                    f = open("./Funciones/" + func['name'] + ".py", "r")
                    pruebaaa = f.read()
                    optt = opt.optimizar(pruebaaa)
                    exepy += optt
                    f.close()
                except:
                    exepy += '#Se cambio el nombre del archivo que guarda la funcion. Funcion no encontrada'
    exepy += '''
#main
@with_goto
def main():
    global heap
'''

    exepy += str(prueba['text'])

    exepy += '''
#Ejecucion del main
if __name__ == "__main__":
    main()
'''

    f = open("./c3d.py", "w")
    f.write(exepy)
    f.close()

    '''try:
        f = open("./Utils/tabla.txt", "r")
        text = f.read()
        f.close()
        text = text.replace('\'','"')
        text = text.replace('False','"False"')
        text = text.replace('None','""')
        text = text.replace('True','"True"')
        datos.reInsertarValores(json.loads(text))
    except:
        print('error')

    instrucciones = g.parse(texto)
    erroresSemanticos = []

    try:
        hacerReporteGramatica(instrucciones['reporte'])
    except:
        print("")

    for instr in instrucciones['ast'] :

            if instr != None:
                result = instr.execute(datos)
                if isinstance(result, Error):
                    escribirEnSalidaFinal(str(result.desc))
                    erroresSemanticos.append(result)
                elif isinstance(instr, select.Select) or isinstance(instr, select.QuerysSelect):
                    escribirEnSalidaFinal(str(instr.ImprimirTabla(result)))
                else:
                    escribirEnSalidaFinal(str(result))


    f = open("./Utils/tabla.txt", "w")
    f.write(str(datos))
    f.close()

    '''
    try:
        errores = g.getMistakes()
        recorrerErrores(errores)
    #Rerrores(errores, erroresSemanticos)
        errores.clear()
    #erroresSemanticos.clear()
        reporteTabla()
        del prueba
    except:
        ''

    escribirEnSalidaFinal('Se ha generado el codigo en 3 direcciones.')
    #aqui se puede poner o llamar a las fucniones para imprimir en la consola de salida
    reptOpti = prueba['opt']
    fro = open("./Reportes/ReporteOptimizacion.txt", "w")
    fro.write(reptOpti)
    fro.close()
    
def Rerrores(errores, semanticos):
    f = open("./Reportes/Reporte_Errores.html", "w")
    f.write("<!DOCTYPE html>\n")
    f.write("<html>\n")
    f.write("   <head>\n")
    f.write('       <meta charset="UTF-8">\n')
    f.write('       <meta name="viewport" content="width=device-width, initial-scale=1.0">')
    f.write("       <title>Reporte de errores</title>\n")
    f.write('      <link rel="stylesheet" href="style.css">\n')
    f.write("   </head>\n")
    f.write("   <body>\n")
    f.write("       <p><b>Reporte de Errores<b></p>")
    f.write("       <div>")
    f.write("       <table>\n")
    f.write("           <tr class='titulo'>   <td><b>Tipo</b></td>   <td><b>Descripcion</b></td>   <td><b>Linea</b></td> </tr>\n")
    for error in errores:
        f.write("           <tr> <td>" + error.getTipo() + "</td> <td>" + error.getDescripcion() + "</td> <td>"+ error.getLinea()  + "</td> </tr>\n")
    for semantico in semanticos:
        f.write("           <tr> <td>Semantico"  + "</td> <td>" + semantico.desc + "</td> <td>" + str(semantico.line) + "</td> </tr>\n")
    f.write("       </table>\n")
    f.write("         </div>")
    f.write("   </body>\n")
    f.write("</html>\n")
    f.close()

def tabla():
    ruta = ".\\Reportes\\Reporte_TablaSimbolos.html"
    webbrowser.open(ruta)

def ast():
    g.grafo.showtree()

def gramatica():
    os.system("notepad   ./Reportes/GramaticaAutomatica.md")

def guardar():
    print("hola")

def ayuda():
    print("hola")

def mistakes():
    ruta = ".\\Reportes\\Reporte_Errores.html"
    webbrowser.open(ruta)

def recorrerErrores(errores):
    salidaE = ""
    for error in errores:
        salidaE += error.toString() + "\n"
    salida.insert("1.0", salidaE)

def hacerReporteGramatica(gramatica):
    if gramatica != None:
        f = open("./Reportes/GramaticaAutomatica.md", "w")
        f.write("# Gramatica Generada Automaticamente\n")
        f.write("La gramatica que se genero en el analisis realizado es la siguiente:\n")
        f.write("******************************************************************\n")
        f.write(gramatica)
        f.write("\n******************************************************************")
        f.close()
    else:
        f = open("./Reportes/GramaticaAutomatica.md", "w")
        f.write("#Gramatica Generada Automaticamente\n")
        f.write("No se detecto")

def reporteTabla():
    f = open("./Reportes/Reporte_TablaSimbolos.html", "w")
    f.write("<!DOCTYPE html>\n")
    f.write("<html>\n")
    f.write("   <head>\n")
    f.write('       <meta charset="UTF-8">\n')
    f.write('       <meta name="viewport" content="width=device-width, initial-scale=1.0">')
    f.write("       <title>Reporte de tabla simbolos</title>\n")
    f.write('      <link rel="stylesheet" href="style.css">\n')
    f.write("   </head>\n")
    f.write("   <body>\n")
    f.write("       <p><b>Reporte Tabla de Simbolos<b></p>\n")
    f.write("       <div>\n")
    for a in datos.tablaSimbolos:
        f.write("           <div>\n")
        f.write("               <p class='base'>BASE DE DATOS: ")
        f.write(a)
        f.write("</p>\n")
        owner = datos.tablaSimbolos[a]['owner']
        for table in datos.tablaSimbolos[a]['tablas']:
                columnas = []
                for column in datos.tablaSimbolos[a]['tablas'][table]['columns']:
                    cc = ""
                    try:
                        cc = column['name']
                    except:
                        cc = column.name
                    nombre = cc

                    tt = ""
                    try:
                        tt = column.type
                    except:
                        tt = column['type']
                    tipo = tt

                    yy = ""
                    try:
                        yy = column.size
                    except:
                        yy = column['size']
                    size = yy

                    c = fila(nombre, tipo, size)

                    ff = ""
                    try:
                        ff = column['pk']
                    except:
                        ff = column.pk
                    if ff != None:
                        c.setPK()

                    gg = ""
                    try:
                        gg = column['fk']
                    except:
                        gg = column.fk
                    if gg != None:
                        c.setFK()

                    aa = ""
                    try:
                        aa = column['unique']
                    except:
                        aa = column.unique
                    if aa != None:
                        c.setUnique()

                    bb = ""
                    try:
                        bb = column['default']
                    except:
                        bb = column.default
                    if bb == None:
                        c.setDefault('None')
                    else:
                        c.setDefault(column.default)
                    columnas.append(c)
                f.write("<p class='tabla'>Tabla: ")
                f.write(table)
                f.write("</p>")
                f.write("               <table>\n")
                f.write("                   <tr class='titulo'>   <td><b>Nombre</b></td>   <td><b>Tipo</b></td>   <td><b>Size</b></td>   <td><b>PK</b></td>  <td><b>FK</b></td> <td><b>Unique</b></td>  <td><b>Default</b></td> </tr>\n")
                for col in columnas:
                    f.write("               <tr><td>")
                    f.write(col.nombre)
                    f.write("</td><td>")
                    f.write(col.tipo)
                    f.write("</td><td>")
                    f.write(str(col.size))
                    f.write("</td><td>")
                    if col.PK == False:
                        f.write("False")
                    else:
                        f.write("True")
                    f.write("</td><td>")
                    if col.FK == False:
                        f.write("False")
                    else:
                        f.write("True")
                    f.write("</td><td>")
                    if col.unique == False:
                        f.write("False")
                    else:
                        f.write("True")
                    f.write("</td><td>")
                    f.write(col.default)
                f.write("</td></tr>\n")
                f.write("               </table>\n")
                for column in datos.tablaSimbolos[a]['tablas'][table]['index']:
                    f.write("<p class='i'>Indice :")
                    f.write(column.name)
                    f.write("</p>\n")
                    f.write("<li>")
                    f.write("<ol>Nombre: ")
                    f.write(column.name)
                    f.write("</ol></li><li>Columnas: ")
                    for h in column.columns:
                        f.write("<ul>")
                        f.write("Tabla ->")
                        if h.table != None:
                            f.write(h.table)
                        else:
                            f.write("None")
                        f.write("Columna ->")
                        f.write(h.column)
                        f.write("</ul>\n")
                    f.write("</li><li>Condiciones: ")
                    if column.conditions != None:
                        for h in column.conditions:
                            f.write("<ul>")
                            f.write(h)
                            f.write("</ul>")
                    else:
                        f.write("<ul>SIN CONDICIONES</ul>\n</li>")
                f.write("           </div>\n")
                f.write("         </div>\n")
    f.write("   </body>\n")
    f.write("</html>\n")
    f.close()

def escribirEnSalidaInicio(texto): #borra lo que hay y escribe al inicio
    salida.insert("1.0", texto)

def escribirEnSalidaFinal(texto): # no borra y escribe al final de lo que ya estaACTIVE
    text = texto + "\n"
    salida.insert("end", text)
#root
################################Configuracion#################################
root = Tk()
root.title("TytusDB_Manager")#titulo
root.resizable(0,0)
root.geometry("1300x700")#ajustar tamaño
root.config(bg="black", cursor="pirate")
###############################Barra menú#####################################
barra = Menu(root)
root.config(menu=barra, width=300, height=300)

archivoMenu = Menu(barra, tearoff=0)
archivoMenu.add_command(label="Abrir", command=openFile)
archivoMenu.add_command(label="Guardar", command=guardar)
barra.add_cascade(label="Archivo", menu=archivoMenu)

herramientaMenu=Menu(barra, tearoff=0)
herramientaMenu.add_command(label="Ejecutar Analisis", command=analisis)
barra.add_cascade(label="Analisis", menu=herramientaMenu)

reporteMenu = Menu(barra, tearoff=0)
reporteMenu.add_command(label="Reporte errores", command=mistakes)
reporteMenu.add_command(label="Tabla de simbolos", command=tabla)
reporteMenu.add_command(label="Reporte AST", command=ast)
reporteMenu.add_command(label="Reporte Gramatical", command=gramatica)
barra.add_cascade(label="Reportes", menu=reporteMenu)

ayudaMenu=Menu(barra, tearoff=0)
ayudaMenu.add_command(label="Ayuda", command=ayuda)
barra.add_cascade(label="Ayuda", menu=ayudaMenu)
##################################EDITOR DE CODIGO#############################
nombreL=Label( root, text="EDITOR", fg="BLUE", font=("Arial", 12))
nombreL.place(x=300, y=10)
editor = Text(root, width=122, height=18, bg="white")
editor.place(x=300, y=45)

nombreL=Label( root, text="SALIDA", fg="BLUE", font=("Arial", 12))
nombreL.place(x=300, y=350)
salida = Text(root, width=122, height=18, bg="skyblue")
salida.place(x=300, y=380)


root.mainloop() #mostrar interfaz
