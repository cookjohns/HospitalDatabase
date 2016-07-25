drop table if exists Nurse;

CREATE TABLE Nurse (
	employeeID integer,
	PRIMARY KEY (employeeID),
	FOREIGN KEY (employeeID) REFERENCES Worker.employeeID
);
