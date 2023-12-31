from tkinter import * 
import psycopg2
from tkinter import ttk
from tkcalendar import DateEntry
from matplotlib import pyplot
from datetime import datetime
from PIL import ImageTk, Image
import re
import set_database

class FinanceTracker:
    def __init__(self):
        self.categories = ["food","education","miscellaneous","travel","rent","taxes","health and medicine"]


    def connect_database(self,db_name,user_name,pwd,host):
        #connecting to databse
        self.database=psycopg2.connect(database=db_name,user=user_name,password=pwd,host=host)
        
        #connecting to server
        self.cursor=self.database.cursor()
        self.cursor.execute('''
        CREATE TABLE  IF NOT EXISTS expenses(
            id SERIAL PRIMARY KEY,
            amount REAL,
            category TEXT,
            date DATE,
            remarks TEXT
        )
        ''')
        #commiting change to
        self.database.commit()
    
    def close_database(self):
        self.database.close()

    def add_expense(self,amount,category,date,remarks):
        try:
            if matches := re.match(r"^(\d+)$",amount) and re.match(r"^\w+(\ )*\w+$",remarks):
                pass
            else:
                raise ValueError("INVALID REMARKS OR AMOUNT")

            if date > str(datetime.now().date()):
                raise ValueError("INVALID DATE")

            #sql command
            sql_command = "INSERT INTO expenses(amount,category,date,remarks) VALUES(%s,%s,%s,%s)"
            values = (amount,category,date,remarks)
            #adding to data base
            self.cursor.execute(sql_command,values)
            self.database.commit()

        except ValueError as e:
            return str(e)

        else:
            return 'ADDED SUCCESSFULLY'

    def delete_expense(self,id,date):
        try:
            sql_command = f"DELETE FROM expenses WHERE id={id} AND date='{date}'"
            self.cursor.execute(sql_command)
            self.database.commit()
        except:
            return "DELETION FAILED"
        else:
            return "DELETED SUCCESSFULLY"

    def get_expense(self,start_date,end_date):
        try:
            if str(start_date) <= str(datetime.now().date()) and str(end_date) <= str(datetime.now().date()):
                sql_command=f"SELECT * FROM expenses WHERE date BETWEEN DATE '{start_date}' AND '{end_date}'"
                self.cursor.execute(sql_command)
                expenses=self.cursor.fetchall()
            
            else:
                return "COULDNOT FETCH"
        except:
            return 'COULDNOT FETCH'

        return expenses

    def get_monthly_total(self,month):
        try:
            sql_command=f"SELECT SUM(amount) FROM expenses WHERE EXTRACT(MONTH FROM date)='{month}'"
            self.cursor.execute(sql_command)
            total=self.cursor.fetchone()[0]
            if total:
              return total
            else:
              return 0

        except:
            return 'COULDNOT FETCH'
       
    def get_pie_chart(self,month):
        category_expenses = []
        category_name= []
        
        for category in self.categories:
            sql_command = f"SELECT SUM(amount) FROM expenses WHERE category='{category}' AND EXTRACT(MONTH FROM date)={month}"
            self.cursor.execute(sql_command)
            category_total = self.cursor.fetchone()[0]

            if category_total:
                category_expenses.append(category_total)
                category_name.append(category)

        try:
            if len(category_expenses) == 0:
                raise ValueError("NOT ENOUGH RECORD")

            pyplot.pie(category_expenses, labels=None, autopct='%1.1f%%', startangle=90)
            pyplot.title("EXPENSES OF THIS MONTH")
            pyplot.legend(category_name,loc="right",bbox_to_anchor = (1.36,.05))
            pyplot.savefig("monthly_pie_chart.png")
            pyplot.close()
        
        except ValueError as e:
            return False
        
        else:
            return True

    def get_bar_graph(self):
        sql_command = "SELECT SUM(amount),TO_CHAR(date, 'month') AS expense_month FROM expenses WHERE date >=CURRENT_DATE - INTERVAL '11 months' GROUP BY expense_month ORDER BY MIN(date) ASC"
        self.cursor.execute(sql_command)
        monthly_expenses = self.cursor.fetchall()
        
        amount  = []
        months = []
        for value in monthly_expenses:
            amount.append(value[0])
            months.append((value[1])[0:3])

        try:
            if len(amount) == 0:
                raise ValueError("NOT ENOUGH RECORDS")
                
            pyplot.figure(figsize=(8,6))
            pyplot.bar(months,amount,color="skyblue")
            pyplot.title("THIS YEAR'S EXPENSES")
            pyplot.xlabel("MONTHS")
            pyplot.ylabel("EXPENSES")
            pyplot.savefig("bar_graph.png")
            pyplot.close()
        
        except ValueError as e:
            return False
        
        else:
            return True



