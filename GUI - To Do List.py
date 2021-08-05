import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from time import strftime

todos = {}


def DetailTodo(cb=None):
    win = tk.Toplevel()
    win.wm_title("Detail todo")
    selectedItem = treev.focus()
    selectedIndex = treev.item(selectedItem)["text"]
    selectedTodo = todos[tanggal][selectedIndex]
    judul = tk.StringVar(value=selectedTodo["judul"])
    tk.Label(win,text="tanggal").grid(row=0, column = 0, sticky = "N")
    tk.Label(win, text="{} | {} ".format(tanggal, selectedTodo["waktu"])).grid(row = 0, column = 1, sticky = "N")
    tk.Label(win, text="Judul: ").grid(row = 1, column = 0, sticky ="N" )
    tk.Entry(win, stat="disabled", textvariable= judul).grid(row = 1, column = 1, sticky = "E")
    tk.Label(win, text="Keterangan").grid(row = 2, column = 0, sticky = "E")
    keterangan = ScrolledText(win, width = 12, height = 5)
    keterangan.grid(row = 2, column = 1, sticky = "E")
    keterangan.insert(tk.INSERT, selectedTodo["keterangan"])
    keterangan.configure(state="disabled")


def SaveTodo():
    f = open("mytodo.dat", "w")
    f.write(str(todos))
    f.close()

def LoadTodo():
    global todos
    f = open("mytodo.dat", "r")
    data = f.read()
    f.close
    todos = eval(data)
    ListTodo()

def DelTodo():
    tanggal = str(cal.selection_get())
    selectedItem = treev.focus()
    todos[tanggal].pop(treev.item(selectedItem)["text"])
    ListTodo()

def ListTodo(cb=0):
    for i in treev.get_children():
        treev.delete(i)
    tanggal = str(cal.selection_get())
    if tanggal in todos:
        for i in range(len(todos[tanggal])):
            treev.insert("","end", text=i, values=(todos[tanggal][i]["waktu"], todos[tanggal][i]["judul"]))

def AddTodo(win, key, jam, menit, judul, keterangan):
    newTodo = {
        "waktu":"{}:{}".format(jam.get(), menit.get()),
        "judul": judul.get(),
        "keterangan":keterangan.get("1.0", tk.END)
    }
    if key in todos:
        todos[key].append(newTodo)
    else:
        todos[key] = [newTodo]
    win.destroy()
    ListTodo()

def AddForm():
    win = tk.Toplevel()
    win.wm_title("Add +")
    jam = tk.IntVar(value=10)
    menit = tk.IntVar(value=30)
    judul = tk.StringVar(value="")
    tk.Label(win, text="Time: ", font = "fixedsys").grid(row=0, column = 0)
    tk.Spinbox(win,from_= 0,to= 23, textvariable = jam, width = 3).grid(row = 0, column = 1)
    tk.Spinbox(win,from_= 0,to= 59, textvariable = menit, width = 3).grid(row = 0, column = 2)
    tk.Label(win, text="Title: ", font = "fixedsys").grid(row = 1, column = 0)
    tk.Entry(win, textvariable=judul ).grid(row = 1, column = 1, columnspan = 2)
    tk.Label(win, text="Caption", font = "fixedsys").grid(row =2, column = 0)
    keterangan = ScrolledText(win,width = 12, height = 5)
    keterangan.grid(row =2, column =1, columnspan = 2, rowspan = 4 )
    
    tk.Button(win, text="Add", command= lambda : AddTodo(win, tanggal, jam, menit, judul, keterangan)).grid(row=6, column = 0)

    tanggal = str(cal.selection_get())

def title():
    waktu = strftime('%H:%M')
    tanggal = str(cal.selection_get())
    root.title(tanggal + " | " + waktu + " | My Calendar")
    root.after(1000, title)

root = tk.Tk()
s = ttk.Style()
s.configure("Treeview", rowheight = 16)
root.title("My Calender")

#Calendar Settings
cal = Calendar(root, font = "fixedsys 14", 
selectmode = "day", 
locale = "en_US", 
cursor = "sizing", 
background="white", 
disabledbackground="white", 
bordercolor="pink", 
headersbackground="bisque2", 
normalbackground="black", 
foreground="bisque4",
normalforeground="bisque4", 
headersforeground="bisque4")

cal.config(background = "black")
cal.grid(row = 0, column = 0, sticky = "N", rowspan = 9)
cal.bind("<<CalendarSelected>>", ListTodo)

#Variable Global
tanggal = str(cal.selection_get())

#Style
style = ttk.Style()
style.configure("Treeview", background="bisque4", foreground = "bisque4")

treev = ttk.Treeview(root)
treev.grid(row = 0, column = 1, sticky = "WNE", rowspan = 4, columnspan = 2)

#Scrollbar Settings
scrollBar = tk.Scrollbar(root, orient = "vertical", command = treev.yview)
scrollBar.grid(row = 0, column = 3, sticky = "ENS", rowspan = 4)
treev.configure(yscrollcommand = scrollBar.set)
treev.bind("<Double-1>", DetailTodo)


#Time and Title Setting
treev["columns"] = ("1", "2")
treev["show"] = "headings"
treev.column("1", width = 100)
treev.heading("1", text = "Time")
treev.heading("2", text = "Title")

style = ttk.Style()
style.configure("Treeview.Heading", foreground='bisque4', font = ("fixedsys 8"), fieldbackground = "black")
style.configure("Treeview",
background = "bisque3", foreground = "black", fieldbackground = "bisque4")
style.map("Treeview", background = [("selected", "bisque4")])


#Button Settings
btnAdd = tk.Button(root, text = "Add", width = 20, font = "fixedsys", cursor = "plus", bg = "green", command= AddForm)
btnAdd.grid(row = 4, column = 2, sticky = "N")

btnDel = tk.Button(root, text = "Delete", width = "20", font = "fixedsys", cursor = "hand2", bg = "red", command= DelTodo)
btnDel.grid(row = 4, column = 1, sticky = "N")

btnLoad = tk.Button(root, text = "Load", width = 20, font = "fixedsys", cursor = "exchange", bg = "bisque4", command= LoadTodo )
btnLoad.grid(row = 6, column = 1, sticky = "S")

btnSave = tk.Button(root, text = "Save", width = 20, font = "fixedsys", cursor = "hand2", bg = "blue", command= SaveTodo)
btnSave.grid(row = 6, column = 2, sticky = "S")

title()
root.mainloop()