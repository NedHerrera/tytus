from storage.avl import avlMode as avl
from storage.b import BMode as b
from storage.bplus import BPlusMode as bplus
from storage.hash import HashMode as hash
from storage.isam import ISAMMode as isam
from storage.json import jsonMode as json
from storage.dict import DictMode as dict
import pickle
import os
import zlib
from cryptography.fernet import Fernet
import base64

modos = ["avl", "b", "bplus", "hash", "isam", "json", "dict"]
encoding = ["ascii", "utf8", "iso-8859-1"]

def commit(objeto, nombre):
    file = open(nombre + ".bin", "wb+")
    file.write(pickle.dumps(objeto))
    file.close()

def rollback(nombre):
    file = open(nombre + ".bin", "rb")
    b = file.read()
    file.close()
    return pickle.loads(b)

def __init__():
    global lista_db
    lista_db = []
    lista_db = rollback("prueba")
__init__()



def buscar(nombre):
    for db in lista_db:
        if nombre == db[0]:
            return db
    else:
        return None

def verificarmodo(mode):
    if mode == 'avl':
        return avl
    elif mode == 'b':
        return b
    elif mode == 'bplus':
        return bplus
    elif mode == 'dict':
        return dict
    elif mode == 'isam':
        return isam
    elif mode == 'json':
        return json
    elif mode == 'hash':
        return hash

def createDatabase(db,modo,cod):
    if not modo in modos:
        return 3
    if not cod in encoding:
        return 4
    if buscar(db) == None:
        tmp = verificarmodo(modo).createDatabase(db)
        if tmp == 0:
            lista_db.append([db, modo, cod,{},[],[]])
            return 0
        else:
            return 1
    else:
        return 2

def cambiardatos(db, modo,modonuevo):
    nodo = buscar(db)
    verificarmodo(modonuevo).createDatabase(db)
    tablas=verificarmodo(modo).showTables(db)
    listapk = nodo[4]
    if len(tablas)>0:
        for tabla in tablas:
            registros = verificarmodo(modo).extractTable(db,tabla)
            verificarmodo(modonuevo).createTable(db,tabla,len(registros[0]))
            for pk in listapk:
                if db in pk and tabla in pk:
                    verificarmodo(modonuevo).alterAddPK(db, tabla, pk[2])
            if len(registros)>0:
                for registro in registros:
                    verificarmodo(modonuevo).insert(db,tabla,registro)

def alterDatabaseMode(db, modo):
    nodo = buscar(db)
    if nodo != None:
        if modo in modos:
            try:
                cambiardatos(db,nodo[1],modo)
                verificarmodo(nodo[1]).dropDatabase(db)
                nodo[1] = modo
                dict = nodo[3]
                for i in dict:
                    tablas = verificarmodo(dict[i]).extractTable(db,i)
                    verificarmodo(nodo[1]).createTable(db,i,len(tablas[0]))
                    for registro in tablas:
                        verificarmodo(nodo[1]).insert(db,i,registro)

                for i in dict:
                    if dict[i] != modo:
                        verificarmodo(dict[i]).dropDatabase(db)

                nodo[3]={}
                return 0
            except:
                return 1
        else:
            return 4
    else:
        return 2

def alterDatabaseEncoding(db,cod):
    nodo = buscar(db)
    if nodo != None:
        if cod in encoding:
            try:
                nodo[2]=cod
                return 0
            except:
                return 1
        else:
            return 3
    else:
        return 2

def alterTableMode(db,tabla, modo):
    nodo = buscar(db)
    if nodo != None:
        if modo in modos:
            try:
                dic = nodo[3]
                dic[tabla]=modo
                verificarmodo(modo).createDatabase(db)
                tablas = verificarmodo(nodo[1]).extractTable(db,tabla)
                verificarmodo(modo).createTable(db, tabla,len(tablas[0]))
                for registro in tablas:
                    verificarmodo(modo).insert(db,tabla,registro)
                verificarmodo(nodo[1]).dropTable(db,tabla)
                return 0
            except:
                return 1
        else:
            return 4
    else:
        return 2

