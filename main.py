from tkinter import *
from tkinter import filedialog

from read_audit import write_audit
import ast
import os

SystemDict = {}


class App(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Security Benchmarking Tool 2.0")
        self.pack(fill=BOTH, expand=1)
        # self.master.tk_setPalette(background='#ececec')

        self.search_var = StringVar()
        self.search_var.trace('w', self.highlight_searched)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = Menu(menu)
        fileMenu.add_command(label="Open", command=self.openAndWriteOutput)
        fileMenu.add_command(label="Open Audit from Home", command=self.openCustom)
        fileMenu.add_command(label="Compare", command=self.check)
        fileMenu.add_command(label="Exit", command=self.exitProgram)
        menu.add_cascade(label="File", menu=fileMenu)

        editMenu = Menu(menu)
        editMenu.add_command(label="Save File As", command=self.saveFile)
        editMenu.add_command(label="Save Custom Audit", command=self.saveCustom)
        editMenu.add_command(label="Select All", command=self.selectAll)
        editMenu.add_command(label="Deselect All", command=self.deselectAll)
        menu.add_cascade(label="Actions", menu=editMenu)

        inputBar = Entry(self, textvariable=self.search_var)
        inputBar.pack(fill=BOTH, expand=1)

        self.output = Listbox(selectmode='multiple')
        self.output.pack(fill=BOTH, expand=1)

        self.initialContent = ''
        self.initialList = list()
        self.highlight_searched()

        # self.output = Text()
        # self.output.pack(fill=BOTH, expand=1)

    def check(self):
        path = os.getcwd()
        print(path)
        os.system('Secedit.exe /export /cfg ' + path + '\\security.txt')
        file = open('security.txt', 'r')
        input = file.read()
        san = ""
        for i in input:
            if i.isprintable() or i.isspace():
                san += i
        san = san.split('\n')
        san = [x for x in san if len(x) > 0]

        # print(san)
        for str in san:
            if '=' in str:
                to_add = str[str.index('=') + 1:]
                key_to_add = str[:str.index('=')]
                result_value = ''
                result_key = ''
                for char in to_add:
                    if char != ' ':
                        result_value += char
                for char in key_to_add:
                    if char != ' ':
                        result_key += char
                SystemDict[result_key] = result_value
        print(SystemDict)

    @staticmethod
    def exitProgram():
        exit()

    def highlight_searched(self, *args):
        search = self.search_var.get()
        self.output.delete(0, END)
        for item in self.initialList:
            if search.lower() in item.lower():
                self.output.insert(END, item)

    def saveCustom(self):
        if not self.initialContent:
            return

        file = filedialog.asksaveasfile(mode="w", filetypes=(("Audit files", "*.audit"), ("All files", "*.*")))

        if not file:
            return

        values = [self.output.get(idx) for idx in self.output.curselection()]

        f = open(file.name, "w")
        f.write(str(values))
        f.close()

    def selectAll(self):
        self.output.select_set(0, END)

    def deselectAll(self):
        self.output.selection_clear(0, END)

    def saveFile(self):

        if not self.initialContent:
            return

        file = filedialog.asksaveasfile(mode="w", filetypes=(("Audit files", "*.audit"), ("All files", "*.*")))

        if not file:
            return

        f = open(file.name, "w")
        f.write(self.initialContent)
        f.close()

    def openCustom(self):
        file = filedialog.askopenfile(mode="r", filetypes=(("Audit files", "*.audit"), ("All files", "*.*")))

        if not file:
            return

        f = open(file.name, "r")
        self.initialContent = f.read()

        structure = ast.literal_eval(self.initialContent)
        self.output.delete(0, END)

        for element in structure:
            self.output.insert(END, element)

        self.initialList = structure

    def openAndWriteOutput(self):
        file = filedialog.askopenfile(mode="r", filetypes=(("Audit files", "*.audit"), ("All files", "*.*")))

        if not file:
            return

        f = open(file.name, "r")
        self.initialContent = f.read()

        structure = write_audit(self.initialContent)

        form = '{}'

        self.output.delete(0, END)
        customItemFlag = False
        for (_, _, text) in structure:
            if (text == "<custom_item>"):
                customItemFlag = True
                continue

            if (customItemFlag == True):
                self.output.insert(END, form.format(text))
                customItemFlag = False

        self.initialList = self.output.get(0, END)


if __name__ == '__main__':
    root = Tk()
    app = App(root)
    # root.wm_title("Security Benchmarking Tool")
    root.geometry("600x500")
    root.mainloop()
