drop table if exists OutPatient;

CREATE TABLE OutPatient (
	patientId integer,
	PRIMARY KEY (patientId),
	FOREIGN KEY (patientId) REFERENCES Patient.patientId
);
