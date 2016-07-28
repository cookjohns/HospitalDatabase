import sqlite3
import sys

# Main driver
def mainFunc():
  print('Welcome to our Hospital Database')
  while True:  
    print('\nSelect the corresponding option or type \'help\'\n')
    print('1.  Patient Room Utilization')
    print('2.  Patient Information')
    print('3.  Diagonosis and Treatment Information')
    print('4.  Employee Information')
    print('5.  Quit')
    
    num = raw_input('Enter a command: ')
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

    elif (num.lower() == 'quit'):
      break
    
    elif (num.lower() == 'help'):
      driverHelp()

    else:
      print('\nInvalid Input.')
    

# Driver help
def driverHelp():
  print('\n\n')
  print('\tRoom Utilization gives information on both occupied')
  print('\t\tand unoccupied rooms.')
  print('\tPatient Information gives information on all patients ')
  print('\t\tin our database.')
  print('\tDiagnosis and Treatment Information gives information on ')
  print('\t\ttreatments performed at our hospital as well as all diagnoses ')
  print('\t\tgiven to our patients. There maybe be some HIPAA violations ')
  print('\t\twith this one.')
  print('\tEmployee Information gives information on all workers and ')
  print('\t\tvolunteers at our hospital including their specific jobs and, ')
  print('\t\tif they\'re a doctor, some treatment information.')
  print('\tQuit exits the program.\n')
  

#Room Utilization
def roomUtilization():
  con =   sqlite3.connect('HospitalDB.db')
  c = con.cursor()
  while True:
    print('\n\nEnter a command or type \'back\'')
    print('\t1.  Occupied Patient Rooms')
    print('\t2.  Unoccupied Patient Rooms')
    print('\t3.  All Patient Rooms')

    num = raw_input('Enter a command: ')

    if (num == '1'):
      try:
        for row in c.execute('''SELECT roomNumber, firstName, lastName, timeAdmitted, patientID
             FROM (Admits as A join PatientRoom using (patientID)) join
                Patient using (patientID)
             WHERE A.timeAdmitted > (SELECT MAX (date)
                                     FROM Discharges as C
                                     WHERE A.patientID = C.patientID);
          '''):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in roomUtilization 1:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '2'):
      try:
        for row in c.execute('''SELECT pr.roomNumber 
           FROM PatientRoom pr LEFT JOIN RoomAssignment ra ON pr.roomNumber = ra.roomNumber
           WHERE ra.patientId IS NULL;'''):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in roomUtilization 2:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '3'):
      try:
        for row in c.execute('''SELECT pr.roomNumber, p.firstName, p.lastName, a.admittedDate
          FROM PatientRoom pr
            LEFT JOIN RoomAssignment ra 
            ON pr.roomNumber = ra.roomNumber
            JOIN Patient p 
            ON ra.patientId = p.patientId
            JOIN Admits a 
            ON p.patientId = a.patientId;'''):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in roomUtilization 3:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])

    elif (num.lower() == 'back'):
      con.close()
      break

    else:
      print('\nInvalid Input.')


