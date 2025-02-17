from  tkinter import *

from gui import FinanceTrackerGUI

def main():
    root=Tk()
    finance=FinanceTrackerGUI(root)
    root.mainloop()
    
if __name__== '__main__':
    main()