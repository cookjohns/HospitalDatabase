drop table if exists OutPatient;

CREATE TABLE OutPatient (
	patientId integer,
	PRIMARY KEY (patientID),
	FOREIGN KEY (patientID) REFERENCES Patient.patientID
);
