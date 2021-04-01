import tkinter as tk
from window import Window

def Main():
    width = 600
    height = 400

    rootWindow = tk.Tk()
    win = Window(rootWindow, width, height, mat_plot_lib=True)
    # Window's origin positions
    x = int(rootWindow.winfo_screenwidth() / 2 - width)
    y = int(rootWindow.winfo_screenheight() / 2 - height)
    rootWindow.geometry("+{}+{}".format(x, y))
    rootWindow.resizable(False, False)
    rootWindow.title("Compare images")
    rootWindow.mainloop()
    # Delete contents of windows after it's being closed
    del(win)

if __name__ == '__main__':
    Main()
