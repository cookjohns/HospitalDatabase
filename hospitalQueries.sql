-- A. Room Utilization
	--1) 
	-- List the rooms that are occupied, along with the associated patient names and the date the patient was admitted.
	-- WORKS!
	SELECT roomNumber, firstName, lastName, timeAdmitted, patientID
	FROM (Admits as A join PatientRoom using (patientID)) join Patient using (patientID)
	WHERE A.timeAdmitted > (select MAX (date)
							from Discharges as C
							where A.patientID = C.patientID);
	--2) 
	-- List the rooms that are currently unoccupied.
	-- WORKS!
	SELECT pr.roomNumber AS roomNumber
	FROM PatientRoom pr
	EXCEPT
	SELECT pr.roomNumber
	FROM PatientRoom pr
		JOIN (
			SELECT p.patientId
			FROM Patient p LEFT JOIN Discharges d ON p.patientId = d.patientId WHERE d.date IS NULL) currentPatients
		ON pr.patientId = currentPatients.patientId;

	--3) 
	-- List all rooms in the hospital along with patient names and admission dates for those that are occupied.
	SELECT allRooms.roomNumber, allRooms.firstName, allRooms.lastName, a.timeAdmitted
	FROM Admits a
		JOIN (
			SELECT pr.roomNumber, currentPatients.patientId, currentPatients.firstName, currentPatients.lastName
			FROM PatientRoom pr
			LEFT JOIN (
				SELECT p.patientId, p.firstName, p.lastName
				FROM Patient p LEFT JOIN Discharges d ON p.patientId = d.patientId WHERE d.date IS NULL) currentPatients
			ON pr.patientId = currentPatients.patientId) allRooms
		ON a.patientId = allRooms.patientId
	ORDER BY allRooms.roomNumber;
							
	SELECT pr.roomNumber, currentPatients.patientId, currentPatients.firstName, currentPatients.lastName
	FROM (PatientRoom pr
	LEFT JOIN
		(SELECT p.patientId, p.firstName, p.lastName
		FROM Patient p LEFT JOIN Discharges d ON p.patientId = d.patientId WHERE d.date IS NULL) currentPatients) join 
	ON currentPatients.patientId = pr.patientId;
	
	SELECT * FROM PatientRoom JOIN Admits ON PatientRoom.patientId = Admits.patientId;
	
	SELECT DISTINCT roomNumber, firstName, lastName, timeAdmitted, patientID
	FROM ((PatientRoom join Admits using (patientID))
			LEFT JOIN
			(SELECT roomNumber, firstName, lastName, timeAdmitted, patientID
			FROM (Admits as A join PatientRoom using (patientID)) join Patient using (patientID)
			WHERE A.timeAdmitted > (select MAX (date)
									from Discharges as C
									where A.patientID = C.patientID)) USING (timeAdmitted, roomNumber, patientID));
									
