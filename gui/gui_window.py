import re
import tkinter
from tkinter import filedialog
import threading

from src.CNF import ClauseSet, Clause


class gui_window:
    def __init__(self, name):
        self.mainframe = tkinter.Tk()
        self.mainframe.title(name)
        self.mainframe.geometry("200x200")
        self.clauseframe = clauses_frame(self)
        self.menubar = tkinter.Menu(self.mainframe)
        self.menus = list()
        file_menu = tkinter.Menu(self.menubar, title="File")
        file_menu.add_command(label="New", command=self.new)
        file_menu.add_command(label="Open", command=self.load)
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_separator()
        file_menu.add_command(label="Exit without saving", command=self.mainframe.destroy)
        self.menubar.add_cascade(label="File", menu=file_menu)
        self.mainframe.config(menu=self.menubar)
        self.active = False
        return

    def run(self):
        self.clauseframe.update()
        self.active = True
        self.mainframe.mainloop()
        self.active = False
        return

    def new(self, cs=ClauseSet()):
        return self.clauseframe.new_clauseset(cs, True)

    def load(self):
        filename = filedialog.askopenfilename()
        return self.clauseframe.load_clauseset(filename)

    def save(self):
        filename = filedialog.asksaveasfilename()
        return self.clauseframe.save_clauseset(filename)


class clauses_frame:
    def __init__(self, root: gui_window):
        self.root = root
        self.frame = tkinter.Frame(self.root.mainframe)
        self.frame.pack(fill=tkinter.X)
        self.list = tkinter.Listbox(self.frame, selectmode=tkinter.EXTENDED)
        self.list.pack(fill=tkinter.X)
        self.input = tkinter.Entry(self.frame)
        self.input.pack(fill=tkinter.X)
        self.addbutton = tkinter.Button(self.frame, text="Add", command=lambda: self.input_clauses())
        self.addbutton.pack(fill=tkinter.X)
        self.clauseset = ClauseSet()
        return

    def update(self, force=False):
        if not (self.root.active or force):
            return
        self.list.delete(0, tkinter.END)
        if self.clauseset.isContradictionDetected():
            self.list.insert(tkinter.END, "~")
            return
        for e in self.clauseset.clauses:
            self.list.insert(tkinter.END, e)
        return

    def new_clauseset(self, cs=ClauseSet(), forceUpdate=False):
        self.clauseset = cs
        self.update(forceUpdate)
        return

    def load_clauseset(self, filename, overwrite=True):
        F = open(filename, "r")
        s = F.read()
        F.close()
        L = re.findall(r"[\w|~]+", s)
        if overwrite:
            self.new_clauseset()
        for e in L:
            self.clauseset.add(Clause(e))
        self.update()
        return

    def save_clauseset(self, filename):
        lines: list[str] = [str(e) for e in self.clauseset.clauses]
        lines.sort()
        F = open(filename, "w")
        F.writelines(lines)
        F.close()
        return

    def input_clauses(self):
        raw = self.input.get()
        if len(raw) == 0:
            return
        elif raw == "~":
            raw = ""
        clauses = raw.split(",")
        for e in clauses:
            self.clauseset.add(Clause(e))
        self.update()
        return


def T(gui: gui_window):
    while not gui.active:
        pass
    gui.clauseframe.load_clauseset("testCS_1")
    gui.clauseframe.save_clauseset("testCS_2")
    return


if __name__ == "__main__":
    X = gui_window("name")
    A = threading.Thread(target=T, args=(X,))
    A.start()
    X.new(ClauseSet(["A", "B", "CvD"]))
    X.run()
