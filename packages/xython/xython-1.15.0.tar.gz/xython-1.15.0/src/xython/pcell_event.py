# -*- coding: utf-8 -*-
import time  #내장모듈

import pythoncom #pywin32의 모듈
import win32com.client as win32 #pywin32의 모듈

class ApplicationEvents:
    def OnNewWorkbook(self, *args):
        print("Application Event => OnNewWorkbook, 엑셀->새로운 워크북")

    def OnSheetActivate(self, *args):
        print("Application Event => OnSheetActivate, 엑셀->다른 시트로 이동")

    def OnActivate(self, *args):
        print("Application Event => OnActivate, 엑셀->실행")

    def OnSheetBeforeDoubleClick(self, *args):
        print("Application Event => OnSheetBeforeDoubleClick, 엑셀->더블클릭 전에")

    def OnSheetBeforeRightClick(self, *args):
        print("Application Event => OnSheetBeforeRightClick, 엑셀->오른쪽 클릭전에")

    def OnSheetCalculate(self, *args):
        print("Application Event => OnSheetCalculate 엑셀->시트계산하고나서")

    def OnSheetChange(self, *args):
        print("Application Event => OnSheetChange, 엑셀->시트->셀값변경")

    def OnSheetDeactivate(self, *args):
        print("Application Event => OnSheetDeactivate,  엑셀->시트->비활성화")

    def OnSheetSelectionChange(self, *args):
        print("Application Event => OnSheetSelectionChange, 엑셀->시트->선택영역변경")

    def OnWindowActivate(self, *args):
        print("Application Event => OnWindowActivate, 엑셀->실행")

    def OnWindowDeactivate(self, *args):
        print("Application Event => OnWindowDeactivate, 엑셀->종료")

    def OnWindowResize(self, *args):
        print("Application Event => OnWindowResize, 엑셀->크기변경")

    def OnWorkbookActivate(self, *args):
        print("Application Event => OnWorkbookActivate, 엑셀->워크북->활성화")

    def OnWorkbookBeforeClose(self, *args):
        print("Application Event => OnWorkbookBeforeClose, 엑셀->워크북->비활성화")

    def OnWorkbookBeforSave(self, *args):
        print("Application Event => OnWorkbookBeforSave, 엑셀->워크북->저장되기전")

    def OnWorkbookDeactivate(self, *args):
        print("Application Event => OnWorkbookDeactivate, 엑셀->워크북->비활성화")

    def OnWorkbookNewSheet(self, *args):
        print("Application Event => OnWorkbookNewSheet, 엑셀->워크북->새로운시트")

    def OnWorkbookOpen(self, *args):
        print("Application Event => OnWorkbookOpen, 엑셀->워크북->열때")

class WorkbookEvents:
    def OnActivate(self, *args):
        print("Workbook Event => OnActivate, 워크북->활성화")

    def OnBeforeClose(self, *args):
        print("Workbook Event => OnBeforeClose, 워크북->꺼지기 전에 실행")

    def OnBeforSave(self, *args):
        print("Workbook Event => OnBeforSave, 워크북->저장되기 전")

    def OnDeactivate(self, *args):
        print("Workbook Event => OnDeactivate, 워크북->비활성화")

    def OnNewSheet(self, *args):
        print("Workbook Event => OnNewSheet, 워크북->새로운시트 만들때")

    def OnOpen(self, *args):
        print("Workbook Event => OnOpen, 워크북->새로운 워크북 열때")

    def OnSheetActivate(self, *args):
        print("Workbook Event => OnSheetActivate, 워크북->시트활성화")

    def OnSheetBeforeDoubleClick(self, *args):
        print("Workbook Event => OnSheetBeforeDoubleClick, 워크북->더블클릭 전에")

    def OnSheetBeforeRightClick(self, *args):
        print("Workbook Event => OnSheetBeforeRightClick, 워크북->오른쪽 클릭전에")

    def OnSheetCalculate(self, *args):
        print("Workbook Event => OnSheetCalculate, 워크북->계산후에")

    def OnSheetChange(self, *args):
        print("Workbook Event => OnSheetChange, 워크북->시트변경")

    def OnSheetDeactivate(self, *args):
        print("Workbook Event => OnSheetDeactivate, 워크북->워크시트 비활성화")

    def OnSheetSelectionChange(self, *args):
        print("Workbook Event => OnSheetSelectionChange, 워크북->시트->Selection변경")

    def OnWindowActivate(self, *args):
        print("Workbook Event => OnWindowActivate, 워크북->엑셀-> 실행")

    def OnWindowDeactivate(self, *args):
        print("Workbook Event => OnWindowDeactivate, 워크북->엑셀->종료")

    def OnWindowResize(self, *args):
        print("Workbook Event => OnWindowResize, 워크북->엑셀->창크기변경")

class SheetEvents:
    def OnActivate(self, *args):
        print("Sheet Event => OnActivate, 시트->활성화")

    def OnSheetBeforeDoubleClick(self, *args):
        print("Sheet Event => OnSheetBeforeDoubleClick, 시트->더블클릭 전")

    def OnBeforeRightClick(self, *args):
        print("Sheet Event => OnBeforeRightClick, 시트->오른쪽 클릭전에")

    def OnCalculate(self, *args):
        print("Sheet Event => OnCalculate, 시트->계산하고나서")

    def OnChange(self, *args):
        print("Sheet Event => OnChange, 시트->셀의 뭔가가 변경")

    def OnDeactivate(self, *args):
        print("Sheet Event => OnDeactivate, 시트->비활성화")

    def OnSelectionChange(self, *args):
        print("Sheet Event => OnSelectionChange, 시트->Selection변경")


excel = win32.dynamic.Dispatch("Excel.Application")
excel.Visible = 1
workbook = excel.ActiveWorkbook
sheet = excel.ActiveSheet
excel_application_event = win32.WithEvents(excel, ApplicationEvents)
excel_workbook_event = win32.WithEvents(workbook, WorkbookEvents)
excel_sheet_event = win32.WithEvents(sheet, SheetEvents)

while True:
    pythoncom.PumpWaitingMessages()
    time.sleep(0.01)