--B. Patient Information
	--1)
	-- List all patients in the database, with full personal information
	-- WORKS!
	SELECT *
	FROM Patient;
	
	--2)
	-- List all patients currently admitted to the hospital (i.e., those who are currently receiving inpatient services).
	-- List only patient identiﬁcation number and name.
	-- WORKS!
	SELECT currentPatients.patientId AS patientID, 
	currentPatients.firstName, currentPatients.lastName
	FROM InPatient ip
		JOIN (
			SELECT p.patientId, p.firstName, p.lastName
			FROM Patient p LEFT JOIN Discharges d ON p.patientId = d.patientId WHERE d.date IS NULL) currentPatients
		ON ip.patientId = currentPatients.patientId;
	
	--3)
	-- List all patients who were receiving inpatient services within a given date range. List only patient identiﬁcation number and name.
	-- NOTE: startDate and endDate are parameters provided by user (yyyy-mm-dd)
	-- WORKS!
	SELECT p.patientId, p.firstName, p.lastName
	FROM Patient p 
		JOIN InPatient ip 
			ON p.patientId = ip.patientId
		JOIN Administers a
			ON ip.patientId = a.patientId
	WHERE a.timeAdministered > startDate
	AND a.timeAdministered < endDate;
	
	--4)
	-- List all patients who were discharged in a given date range. List only patient identiﬁcation number and name.
	-- NOTE: startDate and endDate are parameters provided by user
	-- WORKS!
	SELECT p.patientId, p.firstName, p.lastName
	FROM Patient p JOIN Discharges d ON p.patientId = d.patientId
	WHERE d.date > startDate
	AND d.date < endDate; 
	
	--5)
	-- List all patients who are currently receiving outpatient services. 
	-- List only patient identiﬁcation number and name.
	-- WORKS!
	SELECT currentPatients.patientId AS patientID,
	currentPatients.firstName || ' ' || currentPatients.lastName AS patientName
	FROM OutPatient op
		JOIN (
			SELECT p.patientId, p.firstName, p.lastName
			FROM Patient p LEFT JOIN Discharges d ON p.patientId = d.patientId WHERE d.date IS NULL) currentPatients
		ON op.patientId = currentPatients.patientId;
	
	--6)
	-- List all patients who have received outpatient services within a given date range. List only patient identiﬁcation number and name.
	-- NOTE: startDate and endDate are parameters provided by user ('yyyy-mm-dd')
	-- WORKS!
	SELECT DISTINCT(OutPatientNames.patientId) AS patientId, 
	OutPatientNames.firstName || ' ' || OutPatientNames.lastName AS patientName
	FROM Admits a JOIN (
		SELECT p.patientId, p.firstName, p.lastName
		FROM Patient p JOIN OutPatient op ON p.patientId = op.patientId) OutPatientNames
	WHERE a.timeAdmitted > startDate
	AND a.timeAdmitted < endDate;
	
	--7)
	-- For a given patient (either patient identiﬁcation number or name), list all admissions to the hospital along with the diagnosis for each admission.
	-- NOTE: requestedPatient is a parameter provided by user
	-- Missing Diagnoses table
	SELECT a.timeAdmitted AS admission, d.diagnosisId, d.name AS diagnosisName
	FROM Diagnoses d
		JOIN Admits a
			ON d.diagnosisId = a.diagnosisId
		LEFT JOIN Patient p 
			ON a.patientId = p.patientId
	WHERE p.patientId = requestedPatient;
	
	--8)
	-- For a given patient (either patient identiﬁcation number or name), list all treatments that were administered. 
	-- Group treatments by admissions. List admissions in descending chronological order, and list treatments in 
	-- ascending chronological order within each admission.
	-- NOTE: requestedPatient is a parameter provided by user
	-- WORKS!
	SELECT patientTreatments.treatmentId AS treatmentId, patientTreatments.name AS name
	FROM Admits a 
	JOIN (
		SELECT t.treatmentId, t.name, treatedPatients.patientId
		FROM Treatment t 
			JOIN (
				SELECT p.patientId, a.treatmentId
				FROM Patient p JOIN Administers a ON p.patientId = a.patientId
				ORDER BY a.timeAdministered ASC) treatedPatients
			ON t.treatmentId = treatedPatients.treatmentId
		WHERE treatedPatients.patientId = requestedPatient) patientTreatments
	ON patientTreatments.patientId = a.patientId
	GROUP BY a.timeAdmitted
	ORDER BY a.timeAdmitted DESC;
	
	--9)
	-- UPDATE tablename SET creationDate=DATETIME(creationDate, '+330 minutes');
	-- NO IDEA
	
	--10)
	-- For each patient that has ever been admitted to the hospital, list their total number of admissions, average duration of each admission, longest span between admissions, shortest span between admissions, and average span between admissions.
	SELECT p.patientId, COUNT(a.admissions), duration??, longest span??, shortest span??, AVG(a.span)
	GROUP BY p.patientId
	
	--Avg duration of each admission
	SELECT MAX(julianday(d.date) - julianday(a.timeAdmitted)) 
	FROM Patient p 
		JOIN Discharges d 
			ON p.patientId = d.patientId
		JOIN Admits a
			ON p.patientId = a.patientId;
			
	--Longest span between admissions
	SELECT 
		
