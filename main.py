from utils import GoogleSheetsApi, logger, print_logger

def calculate_student_situation(student_data: list, total_number_of_classes: int = 60) -> tuple:
    """
    Calculates the situation of a student based on their data.
    This calculation is carried out on spreadsheets with a range of grades from 0 to 100.

    Args:
        student_data (list): A list containing student data including Id, name, absences, and grades.
        total_number_of_classes (int, optional): Total number of classes in the course. Defaults to 60.

    Returns:
        tuple: A tuple containing the student's situation and, if applicable, their final grade.
    """
    student_absences = int(student_data[2])
    if (student_absences / total_number_of_classes) * 100 > 25:
        return (['Reprovado por Falta'], [0])
    
    # average of all student tests
    average_test = sum([int(vl) for vl in student_data[3:6]]) / 3

    if average_test >= 70:
        return (['Aprovado'], [0])
    elif average_test < 50:
        return (['Reprovado por Nota'], [0])
    
    # As the student does not have grades lower than 5 or higher than 7, no conditions are necessary
    naf = 100 - average_test   # Calculating the naf based on the simplified formula
    return (['Exame Final'], [round(naf)])

@logger
def start_job(sheet: GoogleSheetsApi) -> None:
    """
    Initiates the job of calculating students' situations and final grades.

    Args:
        sheet (GoogleSheetsApi): An instance of GoogleSheetsApi used to interact with Google Sheets.
    """
    sheet_dt = sheet.sheet_get_values().get('values', [])

    # obtaining the total number of classes through the spreadsheet header
    total_number_of_classes = int(sheet_dt[0][0].split(': ')[1])
    students_data = sheet_dt[2:] # obtain students data

    situation_students = []
    grade_for_final_approval = []

    print_logger("calculating students recovery status and final grade.")
    for student in students_data:
        situation, final_grade = calculate_student_situation(student, total_number_of_classes)
        situation_students.append(situation)
        grade_for_final_approval.append(final_grade)

    sheet.sheet_batch_update([
        {"range": "G4", "values": situation_students},
        {"range": "H4", "values": grade_for_final_approval},
    ])

SAMPLE_SPREADSHEET_ID = "15-otkpRl7Lr-e4Z1vtw7i6X5B9VPb2RoNIlSd6FKHF4"
SAMPLE_RANGE_NAME = "engenharia_de_software!A2:K"

sheet = GoogleSheetsApi(SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME)
start_job(sheet)