def showDatabases():
    lista= []
    for db in lista_db:
        lista.append(db[0])

    return lista

def dropDatabase(db):
    nodo = buscar(db)
    if nodo != None:
        num = 0
        for i in lista_db:
            try:
                if i[0]==db:
                    verificarmodo(nodo[1]).dropDatabase(db)
                    lista_db.pop(num)
                return 0
            except:
                return 1
            num = num + 1
    else:
        return 2

def alterDatabase(db,nuevadb):
    nodo = buscar(db)
    nodonuevo = buscar(nuevadb)
    if nodonuevo is None:
        if nodo != None:
            try:
                res = verificarmodo(nodo[1]).alterDatabase(db,nuevadb)
                nodo[0]=nuevadb
                return res
            except:
                return 1
        else:
            return 2
    else:
        return 3

def createTable(db,tabla,columnas):
    nodo = buscar(db)
    if nodo != None:
        try:
            res = verificarmodo(nodo[1]).createTable(db,tabla,columnas)
            return res
        except:
            return 1
    else:
        return 2

def showTables(db):
    nodo = buscar(db)
    if nodo != None:
        try:
            lista = verificarmodo(nodo[1]).showTables(db)
            dict = nodo[3]
            for tabla in dict:
                lista.append(tabla)
            return lista
        except:
            return []
    else:
        return []

def extractTable(db,tabla):
    nodo = buscar(db)
    if nodo != None:
        try:
            dict = nodo[3]
            if tabla in dict:
                lista = verificarmodo(dict[tabla]).extractTable(db,tabla)
                return lista
            else:
                lista = verificarmodo(nodo[1]).extractTable(db,tabla)
                return lista
        except:
            return []
    else:
        return []

def extractRangeTable(db,tabla,columna,menor,mayor):
    nodo = buscar(db)
    if nodo != None:
        try:
            dict = nodo[3]
            if tabla in dict:
                lista = verificarmodo(dict[tabla]).extractRangeTable(db,tabla,columna,menor,mayor)
                return lista
            else:
                lista = verificarmodo(nodo[1]).extractRangeTable(db,tabla,columna,menor,mayor)
                return lista
        except:
            return []
    else:
        return []

def alterAddPK(db,tabla,columnas):
    nodo = buscar(db)
    if nodo != None:
        try:
            dict = nodo[3]
            if tabla in dict:
                res = verificarmodo(dict[tabla]).alterAddPK(db, tabla, columnas)
                if res == 0:
                    lista = nodo[4]
                    lista.append([tabla, columnas])
                return res
            else:
                res = verificarmodo(nodo[1]).alterAddPK(db, tabla, columnas)
                if res == 0:
                    lista = nodo[4]
                    lista.append([tabla, columnas])
                return res
        except:
            return 1
    else:
        return 2

def alterDropPK(db,tabla):
    nodo = buscar(db)
    if nodo != None:
        try:
            dict = nodo[3]
            if tabla in dict:
                res = verificarmodo(dict[tabla]).alterDropPK(db, tabla)
                if res == 0:
                    c = 0
                    listapk = nodo[4]
                    for pk in listapk:
                        if tabla in pk:
                            listapk.pop(c)
                    c = c + 1
                return res
            else:
                res = verificarmodo(nodo[1]).alterDropPK(db, tabla)
                if res == 0:
                    c = 0
                    listapk = nodo[4]
                    for pk in listapk:
                        if tabla in pk:
                            listapk.pop(c)
                    c = c + 1
                return res
        except:
            return 1
    else:
        return 2

def alterTable(db,tabla,tablanueva):
    nodo = buscar(db)
    if nodo != None:
        try:
            dict = nodo[3]
            if tabla in dict:
                res = verificarmodo(dict[tabla]).alterTable(db, tabla,tablanueva)
                tabla = tablanueva
                return res
            else:
                res = verificarmodo(nodo[1]).alterTable(db, tabla, tablanueva)
                return res
        except:
            return 1
    else:
        return 2