#Patient Information
def patientInformation():
  con =   sqlite3.connect('HospitalDB.db')
  c = con.cursor()
  while True:
    print('\n\nEnter a command or type \'back\'')
    print('\t1.  All Patients')
    print('\t2.  All Admitted Patients')
    print('\t3.  All Admitted Patients in a Given Date Range')
    print('\t4.  All Patients Discharged in a Given Date Range')
    print('\t5.  All Patients Currently Receiving Outpatient Services')
    print('\t6.  All Patients Receiving Outpatient Services in a Given Date Range') 
    print('\t7.  All Admission and Diagnoses for a Given Patient') 
    print('\t8.  All Treaments Administered to a Given Patient') 
    print('\t9.  All Patients Readmitted Within 30 Days of Their '  #\nNYI
           'Last Discharge Date')
    print('\t10. Patient Statistics') #\nNYI
  
    num = raw_input('Enter a command: ')
    
    if (num == '1'):
      try:    
        for row in c.execute('''SELECT *
          FROM Patient;'''):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in patientInformation 1:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '2'):
      try:
        for row in c.execute('''SELECT patientId, firstName, lastName
          FROM (
            SELECT p.patientId, d.date
            FROM Patient p JOIN Discharges d ON p.patientId = d.patientId) DischargeDates
              LEFT JOIN (
                SELECT p.patientId, p.firstName, p.lastName
                FROM Patient p JOIN InPatients ip ON p.patientId = ip.patientId) InPatientNames
              ON DischargeDates.patientId = InPatientNames.patientId
              WHERE date IS NULL;'''):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in patientInformation 2:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '3'):
      dates = ['', '']
      dates[0] = raw_input('Enter a startDate: ')
      dates[1] = raw_input('Enter an endDate: ')
      try:
        for row in c.execute('''SELECT p.patientId, p.firstName, p.lastName
          FROM Patient p 
            JOIN InPatient ip 
            ON p.patientId = ip.patientId
            JOIN Administers a
            ON ip.patientId = a.patientId
          WHERE a.timeAdministered < ?
          AND a.timeAdministered > ?;''', dates):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in patientInformation 3:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except TypeError as err2:
        print("\nSomething went wrong in patientInformation 3:")
        print("TypeError: {0}".format(err2))
      except:
        print("Unexpected Error: ", sys.exc_info()[0])
          
    elif (num == '4'):
      dates = ['', '']
      dates[0] = raw_input('Enter a startDate: ')
      dates[1] = raw_input('Enter an endDate: ')
      try:
        for row in c.execute('''SELECT p.patientId, p.firstName, p.lastName
          FROM Patient p JOIN Discharges d ON p.patientId = d.patientId
          WHERE d.date > ?
          AND d.date < ?; ''', dates):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in patientInformation 4:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except TypeError as err2:
        print("\nSomething went wrong in patientInformation 4:")
        print("TypeError: {0}".format(err2))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '5'):
      try:
        for row in c.execute(''''SELECT patientId, firstName, lastName
           FROM (
                  SELECT p.patientId, d.date
                  FROM Patient p JOIN Discharges d ON p.patientId = d.patientId) DischargeDates
                  LEFT JOIN ( 
                  SELECT p.patientId, p.firstName, p.lastName
                  FROM Patient p JOIN OutPatients op ON p.patientId = op.patientId) InPatientNames
                  ON DischargeDates.patientId = InPatientNames.patientId
           WHERE date IS NULL;'''):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in patientInformation 5:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '6'):
      dates = ['', '']
      dates[0] = raw_input('Enter a startDate: ')
      dates[1] = raw_input('Enter an endDate: ')
      try:
        for row in c.execute('''SELECT p.patientId, p.firstName, p.lastName
           FROM Admits a JOIN (
                  SELECT p.patientId, p.firstName, p.lastName
                  FROM Patient p JOIN OutPatients op ON p.patientId = op.patientId) OutPatientNames
           WHERE a.date > ?
           AND a.date < ?;''', dates):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in patientInformation 6:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except TypeError as err2:
        print("\nSomething went wrong in patientInformation 3:")
        print("TypeError: {0}".format(err2))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
      
    elif (num == '7'):
      requestedPatient = raw_input('Enter a patient\'s name: ')
      try:
        for row in c.execute('''SELECT a.date, d.diagnosis
           FROM Diagnoses d
                  JOIN Admits a
                          ON d.diagnosesId = a.diagnosesId
                  LEFT JOIN Patient p 
                          ON a.patientId = p.patientId
           WHERE p.patientId = ?;''', requestedPatient):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in patientInformation 7:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '8'):
      requestedPatient = raw_input('Enter a patient\'s name: ')
      try:
        for row in c.execute('''SELECT admit.date, t.treatmentId
           FROM InPatient ip
                  JOIN Administers admin
                          ON ip.patientId = admin.patientId
                  JOIN Treatment t
                          ON a.treatmentId = t.treatmentId
                  JOIN Admits admit
                          ON admit.patientId = ip.patientId
           WHERE ip.patientId = ?
           GROUP BY admit.date
           ORDER BY admit.date DESC, admin.timeAdministered ASC;''', requestedPatient):
            print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in patientInformation 8:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '9'):
      print('\nNYI')
      try:
        c.execute('')
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in patientInformation 9:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])

    elif (num == '10'):
      print('\nNYI')
      try:
        c.execute('')
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in patientInformation 10:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num.lower() == 'back'):
      con.close()
      break;
      
    else:
      print('\nInvalid Input.')


