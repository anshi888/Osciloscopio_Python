from tkinter import Tk
from mainFrame import MainFrame
import tkinter
def main():
        root = Tk()
        root.wm_title("Chispitas")
        root.geometry('1200x1000')
        app= MainFrame(root)

        def call_update():
                global update, update_after
                update_test()

        def update_test():
                global update, update_after
                app.animete()
                app.animate_osc()
                update_after = root.after(10, update_test)
                #poned el tiempo que desee
        call_update()
        app.mainloop()

if __name__ == '__main__':
        main()
