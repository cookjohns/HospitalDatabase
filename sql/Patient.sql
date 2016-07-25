drop table if exists Patient;

CREATE TABLE Patient (
	patientId integer,
	firstName varchar(20) NOT NULL,
	lastName varchar(20) NOT NULL,
	insurancePolicy integer NOT NULL,
	emergencyContact varchar(50) NOT NULL,
	PRIMARY KEY (patientId)
);