--C. Diagnosis and Treatment Information
	--1)
	-- List the diagnoses given to admitted patients, in descending order of occurrences. List diagnosis identiﬁcation number, name, and total occurrences of each diagnosis.
	-- WORKS!
	SELECT d.diagnosisId, d.name AS diagnosisName, COUNT(d.diagnosisId) totalOccurences
	FROM InPatient ip 
		JOIN Patient p
			ON ip.patientId = p.patientId
		JOIN Admits a
			ON p.patientId = a.patientId
		JOIN Diagnoses d
			ON a.diagnosisId = d.diagnosisId
	GROUP BY d.diagnosisId
	ORDER BY COUNT(d.diagnosisId) DESC;
	
	--2)
	-- List the diagnoses given to outpatients, in descending order of occurrences. List diagnosis identiﬁcation number, name, and total occurrences of each diagnosis.
	-- WORKS!
	SELECT d.diagnosisId, d.name AS diagnosisName, COUNT(d.diagnosisId) totalOccurences
	FROM OutPatient op 
		JOIN Patient p
			ON op.patientId = p.patientId
		JOIN Admits a
			ON p.patientId = a.patientId
		JOIN Diagnoses d
			ON a.diagnosisId = d.diagnosisId
	GROUP BY d.diagnosisId
	ORDER BY COUNT(d.diagnosisId) DESC;
	
	--3)
	-- List the diagnoses given to hospital patients (both inpatient and outpatient), in descending order of occurrences. List diagnosis identiﬁcation number, name, and total occurrences of each diagnosis.
	SELECT d.diagnosisId, d.name AS diagnosisName, COUNT(d.diagnosisId) AS totalOccurences
	FROM Patient p
		JOIN Admits a
			ON p.patientId = a.patientId
		JOIN Diagnoses d
			ON a.diagnosisId = d.diagnosisId
	GROUP BY d.diagnosisId
	ORDER BY COUNT(d.diagnosisId) DESC;
	
	--4)
	-- List the treatments performed at the hospital (to both inpatients and outpatients), in descending order of occurrences. List treatment identiﬁcation number, name, and total number of occurrences of each treatment.
	-- WORKS!
	SELECT t.treatmentId, t.name AS diagnosisName, COUNT(a.timeAdministered) totalOccurences
	FROM Treatment t JOIN Administers a ON t.treatmentId = a.treatmentId
	GROUP BY t.treatmentId
	ORDER BY COUNT(a.timeAdministered) DESC;
	
	--5)
	-- List the treatments performed on admitted patients, in descending order of occurrences. List treatment identiﬁcation number, name, and total number of occurrences of each treatment.
	-- WORKS!
	SELECT t.treatmentId, t.name, COUNT(DISTINCT t.treatmentId)
	FROM Administers a JOIN Treatment t ON a.treatmentId = t.treatmentId
	WHERE a.patientId IN (
						SELECT patientId 
						FROM InPatient)
	GROUP BY t.treatmentId
	ORDER BY a.timeAdministered DESC;
	
	--6)
	-- List the treatments performed on outpatients, in descending order of occurrences. List treatment identiﬁcation number, name, and total number of occurrences of each treatment.
	-- WORKS!
	SELECT t.treatmentId, t.name, COUNT(DISTINCT t.treatmentId)
	FROM Administers a JOIN Treatment t ON a.treatmentId = t.treatmentId
	WHERE a.patientId IN ( SELECT patientId 
						   FROM OutPatient)
	GROUP BY t.treatmentId
	ORDER BY a.timeAdministered DESC;
	
	--7)
	-- List the diagnoses associated with patients who have the highest occurrences of admissions to the hospital, in ascending order or correlation.
	-- WORKS!
	SELECT p.patientId, d.diagnosisId, d.name 
	FROM Diagnoses d 
		JOIN Patient p 
			ON d.patientId = p.patientId
		JOIN Admits a 
			ON p.patientId = a.patientId
	GROUP BY p.patientId
	HAVING COUNT(a.timeAdmitted) = (SELECT MAX(numAdmissions)
									FROM (
										SELECT COUNT(timeAdmitted) numAdmissions
										FROM Admits
										GROUP BY patientId)
									)
	ORDER BY a.timeAdmitted DESC;
	
	--8)
	-- For a given treatment occurrence, list all the hospital employees that were involved. Also include the patient name and the doctor who ordered the treatment.
	-- requestedTreatment and requestedPatient are parameters provided by user
	SELECT tg.treatmentGiverId, 
	p.firstName || ' ' || p.lastName AS patientName,
	d.employeeId AS doctorID
	FROM Treatment t
		JOIN Administers a 
			ON t.treatmentId = a.treatmentId
		JOIN TreatmentGiver tg 
			ON a.treatmentGiverId = tg.treatmentGiverId
		JOIN Doctor d 
			ON tg.treatmentGiverId = d.treatmentGiverId
		JOIN Patient p
			ON a.patientId = p.patientId
	WHERE t.treatmentId = requestedTreatment
	AND p.patientId = requestedPatient;
	
