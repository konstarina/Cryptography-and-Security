from tkinter import *
from tkinter import filedialog, Button

from read_audit import write_audit


class App(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Security Benchmarking Tool 1.0")
        self.pack(fill=BOTH, expand=3)
        self.master.tk_setPalette(background='#ececec')

        menu = Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = Menu(menu)
        fileMenu.add_command(label="Item")
        fileMenu.add_command(label="Open", command=self.openAndWriteOutput)
        fileMenu.add_command(label="Exit", command=self.exitProgram)
        menu.add_cascade(label="File", menu=fileMenu)

        editMenu = Menu(menu)
        editMenu.add_command(label="Undo")
        editMenu.add_command(label="Redo")
        editMenu.add_command(label="Save", command=self.saveFile)
        menu.add_cascade(label="Actions", menu=editMenu)

        configMenu = Menu(menu)                          
        configMenu.add_command(label="Check")
        configMenu.add_command(label="Modify")
        menu.add_cascade(label="Configure", menu=configMenu)

        #openButton = Button(self, text="Find audit", command=self.openAndWriteOutput)
        #openButton.grid(column=1, row=2)

        #saveButton = Button(self, text="Save audit", command=self.saveFile)
       # saveButton.grid(column=2, row=2)

        self.output = Text()
        self.output.pack(fill=BOTH, expand=1)

        self.initialContent = ''


    def exitProgram(self):
        exit()

    def saveFile(self):

        if not self.initialContent:
            return

        file = filedialog.asksaveasfile(mode="w", filetypes=(("Audit files", "*.audit"), ("All files", "*.*")))

        if not file:
            return

        f = open(file.name, "w")
        f.write(self.initialContent)
        f.close()

    def openAndWriteOutput(self):
        file = filedialog.askopenfile(mode="r", filetypes=(("Audit files", "*.audit"), ("All files", "*.*")))

        if not file:
            return

        f = open(file.name, "r")
        self.initialContent = f.read()

        structure = write_audit(self.initialContent)

        form = '{}'

        self.output.config(state=NORMAL)

        customItemFlag = False
        for (_, _, text) in structure:
            if (text == "<custom_item>"):
                customItemFlag = True
                continue

            if (customItemFlag == True):
                self.output.insert(END, form.format(text))
                self.output.insert(END, '\n')
                customItemFlag = False

        self.output.config(state=DISABLED)


if __name__ == '__main__':
    root = Tk()
    app = App(root)
    # root.wm_title("Security Benchmarking Tool")
    root.geometry("600x500")
    root.mainloop()
