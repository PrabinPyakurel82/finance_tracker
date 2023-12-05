import psycopg2
import tkinter as tk
import matplotlib
from matplotlib import pyplot as plt
from PIL import ImageTk,Image

def create_database():
    database=psycopg2.connect(database='cs50_final_project',user='postgres',password='9860934500',host='localhost')
    cursor=database.cursor()
    cursor.execute('''
    CREATE TABLE  IF NOT EXISTS expenses(
        id SERIAL PRIMARY KEY,
        amount REAL,
        category TEXT,
        expense_date DATE
    )
    ''')
    database.commit()
    database.close()

def add_expense(amount,category):
    pass

def calculate_budget(expenses):
    pass

def visualize_spending():
    x=[5,6,7,8]
    y=[10,20,30,40]
    plt.plot(x,y)
    plt.savefig('my_plot.png')

def create_gui():
    root=tk.Tk()
    root.title("Finance Tracker")
    root.geometry("600x800")
    my_image=ImageTk.PhotoImage(Image.open('my_plot.png'))
    image_label=tk.Label(root,image=my_image)
    image_label.pack(padx=10,pady=10)
    root.mainloop()
    
def main():
   create_database()
   #visualize_spending()
   create_gui()

if __name__=='__main__':
    main()