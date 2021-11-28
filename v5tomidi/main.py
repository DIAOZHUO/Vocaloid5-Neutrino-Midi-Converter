from convert import convert
import tkinter, tkinter.filedialog, tkinter.messagebox



__root = tkinter.Tk()
__root.title("Vocaloid5-Neutrino midi Converter")
__root.geometry("400x100")


def __browse_button1():
    try:
        filename = tkinter.filedialog.askopenfile(filetypes=[("vpr","*.vpr")]).name
        __file_path.set(filename)
    except:
        pass


def __convert_button2():
    res, mes = convert(__file_path.get(), __export_lyrics.get())
    if res:
        tkinter.messagebox.showinfo(message="Done!\n"+"file saved at "+mes)
    else:
        tkinter.messagebox.showerror(message="Error\n"+mes)




__file_path = tkinter.StringVar()
__export_lyrics = tkinter.BooleanVar()
tkinter.Label(text="Please select the .vpr project file").grid(row=1, column=1)
tkinter.Label(master=__root, textvariable=__file_path).grid(row=2, column=1)
__button1 = tkinter.Button(text="Browse", command=__browse_button1)
__button1.grid(row=2, column=0)
__check_box = tkinter.Checkbutton(__root, text='export lyrics', variable=__export_lyrics)
__check_box.grid(row=3, column=0)
__button2 = tkinter.Button(text="Convert", command=__convert_button2)
__button2.grid(row=3, column=1)


__root.mainloop()



