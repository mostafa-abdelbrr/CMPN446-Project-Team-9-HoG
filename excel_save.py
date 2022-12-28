from datetime import datetime, timedelta

import openpyxl

# Example:
# take_attendance(1180126, 'CMPN462-14310071.xlsx', datetime.strptime('01/10/2022', '%d/%m/%Y'))
def take_attendance(student_id: int, filepath: str, semester_start: datetime, student_count=151):
    first_week: datetime = (semester_start - timedelta(days=semester_start.weekday()))
    current_week: datetime = (datetime.now() - timedelta(days=datetime.now().weekday()))
    weeks_since_semester_started: int = ((current_week - first_week).days // 7)
    workbook = openpyxl.load_workbook(filename=filepath)
    sheet = workbook.active
    for row in sheet.iter_rows(max_row=student_count + 1, max_col=20):
        if row[1].value == str(student_id):
            week_index = weeks_since_semester_started + 4  # Weeks + 1 (to get week number) then + 4 as sheet offset
            row[week_index].value = '1'
            workbook.save(filename=filepath)

# semester
# first_week: datetime = (semester_start - timedelta(days=semester_start.weekday()))
# current_week: datetime = (datetime.now() - timedelta(days=datetime.now().weekday()))