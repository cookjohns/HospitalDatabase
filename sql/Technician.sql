drop table if exists Technician;

CREATE TABLE Technician (
	employeeId integer,
   treatmentGiverID integer NOT NULL UNIQUE,
	PRIMARY KEY (employeeID),
	FOREIGN KEY (employeeID) REFERENCES Worker(employeeID),
   FOREIGN KEY (treatmentGiverID) REFERENCES TreatmentGiver(treatmentGiverID)
);
