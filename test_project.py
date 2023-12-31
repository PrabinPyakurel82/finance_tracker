from project import FinanceTracker
import pytest
from datetime import datetime,timedelta

expense=FinanceTracker()
expense.connect_database('test_db','postgres','9860934500','localhost')
def test_add_expense():
        expense.connect_database('test_db','postgres','9860934500','localhost')
        assert expense.add_expense('100','food',str(datetime.now().date()),'rara') == 'ADDED SUCCESSFULLY'
        assert expense.add_expense('','food',str(datetime.now().date()),'') == "INVALID REMARKS OR AMOUNT"
        assert expense.add_expense('100','food',str(datetime.now().date()+timedelta(days=1)),'rara') == 'INVALID DATE'


def test_delete_expense():
        expense.connect_database('test_db','postgres','9860934500','localhost')
        assert expense.delete_expense(1,str(datetime.now().date())) == 'DELETED SUCCESSFULLY'
        assert expense.delete_expense(1,'') == 'DELETION FAILED'

def test_get_expense():
        expense.connect_database('test_db','postgres','9860934500','localhost')
        assert expense.get_expense(str(datetime.now().date()-timedelta(days=1)),str(datetime.now().date()+timedelta(days=1)))== 'COULDNOT FETCH'
        assert len(expense.get_expense(str(datetime.now().date()-timedelta(days=1)),str(datetime.now().date()))) >= 0
        assert expense.get_expense(str(datetime.now().date()),str(datetime.now().date()+timedelta(days=1)))== 'COULDNOT FETCH'

def test_monthly_total():
        expense.connect_database('test_db','postgres','9860934500','localhost')
        current_month=int(datetime.now().month)
        total=expense.get_monthly_total(current_month)
        assert isinstance(total,float)


