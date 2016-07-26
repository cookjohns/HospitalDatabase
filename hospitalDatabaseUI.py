import sqlite3

# Main driver
def mainFunc():
  print("Welcome to our Hospital Database")
  while True:  
    print("\nSelect the corresponding option or type \"help\"")
    print("\n")
    print("1.  Patient Room Utilization")
    print("2.  Patient Information")
    print("3.  Diagonosis and Treatment Information")
    print("4.  Employee Information")
    print("5.  Quit")
    
    num = raw_input("Enter a command: ")
    if (num == '1'):
      roomUtilization()
    elif (num == '2'):
      patientInformation()
    elif (num == '3'):
      diagnosisAndTreatmentInformation()
    elif (num == '4'):
      employeeInformation()
    elif (num == '5'):
      break
    elif (num == 'help'):
      driverHelp()
    

# Driver help
def driverHelp():
  print("\n\n")
  print("\tRoom Utilization gives information on both occupied ")
  print("\tPatient Information gives information on all patients ")
  print("\t\tin our database")
  print("\tDiagnosis and Treatment Information gives information on ")
  print("\t\ttreatments performed at our hospital as well as all diagnoses ")
  print("\t\tgiven to our patients. There maybe be some HIPAA violations ")
  print("\t\twith this one.")
  print("\tEmployee Information gives information on all workers and ")
  print("\t\tvolunteers at our hospital including their specific jobs and, ")
  print("\t\tif they're a doctor, some treatment information")
  print("\tQuit exits the program\n")



#Room Utilization
def roomUtilization():
  con =   sqlite3.connect('hospitaldb.db')
  c = con.cursor()
  while True:
    print("\n\nEnter a command or type \"back\"")
    print("\t1.  Occupied Patient Rooms")
    print("\t2.  Unoccupied Patient Rooms")
    print("\t3.  All Patient Rooms")

    num = raw_input("Enter a command: ")

    if (num == '1'):
      x = 1
    elif (num == '2'):
      x = 2
    elif (num == '3'):
      x = 3
    elif (num == 'back'):
      break
    

#Patient Information
def patientInformation():
  while True:
    print("\n\nEnter a command or type \"back\"")
    print("\t1.  All Patients")
    print("\t2.  All Admitted Patients")
    print("\t3.  All Admitted Patients in a Given Date Range")
    print("\t4.  All Patients Discharged in a Given Date Range")
    print("\t5.  All Patients Currently Receiving Outpatient Services")
    print("\t6.  All Patients Receiving Outpatient Services in a Given Date Range")
    print("\t7.  All Admission and Diagnoses for a Given Patient")
    print("\t8.  All Treaments Administered to a Given Patient")
    print("\t9.  All Patients Readmitted Within 30 Days of Their "
          + "Last Discharge Date")
    print("\t10. Patient Statistics")
  
    num = raw_input("Enter a command: ")

    if (num == '1'):
      x = 1
    elif (num == '2'):
      x = 2
    elif (num == '3'):
      x = 3
    elif (num == '4'):
      x = 4
    elif (num == '5'):
      x = 5
    elif (num == '6'):
      x = 6
    elif (num == '7'):
      x = 7
    elif (num == '8'):
      x = 8
    elif (num == '9'):
      x = 9
    elif (num == '10'):
      x = 10
    elif (num == 'back'):
      break;


#Diagnoses and Treatment Information
def diagnosisAndTreatmentInformation():
  while True:
    print("\n\nEnter a command or type \"back\"")
    print("\t1.  Diagnoses Given to Admitted Patients")
    print("\t2.  Diagnoses Given to Outpatients")
    print("\t3.  Diagnoses Given to All Patients")
    print("\t4.  Treatments Performed at the Hospital")
    print("\t5.  Treatments Performed on Admitted Patients")
    print("\t6.  Treatments Performed on Outpatients")
    print("\t7.  Diagnoses Associated with Patients with Highest Occurrences of "
          + "Addmissions")
    print("\t8.  Employees Involved in a Given Treatment Occurance")
    
    num = raw_input("Enter a command: ")

    if (num == '1'):
      x = 1
    elif (num == '2'):
      x = 2
    elif (num == '3'):
      x = 3
    elif (num == '4'):
      x = 4
    elif (num == '5'):
      x = 5
    elif (num == '6'):
      x = 6
    elif (num == '7'):
      x = 7
    elif (num == '8'):
      x = 8
    elif (num == 'back'):
      break

#Employee Information
def employeeInformation():
  while True:
    print("\n\nEnter a command or type \"back\"")
    print("\t1.  All Workers")
    print("\t2.  All Volunteers at the Information Desk on Tuesdays")
    print("\t3.  Primary Doctors of Patients with High Admission Rates")
    print("\t4.  All Diagnoses Given by a Specified Doctor")
    print("\t5.  All Treatments Ordered by a Given Doctor")
    print("\t6.  All Treatments in Which a Given Doctor Participated")
    print("\t7.  Employees Involved in Any Treatment")
    
    num = raw_input("Enter a command: ")

    if (num == '1'):
      x = 1
    elif (num == '2'):
      x = 2
    elif (num == '3'):
      x = 3
    elif (num == '4'):
      x = 4
    elif (num == '5'):
      x = 5
    elif (num == '6'):
      x = 6
    elif (num == '7'):
      x = 7
    elif (num == 'back'):
      break

mainFunc();