def alterAddColumn(db,tabla,valor):
    nodo = buscar(db)
    if nodo != None:
        try:
            dict = nodo[3]
            if tabla in dict:
                res = verificarmodo(dict[tabla]).alterAddColumn(db, tabla,valor)
                return res
            else:
                res = verificarmodo(nodo[1]).alterAddColumn(db, tabla, valor)
                return res
        except:
            return 1
    else:
        return 2

def alterDropColumn(db,tabla,valor):
    nodo = buscar(db)
    if nodo != None:
        try:
            dict = nodo[3]
            if tabla in dict:
                res = verificarmodo(dict[tabla]).alterDropColumn(db, tabla,valor)
                return res
            else:
                res = verificarmodo(nodo[1]).alterDropColumn(db, tabla, valor)
                return res
        except:
            return 1
    else:
        return 2

def dropTable(db,tabla):
    nodo = buscar(db)
    if nodo != None:
        try:
            dict = nodo[3]
            if tabla in dict:
                res = verificarmodo(dict[tabla]).dropTable(db,tabla)
                del dict[tabla]
                return res
            else:
                res = verificarmodo([nodo[1]]).dropTable(db,tabla)
                return res
        except:
            return 1
    else:
        return 2

def loadCSV(file,db,tabla):
    nodo = buscar(db)
    if nodo != None:
        dict = nodo[3]
        if tabla in dict:
            res = verificarmodo(dict[tabla]).loadCSV(file,db,tabla)
            return res
        else:
            res = verificarmodo(nodo[1]).loadCSV(file,db,tabla)
            return res
    else:
        return 2

def extractRow(db,tabla,lista):
    nodo = buscar(db)
    if nodo != None:
        dict = nodo[3]
        if tabla in dict:
            res = verificarmodo(dict[tabla]).extractRow(db,tabla,lista)
            return res
        else:
            res = verificarmodo(nodo[1]).extractRow(db,tabla,lista)
            return res
    else:
        return []

def update(db,tabla,dict,lista):
    nodo = buscar(db)
    if nodo != None:
        dict = nodo[3]
        if tabla in dict:
            res = verificarmodo(dict[tabla]).update(db,tabla,dict,lista)
            return res
        else:
            res = verificarmodo(nodo[1]).update(db,tabla,dict,lista)
            return res
    else:
        return 2

def delete(db,tabla,lista):
    nodo = buscar(db)
    if nodo != None:
        dict = nodo[3]
        if tabla in dict:
            res = verificarmodo(dict[tabla]).delete(db,tabla,lista)
            return res
        else:
            res = verificarmodo(nodo[1]).delete(db,tabla,lista)
            return res
    else:
        return 2

def truncate(db,tabla,lista):
    nodo = buscar(db)
    if nodo != None:
        dict = nodo[3]
        if tabla in dict:
            res = verificarmodo(dict[tabla]).truncate(db,tabla)
            return res
        else:
            res = verificarmodo(nodo[1]).truncate(db,tabla)
            return res
    else:
        return 2

def insert(db,tabla,lista):
    nodo = buscar(db)
    if nodo != None:
        dict = nodo[3]
        if tabla in dict:
            res = verificarmodo(dict[tabla]).insert(db,tabla,lista)
            return res
        else:
            res = verificarmodo(nodo[1]).insert(db,tabla,lista)
            return res
    else:
        return 2
def encrypt(backup,clave):
    f = Fernet(clave)
    textoencriptado = f.encrypt(backup.encode("utf-8"))
    return textoencriptado

def decrypt(cipherbackup,clave):
    print(clave.encode())
    pss = base64.encodebytes(clave.encode())
    f = Fernet(pss)
    textodesencriptado = f.decrypt(cipherbackup)
    return textodesencriptado.decode()