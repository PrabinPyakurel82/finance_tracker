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


    def connect_database(self,db_name,user_name,host):
        #connecting to databse
        self.database=psycopg2.connect(database=db_name,user=user_name,host=host)
        
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