class FinanceTrackerGUI(FinanceTracker):
    def __init__(self,root):
        self.root = root
        self.root.title('Finance Tracker')
        self.root.geometry('900x900')
        super().__init__()
        self.connect_database(set_database.name,set_database.user,set_database.password,set_database.host)
        self.create_gui()

    def create_gui(self):
         #initializing frames
        self.welcome_frame = Frame(self.root,bg="teal")
        self.welcome_frame.pack(fill="both",expand=1)
        self.dashboard_frame=Frame()
        self.visualize_frame=Frame()
        self.error_label=Label()

        #welcome label
        self.welcome_label = Label(self.welcome_frame,text="Welcome ",font=("arial",20),fg="yellow",bg="teal")
        self.welcome_label.place(relx=0.505, rely=0.45, anchor='center')

        #button
        self.start_button = Button(self.welcome_frame,text="NEW RECORD",bg="teal",fg="yellow",borderwidth=3,command=self.get_dashboard)
        self.start_button.place(relx=.5,rely=.5,anchor='center')

    def get_dashboard(self):
        self.welcome_frame.destroy()
        self.visualize_frame.destroy()
        #create new frame for dashboard
        self.dashboard_frame = Frame(self.root,bg="teal")
        self.dashboard_frame.pack(expand=1,fil="both")
        
        #label to select category
        self.select_category_label = Label(self.dashboard_frame,text="Select a category",bg="teal",fg="yellow",font=("arial",12))
        self.select_category_label.pack(padx=10,pady=10)
        #drop box for category selection
        self.category_options = ["food","education","miscellaneous","travel","rent","taxes","health and medicine"]
        self.category = ttk.Combobox(self.dashboard_frame,values=self.category_options,font=("arial",10))
        self.category.current(0)
        self.category.pack(padx=10,pady=10)
        
        #entry label
        self.remarks_label = Label(self.dashboard_frame,text="Remarks",bg="teal",fg="yellow",font=("arial",12))
        self.remarks_label.pack(padx=10,pady=10)
        #Entry for amount
        self.remarks_entry = Entry(self.dashboard_frame,width=25)
        self.remarks_entry.pack(padx=10,pady=10)

        #entry label
        self.amount_label = Label(self.dashboard_frame,text="Amount",bg="teal",fg="yellow",font=("arial",12))
        self.amount_label.pack(padx=10,pady=10)
        #Entry for amount
        self.amount_entry = Entry(self.dashboard_frame,width=25)
        self.amount_entry.pack(padx=10,pady=10)
        
        #date label
        self.date_label = Label(self.dashboard_frame,text="Select Date",bg="teal",font=("arial",12),fg="yellow")
        self.date_label.pack(padx=10,pady=10)
        self.date_entry = DateEntry(self.dashboard_frame,width=24,date_pattern = "yyyy-mm-dd", background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.pack(padx=10,pady=10)

        #button 
        #to add expenses
        self.add_expense_button = Button(self.dashboard_frame,text="ADD",bg="teal",fg="yellow",borderwidth=3,command=self.add_now)
        self.add_expense_button.place(relx=.3,rely=.54,anchor="center")

        #to visualize
        self.visualize_expenses_button = Button(self.dashboard_frame,text="VISUALIZE EXPENSES",bg="teal",fg="yellow",borderwidth=3,command=self.visualize_this_month)
        self.visualize_expenses_button.place(relx=.5,rely=.54,anchor="center")

        self.exit_button = Button(self.dashboard_frame,text="EXIT",bg="teal",fg="yellow",borderwidth=3,command=self.exit_app)
        self.exit_button.place(relx=.7,rely=.54,anchor="center")

        if self.get_monthly_total(datetime.now().month) is not None:
            self.total_month_expenses=Label(self.dashboard_frame,text=f"This Month Expenses: RS {self.get_monthly_total(datetime.now().month)}",bg="teal",fg="orange",font=("Arial",14))
            self.total_month_expenses.place(relx=.36,rely=.57)
        
        
        today_expenses=self.get_expense(datetime.now().date(),datetime.now().date())

        if today_expenses:
            today_list=Listbox(self.dashboard_frame,width=60,height=5)
            today_list.place(relx=0.2,rely=0.65)
            for expense in today_expenses:
                #self.recent_expenses_list.insert(END,f"Particular: {expenses[4]}    Amount: Rs {expenses[1]}")
                frame = Frame(today_list,bg="teal",borderwidth=3)
                frame.pack(fill="x")

                label = Label(frame,text=f"Category: {expense[2]}    Amount: Rs {expense[1]}  Remarks: {expense[4]}",bg="teal")  
                label.pack(side="left",ipadx=20)

                button = Button(frame,text="UNDO",command=lambda id = expense[0], date = expense[3]:self.delete_now(id,date),fg="orange",bg="teal",borderwidth=3)
                button.pack(side="right",ipadx=50) 

    def add_now(self):
        category = self.category.get()
        amount = self.amount_entry.get()
        date = self.date_entry.get()
        remarks = self.remarks_entry.get()
        self.error_label.destroy()
        try:
            status=self.add_expense(amount,category,date,remarks)
            if status=="ADDED SUCCESSFULLY":
                self.dashboard_frame.destroy()
                self.get_dashboard()
            else:
                self.error_label = Label(self.dashboard_frame,text=status,bg="teal",fg="#ff7f7f",font=("Arial",12))
                self.error_label.pack()

        except ValueError as e:
            self.error_label = Label(self.dashboard_frame,text=e,bg="teal",fg="#ff7f7f",font=("Arial",12))
            self.error_label.pack()

    def delete_now(self,id,date):
        self.dashboard_frame.destroy()
        self.visualize_frame.destroy()
        self.delete_expense(id,date)
        self.get_dashboard()

    def visualize_this_month(self):
        self.dashboard_frame.destroy()

        #visualize frame
        self.visualize_frame = Frame(self.root,bg='teal')
        self.visualize_frame.pack(expand=1,fill='both')
        
        #create a pie chart
        if (self.get_pie_chart(datetime.now().month)):
            self.pie_image = ImageTk.PhotoImage(Image.open("monthly_pie_chart.png"))
            self.pie_image_label = Label(self.visualize_frame,image=self.pie_image)
            self.pie_image_label.pack(padx=10,pady=10)
        
        else:
            self.visualize_error_label = Label(self.visualize_frame,text="NO ENOUGH RECORD TO VISUALIZE",font=("arial",14),bg="teal",fg="yellow")
            self.visualize_error_label.pack(padx=10,pady=10)

        #NEXT BUTTON FOR BARGRAPH VISUALIZATION
        self.next_button = Button(self.visualize_frame,text="NEXT",bg="teal",fg="yellow",borderwidth=3,command=self.visualize_this_year)
        self.next_button.pack(padx=10,pady=10,ipadx=12)

        #button to go back 
        self.go_back_button = Button(self.visualize_frame,text="GO BACK",bg="teal",fg="yellow",borderwidth=3,command=self.get_dashboard)
        self.go_back_button.pack(padx=10,pady=10)
    
    def visualize_this_year(self):
        for children in self.visualize_frame.winfo_children():
          children.destroy()

        if(self.get_bar_graph()):
            self.bargraph_image = ImageTk.PhotoImage(Image.open("bar_graph.png"))
            self.bargraph_image_label = Label(self.visualize_frame,image=self.bargraph_image)
            self.bargraph_image_label.pack(padx=10,pady=10)
        
        else:
            self.visualize_error_label = Label(self.visualize_frame,text="NO ENOUGH RECORD TO VISUALIZE",font=("arial",14),bg="teal",fg="yellow")
            self.visualize_error_label.pack(padx=10,pady=10)

        self.go_back_button = Button(self.visualize_frame,text="GO BACK",bg="teal",fg="yellow",borderwidth=3,command=self.get_dashboard)
        self.go_back_button.pack(padx=10,pady=10)
    
    def exit_app(self):
        self.close_database()
        self.root.destroy()



def main():
    root=Tk()
    finance=FinanceTrackerGUI(root)
    root.mainloop()
    
if __name__== '__main__':
    main()