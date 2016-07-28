drop table if exists Diagnoses;

CREATE TABLE Diagnoses (
   doctorID integer,
   patientID integer,
   diagnosisID integer,
   name varchar(20) NOT NULL,
   FOREIGN KEY (doctorID) REFERENCES Doctor (employeeID),
   FOREIGN KEY (patientID) REFERENCES Patient (patientID),
   PRIMARY KEY (doctorID, patientID, diagnosisID)
);
