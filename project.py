import psycopg2
import tkinter as tk
from tkinter import ttk
import matplotlib
from matplotlib import pyplot as plt
from PIL import ImageTk,Image
from tkcalendar import DateEntry
from datetime import datetime

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
            expense_date DATE,
            remarks TEXT
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
        self.dashboard_frame=tk.Frame(self.root)
        self.visualize_frame=tk.Frame(self.root)
    
    def get_dashboard(self):
        #Destroy an existing start frame
        self.start_frame.destroy()
        self.visualize_frame.destroy()
        #create a new frame
        self.dashboard_frame=tk.Frame(self.root,bg='teal')
        self.dashboard_frame.pack(fill='both',expand=1)
        #list of categories
        self.categories=['Food','Rent','Education','Travel','Miscellneous','Taxes','Health and Medicine']
        #label for category
        self.select_category=tk.Label(self.dashboard_frame,text='Select a category:',bg='teal',fg='yellow',font=('Arial',12))
        self.select_category.pack(padx=10,pady=10)
        #combobox for category
        self.category=ttk.Combobox(self.dashboard_frame, values=self.categories,font=('Arial',10))
        self.category.current(0)
        self.category.pack(padx=10,pady=10)

        #label for remarks
        self.remarks_label=tk.Label(self.dashboard_frame,text='Remarks:',bg='teal',fg='yellow',font=("Arial",12))
        self.remarks_label.pack(padx=10,pady=10)
        self.remarks=tk.Entry(self.dashboard_frame,width=25)
        self.remarks.pack(padx=10,pady=10)

        #entry box for amount
        self.amount_label=tk.Label(self.dashboard_frame, text='Amount',bg='teal',fg='yellow',font=('Arial',12))
        self.amount_label.pack(pady=10, padx=10)
        self.amount_entry=tk.Entry(self.dashboard_frame,width=25)
        self.amount_entry.pack(padx=10,pady=10)

        # Create a DateEntry widget
        self.date_label = tk.Label(self.dashboard_frame, text='Select Date:', font=("Arial", 12), bg='teal', fg='yellow')
        self.date_label.pack(padx=10,pady=10)
        self.date_entry=DateEntry(self.dashboard_frame,width=25, background='sky blue', foreground='black', borderwidth=2)
        self.date_entry.pack(pady=10,padx=10)
        
        #button to add expense
        self.add_expense_button=tk.Button(self.dashboard_frame,text="Add",bg='sky blue',fg='Yellow',command=self.add_expense)
        self.add_expense_button.place(relx=0.3,rely=0.53, anchor=tk.CENTER)
    
        #button to visualize
        self.visualize_button=tk.Button(self.dashboard_frame,text="Visualize",bg='sky blue',fg='Yellow',command=self.visualize)
        self.visualize_button.place(relx=0.5,rely=0.53, anchor=tk.CENTER)

        #buttton to exit
        self.exit_button=tk.Button(self.dashboard_frame,text="Exit",bg='sky blue',fg='Yellow',command=self.exit_app)
        self.exit_button.place(relx=0.7,rely=0.53, anchor=tk.CENTER)

        self.show_recent_expenses()

    def add_expense(self):
        #get the inputs
        category=self.category.get()
        amount=self.amount_entry.get()
        date=self.date_entry.get()
        remarks=self.remarks.get()
        
        #sql command
        sql="INSERT INTO expenses (amount, category, expense_date,remarks) VALUES (%s, %s, %s,%s)"
        data=(amount,category,date,remarks)

        #insert into database
        self.cursor.execute(sql,data)
        self.database.commit()
        
        #clear the amount field
        self.amount_entry.delete(0, tk.END)
        self.show_recent_expenses()

    def show_recent_expenses(self):
        sql="SELECT * FROM expenses WHERE expense_date=CURRENT_DATE"
        self.cursor.execute(sql)
        self.today_expenses=self.cursor.fetchall()
        if len(self.today_expenses)!=0:
            self.list_label=tk.Label(self.dashboard_frame,text="Today's Expenses:",bg='teal',fg='yellow')
            self.list_label.place(relx=0.15,rely=0.6)
            self.expenses_listbox=tk.Listbox(self.dashboard_frame,width=60,height=5)
            self.expenses_listbox.place(relx=0.2,rely=0.65)
            for expense in self.today_expenses:
              expense_info = f"Amount: {expense[1]}, Category: {expense[2]}, Remarks: {expense[4]}"
              frame = tk.Frame(self.expenses_listbox)
              frame.pack(fill='x')
              label = tk.Label(frame, text=expense_info)
              label.pack(side='left')
              undo_button = tk.Button(frame, text="Undo",command=lambda: self.delete_expenses(expense[0]))
              undo_button.pack(side='right')

    def delete_expenses(self,id):
        self.dashboard_frame.destroy()
        sql=f'DELETE FROM expenses WHERE id={id}'
        self.cursor.execute(sql)
        self.database.commit()
        self.get_dashboard()
        self.visualize_frame.destroy()

    def exit_app(self):
        self.root.destroy()
        self.database.close()
        self.root.quit()

    def visualize(self):
        #destroy the dashboard frame
        self.dashboard_frame.destroy()
        self.visualize_frame=tk.Frame(self.root,bg='teal')
        self.visualize_frame.pack(fill='both',expand=1)
        #create a sql command
        
        current_month=str(datetime.now().month)
        self.category_expenses=[]
        self.category_labels=[]
       
        for category in self.categories:
            sql=f"SELECT SUM(amount) FROM expenses WHERE category='{category}' AND EXTRACT(MONTH FROM expense_date)={current_month}"
            self.cursor.execute(sql)
            expenses=self.cursor.fetchone()[0]
            if expenses:
               self.category_expenses.append(expenses)
               self.category_labels.append(category)
            #else:
                #self.category_expenses.append(0)
            
    
        
        try:
          plt.pie(self.category_expenses,labels=None, autopct='%1.1f%%',startangle=90)
          plt.legend(self.category_labels, loc='right', bbox_to_anchor=(1.35, 0.05))
          plt.savefig("my_pie_chart.png")
          plt.close()
          self.my_image=ImageTk.PhotoImage(Image.open('my_pie_chart.png'))
          self.image_label=tk.Label(self.visualize_frame,image=self.my_image)
          self.image_label.pack(padx=10,pady=10)

        except:
            self.error_label=tk.Label(self.visualize_frame,text="NOT ENOUGH RECORD TO VISUALIZE",bg='teal',font=('Arial',12))
            self.error_label.pack()
            print()

        self.back_button=tk.Button(self.visualize_frame,text="Go Back",command=self.get_dashboard)
        self.back_button.pack(padx=10,pady=10)
        
def main():
    root=tk.Tk()
    finance_tracker=FinanceTracker(root)
    root.mainloop()


if __name__=='__main__':
    main()