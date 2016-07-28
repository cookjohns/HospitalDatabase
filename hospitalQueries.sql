-- A. Room Utilization
	--1) 
	-- List the rooms that are occupied, along with the associated patient names and the date the patient was admitted.
	-- NOTE: We've got people who are admitted multiple times without being discharged, but we can hide it with group by...
	-- 
	SELECT occupiedRooms.roomNumber AS roomNumber, 
	occupiedRooms.firstName AS firstName, 
	occupiedRooms.lastName AS lastName, 
	a.timeAdmitted AS timeAdmitted
	FROM Admits a 
		JOIN (
			SELECT pr.roomNumber, currentPatients.patientId, currentPatients.firstName, currentPatients.lastName
			FROM PatientRoom pr
				JOIN (
					SELECT p.patientId, p.firstName, p.lastName
					FROM Patient p LEFT JOIN Discharges d ON p.patientId = d.patientId WHERE d.date IS NULL) currentPatients
				ON pr.patientId = currentPatients.patientId) occupiedRooms
		ON a.patientId = occupiedRooms.patientId
	GROUP BY occupiedRooms.roomNumber
	ORDER BY occupiedRooms.roomNumber, a.timeAdmitted;
	
	SELECT roomNumber, firstName, lastName, timeAdmitted, patientID
	FROM (Admits as A join PatientRoom using (patientID)) join Patient using (patientID)
	WHERE A.timeAdmitted > (select MAX (date)
							from Discharges as C
							where A.patientID = C.patientID);
	--2) 
	-- List the rooms that are currently unoccupied.
	-- WORKS!
	SELECT pr.roomNumber
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
	-- NOTE: Weird admits data, can hide with GROUP BY
	-- D:
	SELECT allRooms.patientId --allRooms.roomNumber, allRooms.firstName, allRooms.lastName, a.timeAdmitted
	FROM Admits a
		JOIN (
			SELECT pr.roomNumber, currentPatients.patientId, currentPatients.firstName, currentPatients.lastName
			FROM PatientRoom pr
			LEFT JOIN (
				SELECT p.patientId, p.firstName, p.lastName
				FROM Patient p LEFT JOIN Discharges d ON p.patientId = d.patientId WHERE d.date IS NULL) currentPatients
			ON pr.patientId = currentPatients.patientId) allRooms
		ON a.patientId = allRooms.patientId
	-- GROUP BY allRooms.roomNumber
	ORDER BY allRooms.roomNumber;
	
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
	SELECT a.date, d.diagnosis, p.patientId
	FROM Diagnoses d
		JOIN Admits a
			ON d.diagnosesId = a.diagnosesId
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
	-- NOT RIGHT NOW
	
	
--C. Diagnosis and Treatment Information
	--1)
	SELECT d.diagnosisId, d.name, COUNT(DISTINCT d.diagnosesId)
	FROM InPatient ip 
		JOIN Patient p
			ON ip.patientId = p.patientId
		JOIN Admits a
			ON p.patientId = a.patientId
		JOIN Diagnoses d
			ON a.diagnosisId = d.diagnosisId
	GROUP BY d.diagnosisId
	ORDER BY a.date DESC;
	
	--2)
	SELECT d.diagnosisId, d.name, COUNT(DISTINCT d.diagnosesId)
	FROM OutPatient op 
		JOIN Patient p
			ON op.patientId = p.patientId
		JOIN Admits a
			ON p.patientId = a.patientId
		JOIN Diagnoses d
			ON a.diagnosisId = d.diagnosisId
	GROUP BY d.diagnosisId
	ORDER BY a.date DESC;
	
	--3)
	SELECT d.diagnosisId, d.name, COUNT(DISTINCT d.diagnosesId)
	FROM Patient p
		JOIN Admits a
			ON p.patientId = a.patientId
		JOIN Diagnoses d
			ON a.diagnosisId = d.diagnosisId
	GROUP BY d.diagnosisId
	ORDER BY a.date DESC;
	
	--4)
	-- List the treatments performed at the hospital (to both inpatients and outpatients), in descending order of occurrences. List treatment identiﬁcation number, name, and total number of occurrences of each treatment.
	-- Treatments, Patient, Admits
	
	--5)
	-- List the treatments performed on admitted patients, indescending order of occurrences. List treatment identiﬁcation number, name, and total number of occurrences of each treatment.
	-- Treatments, InPatient, t.date DESC, 
	SELECT t.treatmentId, t.name, COUNT(DISTINCT t.treatmentId)
	FROM 
	GROUP BY t.treatmentId
	ORDER BY a.timeAdministered;
	
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
	SELECT vi.employeeId
	FROM VolunteersIn vi
		JOIN Room r
			ON vi.roomNumber = r.roomNumber
			WHERE vi.dayOfWeek = 'Tuesday' AND r.roomDescription = 'Info Desk';
	
	SELECT v.employeeId
	FROM Volunteer v
		JOIN VolunteersIn vi
			ON v.employeeId = vi.employeeId
		JOIN VolunteerRoom vr
			ON vi.roomId = vr.roomId
		JOIN InfoDesk id
			ON vr.roomId = id.roomId
	WHERE vi.;
	
	--3)
	-- How to handle 'within one year time frame'
	-- SELECT d.employeeId
	-- FROM ?
	-- GROUP BY p.patientId, a.date
	-- HAVING 
	
	--4)
	-- NOTE: requestedDoctor is a parameter provided by user
	SELECT d.diagnosis, COUNT(d.diagnosis) totalOccurences
	FROM Doctor doc JOIN Diagnoses d ON doc.employeeId = d.employeeId
	WHERE doc.employeeId = requestedDoctor
	GROUP BY d.diagnosis
	ORDER BY d.date DESC;
	
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
	SELECT tg.treatmentGiverID
	FROM TreatmentGiver tg JOIN Administers a ON tg.treatmentGiverID = a.treatmentGiverID
	GROUP BY tg.treatmentGiverID
	HAVING COUNT(DISTINCT a.patientId) = (
		SELECT COUNT(DISTINCT a.patientId)
		FROM Administers a);
	