--D. Employee Information
	--1)
	-- WORKS!
	SELECT employeeId, firstName, lastName, category, hireDate
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
	ORDER BY lastName ASC, firstName ASC;
	
	--2)
	-- List the volunteers who work at the information desk on Tuesdays.
	-- WORKS! We don't have any volunteers who work Info Desk on Tuesdays
	SELECT vi.employeeId
	FROM VolunteersIn vi
		JOIN Room r
			ON vi.roomNumber = r.roomNumber
			WHERE vi.dayOfWeek = 'Tuesday' AND r.roomDescription = 'Info Desk';
	
	--3)
	-- How to handle 'within one year time frame'
	-- SELECT d.employeeId
	-- FROM ?
	-- GROUP BY p.patientId, a.date
	-- HAVING 
	
	--4)
	-- For a given doctor, list all associated diagnoses in descending order of occurrence. For each diagnosis, list the total number of occurrences for the given doctor.
	-- NOTE: requestedDoctor is a parameter provided by user
	SELECT d.diagnosisId, d.name AS diagnosisName, COUNT(d.diagnosisId) totalOccurences
	FROM Doctor doc JOIN Diagnoses d ON doc.employeeId = d.doctorId
	WHERE doc.employeeId = requestedDoctor
	GROUP BY d.diagnosisId
	ORDER BY COUNT(d.diagnosisId) DESC;
	
	--5)
	-- NOTE: requestedDoctor is a parameter provided by user
	-- FROM Doctor doc, Orders o, -- how do I do this with an aggregate?
	
	
	--6)
	-- For a given doctor, list all treatments in which they participated, in descending order of occurrence. For each treatment, list the total number of occurrences for the given doctor.
	-- NOTE: requestedDoctor is a parameter provided by user
	-- WORKS!
	SELECT t.treatmentId, COUNT(t.treatmentId) as totalAdministered
	FROM Doctor doc
		JOIN TreatmentGiver tg
			ON doc.treatmentGiverID = tg.treatmentGiverID
		JOIN Administers a
			ON tg.treatmentGiverID = a.treatmentGiverID
		JOIN Treatment t
			ON a.treatmentId = t.treatmentId
	WHERE doc.employeeId = requestedDoctor
	GROUP BY t.treatmentId
	ORDER BY a.timeAdministered DESC;
	
	--7)
	-- List employees who have been involved in the treatment of every admitted patient.
	-- I think this is right, we just don't have anyone who has treated every patient
	SELECT IFNULL(tg.treatmentGiverID, "No employee has treated all patients.")
	FROM TreatmentGiver tg JOIN Administers a ON tg.treatmentGiverID = a.treatmentGiverID
	GROUP BY tg.treatmentGiverID
	HAVING COUNT(DISTINCT a.patientId) = (
		SELECT COUNT(DISTINCT a.patientId)
		FROM Administers a);
	