#Diagnoses and Treatment Information
def diagnosisAndTreatmentInformation():
  con =   sqlite3.connect('HospitalDB.db')
  c = con.cursor()
  while True:
    print('\n\nEnter a command or type \'back\'')
    print('\t1.  Diagnoses Given to Admitted Patients')
    print('\t2.  Diagnoses Given to Outpatients')
    print('\t3.  Diagnoses Given to All Patients')
    print('\t4.  Treatments Performed at the Hospital') #\nNYI
    print('\t5.  Treatments Performed on Admitted Patients')
    print('\t6.  Treatments Performed on Outpatients') #\nNYI
    print('\t7.  Diagnoses Associated with Patients with Highest Occurrences of ' #\nNYI
           + 'Addmissions')
    print('\t8.  Employees Involved in a Given Treatment Occurance') ##\nNYI
    
    num = raw_input('Enter a command: ')

    if (num == '1'):
      try:
        for row in c.execute('''SELECT d.diagnosisId, d.name, COUNT(DISTINCT d.diagnosesId)
           FROM InPatient ip 
                  JOIN Patient p
                          ON ip.patientId = p.patientId
                  JOIN Admits a
                          ON p.patientId = a.patientId
                  JOIN Diagnoses d
                          ON a.diagnosisId = d.diagnosisId
           GROUP BY d.diagnosisId
           ORDER BY a.date DESC;'''):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in diagnosisAndTreatment 1:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '2'):
      try:
        for row in c.execute('''SELECT d.diagnosisId, d.name, COUNT(DISTINCT d.diagnosesId)
           FROM OutPatient op 
                  JOIN Patient p
                          ON op.patientId = p.patientId
                  JOIN Admits a
                          ON p.patientId = a.patientId
                  JOIN Diagnoses d
                          ON a.diagnosisId = d.diagnosisId
           GROUP BY d.diagnosisId
           ORDER BY a.date DESC;'''):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in diagnosisAndTreatment 2:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '3'):
      try:
        for row in c.execute('''SELECT d.diagnosisId, d.name, COUNT(DISTINCT d.diagnosesId)
          FROM Patient p
            JOIN Admits a
              ON p.patientId = a.patientId
            JOIN Diagnoses d
              ON a.diagnosisId = d.diagnosisId
          GROUP BY d.diagnosisId
          ORDER BY a.date DESC;'''):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in diagnosisAndTreatment 3:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])

    elif (num == '4'):
      print('\nNYI')
      try:
        c.execute('')
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in diagnosisAndTreatment 4:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '5'):
      try:
        for row in c.execute('''SELECT t.treatmentId, t.name, COUNT(DISTINCT t.treatmentId)
          FROM 
          GROUP BY t.treatmentId
          ORDER BY a.timeAdministered;'''):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in diagnosisAndTreatment 5:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '6'):
      print('\nNYI')
      try:
        c.execute('')
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in diagnosisAndTreatment 6:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '7'):
      print('\nNYI')
      try:
        c.execute('')
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in diagnosisAndTreatment 7:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '8'):
      print('\nNYI')
      try:
        c.execute('')
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in diagnosisAndTreatment 8:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num.lower() == 'back'):
      con.close()
      break
      
    else:
      print('\nInvalid Input.')


