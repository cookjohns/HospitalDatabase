drop table if exists InPatient;

CREATE TABLE InPatient (
	patientId integer,
	PRIMARY KEY (patientId),
	FOREIGN KEY (patientId) REFERENCES Patient.patientId
);
