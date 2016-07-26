drop table if exists Doctor;

CREATE TABLE Doctor (
	employeeID integer,
   treatmentGiverID integer NOT NULL UNIQUE,
	PRIMARY KEY (employeeID),
	FOREIGN KEY (employeeID) REFERENCES Worker(employeeID),
   FOREIGN KEY (treatmentGiverID) REFERENCES TreatmentGiver(treatmentGiverID)
);
