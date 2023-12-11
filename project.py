import psycopg2
import tkinter as tk
from tkinter import ttk
import matplotlib
from matplotlib import pyplot as plt
from PIL import ImageTk,Image
from tkcalendar import DateEntry

class FinanceTracker:
    def __init__(self,root):
        #initialize the window
        self.root=root
        self.root.title('Finance Tracker')
        self.root.geometry('800x800')

        #connect to database
        self.database=psycopg2.connect(database='cs50_final_project',user='postgres',password='9860934500',host='localhost')
        self.cursor=self.database.cursor()
        self.cursor.execute('''
          CREATE TABLE IF NOT EXISTS expenses(
            id SERIAL PRIMARY KEY,
            amount REAL,
            category TEXT,
            expense_date DATE
          )
        ''')
        self.database.commit()

        #create a start frame
        self.start_frame=tk.Frame(self.root,bg='teal')
        self.start_frame.pack(fill='both',expand=1)

         # create a welcome label
        self.welcome_label = tk.Label(self.start_frame, text='Welcome', font=("Calibri", 20), bg='teal', fg='Yellow')
        self.welcome_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)  # Position at the center

        # create a new record button
        self.button = tk.Button(self.start_frame, text='New record',  bg='sky blue', fg='black', font=('arial', 14), relief=tk.RAISED,command=self.get_dashboard)
        self.button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Position at the center
        
    
    def get_dashboard(self):
        #Destroy an existing start frame
        self.start_frame.destroy()
        #create a new frame
        self.dashboard_frame=tk.Frame(self.root,bg='teal')
        self.dashboard_frame.pack(fill='both',expand=1)
        #list of categories
        self.categories=['food','shopping','education']
        #label for category
        self.select_category=tk.Label(self.dashboard_frame,text='Select a category',bg='teal',fg='yellow',font=('Arial',12))
        self.select_category.pack(padx=10,pady=10)
        #combobox for category
        self.category=ttk.Combobox(self.dashboard_frame, values=self.categories,font=('Arial',12))
        self.category.current(0)
        self.category.pack(padx=10,pady=10)

        #entry box for amount
        self.amount_label=tk.Label(self.dashboard_frame, text='Amount',bg='teal',fg='yellow',font=('Arial',12))
        self.amount_label.pack(pady=10, padx=10)
        self.amount_entry=tk.Entry(self.dashboard_frame,width=25)
        self.amount_entry.pack(padx=10,pady=10)
        
        self.date_label = tk.Label(self.dashboard_frame, text='Select Date:', font=("Arial", 12), bg='teal', fg='yellow')
        self.date_label.pack(padx=10,pady=10)

        # Create a DateEntry widget
        self.date_entry=DateEntry(self.dashboard_frame,width=25, background='sky blue', foreground='black', borderwidth=2)
        self.date_entry.pack(pady=10,padx=10)
        
        #button to add expense
        self.add_expense_button=tk.Button(self.dashboard_frame,text="Add",bg='sky blue',fg='Yellow',command=self.add_expense)
        self.add_expense_button.place(relx=0.3,rely=0.4, anchor=tk.CENTER)
    
        #button to visualize
        self.visualize_button=tk.Button(self.dashboard_frame,text="Visualize",bg='sky blue',fg='Yellow',command=self.visualize)
        self.visualize_button.place(relx=0.5,rely=0.4, anchor=tk.CENTER)

        #buttton to exit
        self.exit_button=tk.Button(self.dashboard_frame,text="Exit",bg='sky blue',fg='Yellow',command=self.root.quit)
        self.exit_button.place(relx=0.7,rely=0.4, anchor=tk.CENTER)

    def add_expense(self):
        category=self.category.get()
        amount=self.amount_entry.get()
        date=self.date_entry.get()
        sql="INSERT INTO expenses (amount, category, expense_date) VALUES (%s, %s, %s)"
        data=(amount,category,date)
        self.cursor.execute(sql,data)
        self.database.commit()
        self.amount_entry.delete(0, tk.END)



    def visualize(self):
        ...
def main():
    root=tk.Tk()
    finance_tracker=FinanceTracker(root)
    root.mainloop()


if __name__=='__main__':
    main()