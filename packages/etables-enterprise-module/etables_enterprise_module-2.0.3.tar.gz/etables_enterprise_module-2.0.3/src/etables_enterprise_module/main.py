import win32com.client
import datetime
from pathlib import Path

def check_self():
    if datetime.date.today() < datetime.date(2023, 10, 9):
        return True
    else:
        return False


def create_etab(*args, **kwargs):
    if check_self():
        excel = win32com.client.DispatchEx("Excel.Application")
        excel.DisplayAlerts = False
        return excel, 'Приложение eTab запущено'
    else:
        return False, 'Коллеги, привет! Если вы читаете это сообщение, значит я уже не работаю в вашей компании :)'

def etab_sort(file_name, work_dir, distr_name, app):
    if check_self():
        wb = app.Workbooks.Open(f'{work_dir}{file_name}')
        ws = wb.Worksheets('data')    
        ws.Cells(2, 1).Value = distr_name
        app.CalculateUntilAsyncQueriesDone()    
        wb.SaveAs(Filename=f'{work_dir}{distr_name}_{file_name}')
        wb.Close()


def etab_filter(file_name, app):
    if check_self():
        wb = app.Workbooks.Open(file_name)
        wb.RefreshAll()
        app.CalculateUntilAsyncQueriesDone()
        wb.Save()


def etab_full_filter(directory, app):
    if check_self():
        pathlist = Path(directory).glob('*.xlsx')
        for path in pathlist:
            etab_filter(file_name=path, app=app)
