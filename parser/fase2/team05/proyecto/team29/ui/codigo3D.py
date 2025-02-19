from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))
from team29.ui.Pantalla_TS import *
from team29.ui.Pantalla_AST import *
from team29.ui.Pantalla_Error import *
import tkinter.messagebox
from team29.analizer import interpreter
from goto import with_goto

# VARIABLES GLOBALES
window = Tk()
tabControl = ttk.Notebook(window, width=700, height=300)
text_Consola = None
lexicalErrors = list()
syntacticErrors = list()
semanticErrors = list()
postgreSQL = list()
ts = list()
lista = []
simulador_pila = [None]*100

def main():
    global window, tabControl, text_Consola, lexicalErrors, syntacticErrors, semanticErrors, postgreSQL, ts
    # inicializacion de la pantalla
    window.geometry("700x320")
    window.resizable(0, 0)
    window.title("Query Tool")

    # Definicion del menu de items
    navMenu = Menu(window)
    navMenu.add_command(label="Tabla de Simbolos", command=open_ST)
    navMenu.add_command(label="AST", command=open_AST)
    navMenu.add_command(label="Reporte de errores", command=open_Reporte)
    window.config(menu=navMenu)

    # Creacion del notebook
    tabControl = ttk.Notebook(window, width=700, height=300)
    console_frame = Frame(tabControl, height=20, width=150, bg="#d3d3d3")
    text_Consola = tk.Text(console_frame, height=20, width=150)
    text_Consola.pack(fill=BOTH)
    console_frame.pack(fill=BOTH)
    tabControl.add(console_frame, text="Consola")
    tabControl.pack()
    main3d()
    window.mainloop()


def open_ST():
    global window, ts
    windowTableS = Pantalla_TS(window, ts)


def open_AST():
    global window
    windowTableS = Pantalla_AST(window)


def open_Reporte():
    global window, lexicalErrors, syntacticErrors, semanticErrors
    windowTableS = Pantalla_Error(
        window, lexicalErrors, syntacticErrors, semanticErrors
    )


def fill_table(columns, rows, table):  # funcion que muestra la salida de la/s consulta/s
    table["columns"] = columns
    """
    Definicion de columnas y encabezado
    """
    table.column("#0", width=25, minwidth=50)
    i = 0
    ancho = int(600 / len(columns))
    if ancho < 100:
        ancho = 100
    while i < len(columns):
        table.column(str(i), width=ancho, minwidth=50, anchor=CENTER)
        i += 1
    table.heading("#0", text="#", anchor=CENTER)
    i = 0
    while i < len(columns):
        table.heading(str(i), text=str(columns[i]), anchor=CENTER)
        i += 1
    """
    Insercion de filas
    """
    i = 0
    for row in rows:
        i += 1
        table.insert(parent="", index="end", iid=i, text=i, values=(row))


def show_result(consults):
    global tabControl, text_Consola
    if consults is not None:
        i = 0
        for consult in consults:
            i += 1
            if consult is not None:
                frame = Frame(tabControl, height=300, width=450, bg="#d3d3d3")
                # Creacion del scrollbar
                table_scroll = Scrollbar(frame, orient="vertical")
                table_scrollX = Scrollbar(frame, orient="horizontal")
                table = ttk.Treeview(
                    frame,
                    yscrollcommand=table_scroll.set,
                    xscrollcommand=table_scrollX.set,
                    height=12,
                )
                table_scroll.config(command=table.yview)
                table_scrollX.config(command=table.xview)
                fill_table(consult[0], consult[1], table)
                table_scroll.pack(side=RIGHT, fill=Y)
                table_scrollX.pack(side=BOTTOM, fill=X)
                table.pack(side=LEFT, fill=BOTH)
                frame.pack(fill=BOTH)
                tabControl.add(frame, text="Consulta " + str(i))
            else:
                text_Consola.insert(
                    INSERT, "Error: Consulta sin resultado" + "\n"
                )
    tabControl.pack()


def refresh():
    global tabControl, text_Consola, lexicalErrors, syntacticErrors, semanticErrors, postgreSQL, ts
    tabls = tabControl.tabs()
    i = 1
    while i < len(tabls):
        tabControl.forget(tabls[i])
        i += 1
    text_Consola.delete("1.0", "end")
    semanticErrors.clear()
    syntacticErrors.clear()
    lexicalErrors.clear()
    postgreSQL.clear()
    ts.clear()


def analize(entrada):
    global tabControl, text_Consola, lexicalErrors, syntacticErrors, semanticErrors, postgreSQL, ts
    entrada = str(entrada)
    result = interpreter.execution(entrada)
    lexicalErrors = result["lexical"]
    syntacticErrors = result["syntax"]
    semanticErrors = result["semantic"]
    postgreSQL = result["postgres"]
    ts = result["symbols"]
    if (
            len(lexicalErrors)
            + len(syntacticErrors)
            + len(semanticErrors)
            + len(postgreSQL)
            > 0
    ):
        tkinter.messagebox.showerror(
            title="Error", message="La consulta contiene errores"
        )
        if len(postgreSQL) > 0:
            i = 0
            text_Consola.insert(INSERT, "-----------ERRORS----------" + "\n")
            while i < len(postgreSQL):
                text_Consola.insert(INSERT, postgreSQL[i] + "\n")
                i += 1
    querys = result["querys"]
    show_result(querys)
    messages = result["messages"]
    if len(messages) > 0:
        i = 0
        text_Consola.insert(INSERT, "-----------MESSAGES----------" + "\n")
        while i < len(messages):
            text_Consola.insert(INSERT, str(messages[i]) + "\n")
            i += 1
    text_Consola.insert(INSERT, "\n")
    tabControl.pack()


def funcionIntermedia(): 
	global lista
	entrada = lista.pop()
	analize(entrada)


@with_goto
def main3d(): 
	global lista


def C3D_ValidaRegistros():
    if 5 == 5: goto.L0
    goto.L1
    label.L0
    T5 = True
    goto.L2
    label.L1
    T5 = False
    label.L2


if __name__ == "__main__": 
	 main()
