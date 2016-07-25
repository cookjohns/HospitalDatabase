drop table if exists Patient;

CREATE TABLE Patient (
	patientID integer,
	firstName varchar(20) NOT NULL,
	lastName varchar(20) NOT NULL,
	insurancePolicy integer NOT NULL,
	emergencyContact varchar(50) NOT NULL,
	PRIMARY KEY (patientID)
);
