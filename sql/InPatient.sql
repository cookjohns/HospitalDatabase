drop table if exists InPatient;

CREATE TABLE InPatient (
	patientID integer,
	PRIMARY KEY (patientID),
	FOREIGN KEY (patientID) REFERENCES Patient(patientID)
);
