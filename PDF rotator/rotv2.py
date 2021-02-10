import PyPDF2, os, tkinter
from tkinter import filedialog, messagebox

class MainWindow:
    def __init__(self):
        self.filepath = ""
        self.degree = 90
        self.root_window = tkinter.Tk()
        self.empty_label = tkinter.Label(self.root_window, text=' ')
        self.empty_label2 = tkinter.Label(self.root_window, text=' ')
        self.empty_label3 = tkinter.Label(self.root_window, text=' ')

        self.lbl = tkinter.Label(self.root_window, text='1. Choose a file', fg="blue", font=("Arial", 17), justify='left')
        self.textlabel = tkinter.Entry(self.root_window)
        self.button_of_choice = tkinter.Button(self.root_window, text="Open...", command=self.read_file)

        self.label = tkinter.Label(self.root_window, text='2. Choose the direction', fg="blue", font=("Arial", 17), justify='left')
        self.frame = tkinter.Frame(self.root_window)
        self.rot90 = tkinter.Button(self.frame, text="↻", command=lambda: self.change_degree(90))
        self.rot180 = tkinter.Button(self.frame, text="↕", command=lambda: self.change_degree(180))
        self.rot270 = tkinter.Button(self.frame, text="↺", command=lambda: self.change_degree(270))

        self.final_button = tkinter.Button(self.root_window, text="Rotate", state=tkinter.DISABLED, command=self.rotate)

        self.empty_label.grid(row=0, column=0)
        self.lbl.grid(row=1, column=0)
        self.textlabel.grid(row=2, column=0)
        self.button_of_choice.grid(row=2, column=1)
        self.empty_label2.grid(row=3, column=0)
        self.label.grid(row=4, column=0)

        self.frame.grid(row=5, column=0)
        self.rot90.pack(side="right")
        self.rot180.pack(side="right")
        self.rot270.pack(side="right")

        self.empty_label3.grid(row=6, column=0)
        self.final_button.grid(row=7, column=1)


    def read_file(self):
        self.filepath = filedialog.askopenfilename(filetypes=(("PDF files", "*.pdf"), ("All types", "*.*")))
        if self.filepath != None and self.filepath != '' and self.filepath != ():
            if self.is_PDF(self.filepath) == False:
                messagebox.showerror("Error", "File doesn't contain the '.pdf' extension!")
            else:
                self.textlabel.delete(0, tkinter.END)
                self.textlabel.insert(0, self.filepath)
                self.final_button["state"] = tkinter.NORMAL

    def is_PDF(self, filename):
        if filename.count('.pdf') == 0:
            return False
        return True

    def change_degree(self, number):
        self.degree = number

    def rotate(self):
        pdf_in = open(self.filepath, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_in)
        pdf_writer = PyPDF2.PdfFileWriter()

        temp_file = open("temp0.pdf", 'wb')
        self.write_to_file(pdf_writer, pdf_reader, 0)
        pdf_writer.write(temp_file)
        pdf_in.close()
        temp_file.close()
        os.remove(self.filepath)
        pdf_in = open("temp0.pdf", 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_in)
        pdf_writer = PyPDF2.PdfFileWriter()

        self.write_to_file(pdf_writer, pdf_reader, self.degree)
        pdf_out = open(self.filepath, 'wb')
        pdf_writer.write(pdf_out)
        pdf_out.close()
        pdf_in.close()
        os.remove("temp0.pdf")

        messagebox.showinfo("Success", "Operation successfully satisfied!")

    def write_to_file(self, pdf_writer, pdf_reader, degree):
        for pagenum in range(pdf_reader.numPages):
            page = pdf_reader.getPage(pagenum)
            page.rotateClockwise(degree)
            pdf_writer.addPage(page)



def Main():
    window = MainWindow()
    window.root_window.title("Rotate a PDF file")
    window.root_window.geometry("380x220")
    window.root_window.resizable(False, False)
    window.root_window.mainloop()

if __name__ == '__main__':
    Main()