#Employee Information
def employeeInformation():
  con =   sqlite3.connect('HospitalDB.db')
  c = con.cursor()
  while True:
    print('\n\nEnter a command or type \'back\'')
    print('\t1.  All Workers')
    print('\t2.  All Volunteers at the Information Desk on Tuesdays')
    print('\t3.  Primary Doctors of Patients with High Admission Rates') #\nNYI
    print('\t4.  All Diagnoses Given by a Specified Doctor') 
    print('\t5.  All Treatments Ordered by a Given Doctor') ##\nNYI
    print('\t6.  All Treatments in Which a Given Doctor Participated') 
    print('\t7.  Employees Involved in Any Treatment')
    
    num = raw_input('Enter a command: ')
    
    if (num == '1'):
      try:
        for row in c.execute('''SELECT employeeId, firstName, lastName, category, hireDate
          FROM (
                  SELECT w.employeeId, w.firstName, w.lastName, \'Technician\' AS category, w.hireDate
                  FROM Worker w JOIN Technician t ON w.employeeId = t.employeeId
                  UNION
                  SELECT w.employeeId, w.firstName, w.lastName, \'Nurse\' AS category, w.hireDate
                  FROM Worker w JOIN Nurse n ON w.employeeId = n.employeeId
                  UNION
                  SELECT w.employeeId, w.firstName, w.lastName, \'Doctor\' AS category, w.hireDate
                  FROM Worker w JOIN Doctor d ON w.employeeId = d.employeeId
                  UNION
                  SELECT w.employeeId, w.firstName, w.lastName, \'Admin\' AS category, w.hireDate
                  FROM Worker w JOIN Admin a ON w.employeeId = a.employeeId
                  UNION
                  SELECT w.employeeId, w.firstName, w.lastName, \'Staff\' AS category, w.hireDate
                  FROM Worker w JOIN Staff s ON w.employeeId = s.employeeId
                  UNION
                  SELECT w.employeeId, w.firstName, w.lastName,\'Volunteer\' AS category, w.hireDate
                  FROM Worker w JOIN Volunteer v ON w.employeeId = v.employeeId) employeeData
          ORDER BY lastName ASC, firstName ASC;'''):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in employeeInformation 1:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '2'):
      try:
        for row in c.execute('''SELECT v.employeeId
           FROM Volunteer v
                  JOIN VolunteersIn vi
                          ON v.employeeId = vi.employeeId
                  JOIN VolunteerRoom vr
                          ON vi.roomId = vr.roomId
                  JOIN InfoDesk id
                          ON vr.roomId = id.roomId
          WHERE vi.dayOfWeek = \'Tuesday\';'''):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in employeeInformation 2:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '3'):
      print('\nNYI')
      try:  
        c.execute('')
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in employeeInformation 3:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '4'):
      requestedDoctor = raw_input('Enter a doctor\'s name: ')
      try:
        for row in c.execute('''SELECT d.diagnosis, COUNT(d.diagnosis) totalOccurences
          FROM Doctor doc JOIN Diagnoses d ON doc.employeeId = d.employeeId
          WHERE doc.employeeId = ?
          GROUP BY d.diagnosis
          ORDER BY d.date DESC;''', requestedDoctor):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in employeeInformation 4:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '5'):
      print('\nNYI')
      try:
        c.execute('')
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in employeeInformation 5:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '6'):
      requestedDoctor = raw_input('Enter a doctor\'s name: ')
      try:
        for row in c.execute('''SELECT t.treatmentId, COUNT(t.treatmentId) as totalAdministered
          FROM Doctor doc
                  JOIN TreatmentGiver tg
                          ON doc.employeeId = tg.employeeId
                  JOIN Administers a
                          ON tg.employeeId = a.employeeId
                  JOIN Treatment t
                          ON a.treatmentId = treatmentId
          WHERE doc.employeeId = ?
          GROUP BY t.treatmentId
          ORDER BY a.timeAdministered DESC;''', requestedDoctor):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in employeeInformation 6:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '7'):
      try:
        for row in c.execute('''SELECT tg.employeeId
          FROM TreatmentGiver tg JOIN Administers a ON tg.employeeId = a.employeeId
          GROUP BY tg.employeeId
          HAVING COUNT(DISTINCT a.patientId) = (
                  SELECT COUNT(DISTINCT p.patientId)
                  FROM Administers a);'''):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in employeeInformation 7:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num.lower() == 'back'):
      con.close()
      break
      
    else:
      print('\nInvalid Input.')
      
mainFunc();
