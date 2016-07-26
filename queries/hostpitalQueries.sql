-- A. Room Utilization
	--1) 
	SELECT ra.roomNumber, p.firstName, p.lastName, a.date
	FROM RoomAssignment ra 
		JOIN Patient p 
			ON ra.patientId = p.patientId
		JOIN Admits a 
			ON p.patientId = a.patientId;
		
	--2) 
	SELECT pr.roomNumber 
	FROM PatientRoom pr LEFT JOIN RoomAssignment ra ON pr.roomNumber = ra.roomNumber
	WHERE ra.patientId IS NULL;

	--3) 
	-- NOTE: Are these only the occupied ones or do we have to check some dates somewhere?
	SELECT pr.roomNumber, p.firstName, p.lastName, a.admittedDate
	FROM PatientRoom pr 
		LEFT JOIN RoomAssignment ra 
			ON pr.roomNumber = ra.roomNumber
		JOIN Patient p 
			ON ra.patientId = p.patientId
		JOIN Admits a 
			ON p.patientId = a.patientId;
	
--B. Patient Information
	--1)
	SELECT *
	FROM Patient;
	
	--2)
	-- NOTE: must use left join to ensure all dates are shown (patients may come in more than once)
	SELECT patientId, firstName, lastName
	FROM (
		SELECT p.patientId, d.date
		FROM Patient p JOIN Discharges d ON p.patientId = d.patientId) DischargeDates
		LEFT JOIN ( 
		SELECT p.patientId, p.firstName, p.lastName
		FROM Patient p JOIN InPatients ip ON p.patientId = ip.patientId) InPatientNames
		ON DischargeDates.patientId = InPatientNames.patientId
	WHERE date IS NULL;
	
	--3)
	-- NOTE: startDate and endDate are parameters provided by user
	SELECT p.patientId, p.firstName, p.lastName
	FROM Patient p 
		JOIN InPatient ip 
			ON p.patientId = ip.patientId
		JOIN Administers a
			ON ip.patientId = a.patientId
	WHERE a.timeAdministered < startDate
	AND a.timeAdministered > endDate;
	
	--4)
	-- NOTE: startDate and endDate are parameters provided by user
	SELECT p.patientId, p.firstName, p.lastName
	FROM Patient p JOIN Discharges d ON p.patientId = d.patientId
	WHERE d.date > startDate
	AND d.date < endDate; 
	
	--5)
	SELECT patientId, firstName, lastName
	FROM (
		SELECT p.patientId, d.date
		FROM Patient p JOIN Discharges d ON p.patientId = d.patientId) DischargeDates
		LEFT JOIN ( 
		SELECT p.patientId, p.firstName, p.lastName
		FROM Patient p JOIN OutPatients op ON p.patientId = op.patientId) InPatientNames
		ON DischargeDates.patientId = InPatientNames.patientId
	WHERE date IS NULL;
	
	--6)
	-- NOTE: startDate and endDate are parameters provided by user
	SELECT p.patientId, p.firstName, p.lastName
	FROM Admits a JOIN (
		SELECT p.patientId, p.firstName, p.lastName
		FROM Patient p JOIN OutPatients op ON p.patientId = op.patientId) OutPatientNames
	WHERE a.date > startDate
	AND a.date < endDate;
	
	--7)
	-- NOTE: requestedPatient is a parameter provided by user
	SELECT a.date, d.diagnosis
	FROM Diagnoses d
		JOIN Admits a
			ON d.diagnosesId = a.diagnosesId
		LEFT JOIN Patient p 
			ON a.patientId = p.patientId
	WHERE p.patientId = requestedPatient;
	
	--8)
	-- NOTE: requestedPatient is a parameter provided by user
	SELECT admit.date, t.treatmentId
	FROM InPatient ip
		JOIN Administers admin
			ON ip.patientId = admin.patientId
		JOIN Treatment t
			ON a.treatmentId = t.treatmentId
		JOIN Admits admit
			ON admit.patientId = ip.patientId
	WHERE ip.patientId = requestedPatient
	GROUP BY admit.date
	ORDER BY admit.date DESC, admin.timeAdministered ASC;
	
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
	SELECT v.employeeId
	FROM Volunteer v
		JOIN VolunteersIn vi
			ON v.employeeId = vi.employeeId
		JOIN VolunteerRoom vr
			ON vi.roomId = vr.roomId
		JOIN InfoDesk id
			ON vr.roomId = id.roomId
	WHERE vi.dayOfWeek = 'Tuesday';
	
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
	-- NOTE: requestedDoctor is a parameter provided by user
	SELECT t.treatmentId, COUNT(t.treatmentId) as totalAdministered
	FROM Doctor doc
		JOIN TreatmentGiver tg
			ON doc.employeeId = tg.employeeId
		JOIN Administers a
			ON tg.employeeId = a.employeeId
		JOIN Treatment t
			ON a.treatmentId = treatmentId
	WHERE doc.employeeId = requestedDoctor
	GROUP BY t.treatmentId
	ORDER BY a.timeAdministered DESC;
	
	--7)
	SELECT tg.employeeId
	FROM TreatmentGiver tg JOIN Administers a ON tg.employeeId = a.employeeId
	GROUP BY tg.employeeId
	HAVING COUNT(DISTINCT a.patientId) = (
		SELECT COUNT(DISTINCT p.patientId)
		FROM Administers a);
	