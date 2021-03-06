drop table if exists Nurse;

CREATE TABLE Nurse (
	employeeID integer,
   treatmentGiverID integer NOT NULL UNIQUE,
	PRIMARY KEY (employeeID),
	FOREIGN KEY (employeeID) REFERENCES Worker(employeeID),
   FOREIGN KEY (treatmentGiverID) REFERENCES TreatmentGiver(treatmentGiverID)
);
