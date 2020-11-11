from _utils import *
preprocessor()

from tk_interface import *
old_stdout = sys.stdout


root = tk.Tk()
app = Application(master=root)
app.mainloop()

sys.stdout = old_stdout
