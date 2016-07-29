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
        print('RoomNumber, FirstName, LastName, TimeAdmitted, PatientID')
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
        print('RoomNumber')
        for row in c.execute('''SELECT pr.roomNumber AS roomNumber
          FROM PatientRoom pr
          WHERE pr.roomNumber NOT IN (
	  SELECT roomNumber
	  FROM (Admits as A join PatientRoom using (patientID)) join Patient using (patientID)
	  WHERE A.timeAdmitted > (select MAX (date)
	  FROM Discharges as C
	  WHERE A.patientID = C.patientID));'''):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in roomUtilization 2:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '3'):
      try:
        print('RoomNumber, FirstName, LastName, TimeAdmitted, PatientID')
        for row in c.execute('''SELECT roomNumber, firstName, lastName, timeAdmitted, patientID
          FROM (Admits as A join PatientRoom using (patientID)) join Patient using (patientID)
          WHERE A.timeAdmitted > (select MAX (date)
            FROM Discharges AS C
	    WHERE A.patientID = C.patientID)
	    UNION
          SELECT pr.roomNumber AS roomNumber, null, null, null, null
          FROM PatientRoom pr
          WHERE pr.roomNumber NOT IN (
            SELECT roomNumber
	    FROM (Admits AS A JOIN PatientRoom USING (patientID)) JOIN Patient USING (patientID)
	    WHERE A.timeAdmitted > (SELECT MAX (date)
	    FROM Discharges AS C
	    WHERE A.patientID = C.patientID));'''):
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
    print('\t9.  All Patients Readmitted Within 30 Days of Their '  
           'Last Discharge Date')
    print('\t10. Patient Statistics')
  
    num = raw_input('Enter a command: ')
    
    if (num == '1'):
      try:
        print('PatientID, FirstName, LastName, InsurancePolicy, EmergencyContact')
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
        print('PatientID, FirstName, LastName')
        for row in c.execute('''SELECT currentPatients.patientId AS patientID, currentPatients.firstName, currentPatients.lastName
          FROM InPatient ip
            JOIN(
                SELECT p.patientId, p.firstName, p.lastName
                FROM Patient p LEFT JOIN Discharges d ON p.patientId = d.patientId WHERE d.date IS NULL)
                currentPatients
              ON ip.patientId = currentPatients.patientId;'''):
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
        print('PatientID, FirstName, LastName')
        for row in c.execute('''SELECT p.patientId, p.firstName, p.lastName
          FROM Patient p 
            JOIN InPatient ip ON p.patientId = ip.patientId
            JOIN Administers a ON ip.patientId = a.patientId
          WHERE a.timeAdministered > ?
          AND a.timeAdministered < ?;''', dates):
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
        print('PatientID, FirstName, LastName')
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
        print('PatientID, FirstName, LastName')
        for row in c.execute('''SELECT currentPatients.patientId AS patientID,
          currentPatients.firstName || \' \' || currentPatients.lastName AS patientName
          FROM OutPatient op
            JOIN (
              SELECT p.patientId, p.firstName, p.lastName
              FROM Patient p LEFT JOIN Discharges d ON p.patientId = d.patientId WHERE d.date IS NULL) currentPatients
            ON op.patientId = currentPatients.patientId;'''):
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
        print('PatientID, FirstName, LastName')
        for row in c.execute('''SELECT DISTINCT(OutPatientNames.patientId) AS patientId, 
          OutPatientNames.firstName || ' ' || OutPatientNames.lastName AS patientName
          FROM Admits a JOIN (
            SELECT p.patientId, p.firstName, p.lastName
            FROM Patient p JOIN OutPatient op ON p.patientId = op.patientId) OutPatientNames
          WHERE a.timeAdmitted > ?
          AND a.timeAdmitted < ?;''', dates):
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
      requestedPatient = raw_input('Enter a patient\'s ID:')
      try:
        print('TimeAdmitted, DIagnosisID, DiagnosisName')
        for row in c.execute('''SELECT a.timeAdmitted AS admission, d.diagnosisId, d.name AS diagnosisName
          FROM Diagnoses d
            JOIN Admits a ON d.diagnosisId = a.diagnosisId
	    LEFT JOIN Patient p ON a.patientId = p.patientId
          WHERE p.patientId = ?;''', (requestedPatient,)):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in patientInformation 7:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '8'):
      requestedPatient = raw_input('Enter a patient\'s ID:')
      try:
        print('TreatmentID, TreatmentName')
        for row in c.execute('''SELECT patientTreatments.treatmentId AS treatmentId, patientTreatments.name AS name
          FROM Admits a 
          JOIN (
            SELECT t.treatmentId, t.name, treatedPatients.patientId
              FROM Treatment t 
		JOIN (
                  SELECT p.patientId, a.treatmentId
                  FROM Patient p JOIN Administers a ON p.patientId = a.patientId
                    ORDER BY a.timeAdministered ASC) treatedPatients
                  ON t.treatmentId = treatedPatients.treatmentId
                  WHERE treatedPatients.patientId = ?) patientTreatments
          ON patientTreatments.patientId = a.patientId
          GROUP BY a.timeAdmitted
          ORDER BY a.timeAdmitted DESC;''', (requestedPatient,)):
            print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in patientInformation 8:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '9'):
      try:
        print('PatientID, FirstName, LastName, Diagnosis, DoctorID')
        for row in c.execute('''SELECT K.patientID as patientID, firstName || ' ' || lastName as name, name as diagnosis, employeeID as doctorID
          FROM 
          ((SELECT roomNumber, firstName, lastName, timeAdmitted, patientID, employeeID, diagnosisId
          FROM (Admits as A join PatientRoom using (patientID)) join Patient using (patientID)
          WHERE A.timeAdmitted > (select MAX (date)
          from Discharges as C
          where A.patientID = C.patientID)) as K join
          Discharges as D on (D.patientID = K.patientID)) join Diagnoses using (diagnosisId)
          GROUP BY K.patientID
          HAVING (MAX(timeAdmitted) - MAX(date)) <= 30;'''):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in patientInformation 9:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])

    elif (num == '10'):
      try:
        print('PatientID, NumAdmissions, AVGDuration, MaxSpan, MinSpan, AVGSpan')
        for row in c.execute('''SELECT V.patientID, V.NumAdmissions, V.AVGDuration, T.MaxSpan, T.MinSpan, T.AVGSpan
	FROM (SELECT A.patientID,
		MAX (JULIANDAY(A.timeAdmitted) - JULIANDAY(A.date)) MaxSpan,
		MIN (JULIANDAY(A.timeAdmitted) - JULIANDAY(A.date)) MinSpan,
		AVG (JULIANDAY(A.timeAdmitted) - JULIANDAY(A.date)) AVGSpan
		FROM ((Patient join Admits using (patientID)) 
			join Discharges using (patientID)) as A
		WHERE (JULIANDAY(A.timeAdmitted) - JULIANDAY(A.date)) IN
		(select JULIANDAY(B.timeAdmitted) - JULIANDAY(B.date)
		 from ((Patient join Admits using (patientID)) 
			join Discharges using (patientID)) as B
		 where A.patientID = B.patientID
		 and (JULIANDAY(B.timeAdmitted) - JULIANDAY(A.date)) > 0)
		GROUP BY A.patientID) as T,
		(SELECT patientID,
		COUNT (A.timeAdmitted) as NumAdmissions,
		AVG (JULIANDAY(A.date) - JULIANDAY(A.timeAdmitted)) as AVGDuration
		FROM ((Patient join Admits using (patientID)) 
			join Discharges using (patientID)) as A
		GROUP BY A.patientID) as V
	WHERE T.patientID = V.patientID;'''):
          print(row)
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
    print('\t4.  Treatments Performed at the Hospital') 
    print('\t5.  Treatments Performed on Admitted Patients')
    print('\t6.  Treatments Performed on Outpatients') 
    print('\t7.  Diagnoses Associated with Patients with Highest Occurrences of ' 
           + 'Addmissions')
    print('\t8.  Employees Involved in a Given Treatment Occurance')
    
    num = raw_input('Enter a command: ')

    if (num == '1'):
      try:
        print('DiagnosisID, DiagnosisName, TotalOccurences')
        for row in c.execute('''SELECT d.diagnosisId, d.name AS diagnosisName, COUNT(d.diagnosisId) totalOccurences
          FROM InPatient ip 
            JOIN Patient p ON ip.patientId = p.patientId
	    JOIN Admits a ON p.patientId = a.patientId
	    JOIN Diagnoses d ON a.diagnosisId = d.diagnosisId
          GROUP BY d.diagnosisId
          ORDER BY COUNT(d.diagnosisId) DESC;'''):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in diagnosisAndTreatment 1:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '2'):
      try:
        print('DiagnosisID, DiagnosisName, TotalOccurences')
        for row in c.execute('''SELECT d.diagnosisId, d.name AS diagnosisName, COUNT(d.diagnosisId) totalOccurences
          FROM OutPatient op 
            JOIN Patient p ON op.patientId = p.patientId
            JOIN Admits a ON p.patientId = a.patientId
            JOIN Diagnoses d ON a.diagnosisId = d.diagnosisId
          GROUP BY d.diagnosisId
          ORDER BY COUNT(d.diagnosisId) DESC;'''):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in diagnosisAndTreatment 2:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '3'):
      try:
        print('DiagnosisID, Name, TotalOccurences')
        for row in c.execute('''SELECT d.diagnosisId, d.name, COUNT(DISTINCT d.diagnosisId)
          FROM Patient p
            JOIN Admits a ON p.patientId = a.patientId
            JOIN Diagnoses d ON a.diagnosisId = d.diagnosisId
          GROUP BY d.diagnosisId
          ORDER BY a.timeAdmitted DESC;'''):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in diagnosisAndTreatment 3:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])

    elif (num == '4'):
      try:
        print('TreatmentID, DiagnosisName, TotalOccurences')
        for row in c.execute('''SELECT t.treatmentId, t.name AS diagnosisName, COUNT(a.timeAdministered) totalOccurences
          FROM Treatment t JOIN Administers a ON t.treatmentId = a.treatmentId
          GROUP BY t.treatmentId
          ORDER BY COUNT(a.timeAdministered) DESC;'''):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in diagnosisAndTreatment 4:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '5'):
      try:
        print('TreatmentID, DiagnosisName, TotalOccurences')
        for row in c.execute('''SELECT t.treatmentId, t.name, COUNT(DISTINCT t.treatmentId)
          FROM Administers a JOIN Treatment t ON a.treatmentId = t.treatmentId
          WHERE a.patientId IN (
            SELECT patientId 
            FROM InPatient)
          GROUP BY t.treatmentId
          ORDER BY a.timeAdministered DESC;'''):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in diagnosisAndTreatment 5:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '6'):
      try:
        print('TreatmentID, DiagnosisName, TotalOccurences')
        for row in c.execute('''SELECT t.treatmentId, t.name, COUNT(DISTINCT t.treatmentId)
          FROM Administers a JOIN Treatment t ON a.treatmentId = t.treatmentId
          WHERE a.patientId IN ( SELECT patientId 
            FROM OutPatient)
          GROUP BY t.treatmentId
          ORDER BY a.timeAdministered DESC;'''):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in diagnosisAndTreatment 6:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '7'):
      try:
        print('PatientID, DiagnosisID, DiagnosisName')
        for row in c.execute('''SELECT p.patientId, d.diagnosisId, d.name 
          FROM Diagnoses d 
            JOIN Patient p ON d.patientId = p.patientId
	    JOIN Admits a ON p.patientId = a.patientId
          GROUP BY p.patientId
          HAVING COUNT(a.timeAdmitted) = (SELECT MAX(numAdmissions)
	    FROM (
              SELECT COUNT(timeAdmitted) numAdmissions
              FROM Admits
	    GROUP BY patientId))
          ORDER BY a.timeAdmitted DESC;'''):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in diagnosisAndTreatment 7:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '8'):
      requests = ['', '']
      requests[0] = raw_input('Enter a requestedTreatment ID: ')
      requests[1] = raw_input('Enter a requestedPatient ID: ')
      try:
        print('TreatmentGiverID, Firstname, LastName, DoctorID')
        for row in c.execute('''SELECT tg.treatmentGiverId, 
          p.firstName || ' ' || p.lastName AS patientName,
          d.employeeId AS doctorID
          FROM Treatment t
            JOIN Administers a ON t.treatmentId = a.treatmentId
	    JOIN TreatmentGiver tg ON a.treatmentGiverId = tg.treatmentGiverId
	    JOIN Doctor d ON tg.treatmentGiverId = d.treatmentGiverId
	    JOIN Patient p ON a.patientId = p.patientId
          WHERE t.treatmentId = ?
          AND p.patientId = ?;''', requests):
          print(row)
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
    print('\t3.  Primary Doctors of Patients with High Admission Rates') 
    print('\t4.  All Diagnoses Given by a Specified Doctor') 
    print('\t5.  All Treatments Ordered by a Given Doctor')
    print('\t6.  All Treatments in Which a Given Doctor Participated') 
    print('\t7.  Employees Involved in Every Treatment')
    
    num = raw_input('Enter a command: ')
    
    if (num == '1'):
      try:
        print('EmployeeID, FirstName, LastName, Category, HireDate')
        for row in c.execute('''SELECT employeeId, firstName, lastName, category, hireDate
          FROM (
            SELECT w.employeeId, w.firstName, w.lastName, 'Technician' AS category, w.hireDate
            FROM Worker w JOIN Technician t ON w.employeeId = t.employeeId
            UNION
            SELECT w.employeeId, w.firstName, w.lastName, 'Nurse' AS category, w.hireDate
            FROM Worker w JOIN Nurse n ON w.employeeId = n.employeeId
            UNION
            SELECT w.employeeId, w.firstName, w.lastName, 'Doctor' AS category, w.hireDate
            FROM Worker w JOIN Doctor d ON w.employeeId = d.employeeId
            UNION
            SELECT w.employeeId, w.firstName, w.lastName, 'Admin' AS category, w.hireDate
            FROM Worker w JOIN Admin a ON w.employeeId = a.employeeId
            UNION
            SELECT w.employeeId, w.firstName, w.lastName, 'Staff' AS category, w.hireDate
            FROM Worker w JOIN Staff s ON w.employeeId = s.employeeId
            UNION
            SELECT w.employeeId, w.firstName, w.lastName,'Volunteer' AS category, w.hireDate
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
        print('EmployeeID')
        for row in c.execute('''SELECT vi.employeeId
          FROM VolunteersIn vi
            JOIN Room r	ON vi.roomNumber = r.roomNumber
	    WHERE vi.dayOfWeek = 'Tuesday' AND r.roomDescription = 'Info Desk';'''):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in employeeInformation 2:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '3'):
      try:
        print('EmployeeID')
        for row in c.execute('''SELECT d.employeeId
	FROM (Patient as p 
		JOIN Admits as a
			USING (patientId))
		JOIN Doctor d 
			ON d.employeeId = a.employeeId
	GROUP BY patientID
	HAVING
		(SELECT COUNT(a.timeAdmitted)
		FROM Discharges d
		WHERE a.patientId = d.patientId 
		AND ((julianday(d.date) - julianday(a.timeAdmitted)) <= 365)) >= 4
	ORDER BY d.employeeId;'''):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in employeeInformation 3:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '4'):
      requestedDoctor = raw_input('Enter a doctor\'s employeeID: ')
      try:
        print('DiagnosisID, DiagnosisName, TotalOccurences')
        for row in c.execute('''SELECT d.diagnosisId, d.name AS diagnosisName, COUNT(d.diagnosisId) totalOccurences
          FROM Doctor doc JOIN Diagnoses d on doc.employeeId = d.doctorId
          WHERE doc.employeeId = ?
          GROUP BY d.diagnosisId
          ORDER BY COUNT(d.diagnosisId) DESC;''', (requestedDoctor,)):
          print(row)
      except sqlite3.OperationalError as err1:  
        print("\nSomething went wrong in employeeInformation 4:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '5'):
      requestedDoctor = raw_input('Enter a doctor\'s employeeID: ')
      try:
        print('DiagnosisName, TotalOccurences')
        for row in c.execute('''SELECT name, COUNT(*)
          FROM Doctor join Administers using (treatmentGiverID) join Treatment
          using (treatmentId)
          WHERE employeeID = ?
          GROUP BY name
          ORDER BY COUNT(*) DESC;''', requestedDoctor):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in employeeInformation 5:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '6'):
      requestedDoctor = raw_input('Enter a doctor\'s employeeId: ')
      try:
        print('TreatmentID, TotalAdministered')
        for row in c.execute('''SELECT t.treatmentId, COUNT(t.treatmentId) as totalAdministered
          FROM Doctor doc
            JOIN TreatmentGiver tg ON doc.treatmentGiverID = tg.treatmentGiverID
	    JOIN Administers a ON tg.treatmentGiverID = a.treatmentGiverID
	    JOIN Treatment t ON a.treatmentId = t.treatmentId
          WHERE doc.employeeId = ?
          GROUP BY t.treatmentId
          ORDER BY a.timeAdministered DESC;''', (requestedDoctor,)):
          print(row)
      except sqlite3.OperationalError as err1:
        print("\nSomething went wrong in employeeInformation 6:")
        print("sqlite3.OperationalError: {0}".format(err1))
      except:
        print("\nUnexpected Error: ", sys.exc_info()[0])
        
    elif (num == '7'):
      try:
        print('TreatmentGiverID')
        for row in c.execute('''SELECT IFNULL(tg.treatmentGiverID, "No employee has treated all patients.")
          FROM TreatmentGiver tg JOIN Administers a ON tg.treatmentGiverID = a.treatmentGiverID
          GROUP BY tg.treatmentGiverID
          HAVING COUNT(DISTINCT a.patientId) = (
            SELECT COUNT(DISTINCT a.patientId)
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
